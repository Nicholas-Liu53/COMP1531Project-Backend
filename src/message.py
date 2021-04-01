import src.data
from src.error import AccessError, InputError
import src.auth
from src.other import decode, get_channel, get_members, get_user, get_user_permissions, push_tagged_notifications
from datetime import timezone, datetime
import jwt
AuID      = 'auth_user_id'
uID       = 'u_id'
cID       = 'channel_id'
creatorID = 'creator_id'
allMems   = 'all_members'
Name      = 'name'
fName     = 'name_first'
lName     = 'name_last'
chans     = 'channels'
handle    = 'handle_string'
dmID      = 'dm_id'
seshID    = 'session_id'

def message_send_v1(token, channel_id, message):
    
    # Decode the token
    auth_user_id, _ = decode(token)

    # If the message is too long, raise InputError
    if len(message) > 1000:
        raise InputError

    # Check if user is in channel
    if auth_user_id not in get_channel(channel_id)['all_members']:
        raise AccessError

    now = datetime.now()
    time_created = int(now.strftime("%s"))
    newID = len(src.data.messages_log)

    # User is in the channel (which exists) & message is appropriate length
    #* Time to send a message
    src.data.messages_log.append(
        {
            'channel_id'    : channel_id,
            'dm_id'         : -1,
            'u_id'          : get_user(auth_user_id)['u_id'],
            'time_created'  : time_created,
            'message_id'    : newID,
            'message'       : message,
        }
    )

    #* Push notifications if anyone is tagged
    push_tagged_notifications(auth_user_id, channel_id, -1, message)

    return {
        'message_id': newID,
    }

def message_remove_v1(token, message_id):
    
    #* Decode the token
    auth_user_id, _ = decode(token)

    #* Get message dictionary in data
    messageFound = False
    messageDict = {}
    for message in src.data.messages_log:
        if message['message_id'] == message_id:
            messageDict = message
            messageFound = True
            break
    if not messageFound:
        raise InputError

    #* Check if the user is the writer, channel owner or owner of Dreams
    # Get the channel the message belongs to
    channel = get_channel(messageDict['channel_id'])
    if auth_user_id is not messageDict['u_id'] and auth_user_id not in channel['owner_members'] and get_user_permissions(auth_user_id) != 1:
        raise AccessError

    #* Remove the message
    message['message'] = '### Message Removed ###'

    return {
    }

def message_edit_v1(token, message_id, newMessage):
    
    #* Decode the token
    auth_user_id, _ = decode(token)

    #* Get message dictionary in data
    messageFound = False
    messageDict = {}
    for message in src.data.messages_log:
        if message['message_id'] == message_id:
            messageDict = message
            messageFound = True
            break
    if not messageFound:
        raise InputError

    #* Check if the user is the writer, channel owner or owner of Dreams
    # Get the channel the message belongs to
    channel = get_channel(messageDict['channel_id'])
    if auth_user_id is not messageDict['u_id'] and auth_user_id not in channel['owner_members'] and get_user_permissions(auth_user_id) != 1:
        raise AccessError

    if newMessage == '':    #* If new message is empty string --> remove message
        message_remove_v1(token, message_id)
    else:                   # Else 
        message['message'] = newMessage

    return {
    }

def message_senddm_v1(token, dm_id, message):
    auth_user_id, _ = decode(token)
    _, dmMembers = get_members(-1, dm_id)
    if auth_user_id not in dmMembers:
        raise AccessError
    if len(message) > 1000:
        raise InputError
    message_id = len(src.data.messages_log)
    now = datetime.now()
    time_created = int(now.strftime("%s"))
    
    src.data.messages_log.append({
        cID: -1,
        dmID: dm_id,
        'message_id': message_id,
        uID: auth_user_id,
        'message': message, 
        'time_created': time_created,
    })

    return {
        'message_id': message_id,
    }

def message_share_v1(token, og_message_id, message, channel_id, dm_id):

    # the authorised user has not joined the channel or DM they are trying to share the message to
    auth_user_id, _ = decode(token)

    # put message with optional message first,
    newMessage = ''
    for msg in src.data.messages_log:
        if msg["message_id"] == og_message_id:
            if message != '':
                newMessage = msg["message"] + " | " + message
            else:
                newMessage = msg["message"] 

    if dm_id == -1:
        for chans in src.data.channels:
            if chans["channel_id"] == channel_id:
                userAuth = False
                for users in chans["all_members"]:
                    if users == auth_user_id:
                        userAuth = True
                if not userAuth:
                    raise AccessError
        shared_message_id = message_send_v1(token, channel_id, newMessage)   
    elif channel_id == -1:
        for dm in src.data.dms:
            if dm['dm_id'] == dm_id:
                userAuth = False
                for users in dm['all_members']:
                    if users == auth_user_id:
                        userAuth = True
                if not userAuth:
                    raise AccessError
        shared_message_id = message_senddm_v1(token, dm_id, newMessage)
    else:
        # not an error in the spec sheet but if neither channel_id nor dm_id is not -1 or is both -1 probably raise inputerror
        pass #maybe return None
    
    return shared_message_id
