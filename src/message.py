import src.data
from src.error import AccessError, InputError
import jwt
from datetime import timezone, datetime
from src.other import decode, get_channel, get_members, get_user
SECRET = 'MENG'

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

def message_send_v2(token, channel_id, message):
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

    # User is in the channel (which exists) & message is appropriate length
    #* Time to send a message
    src.data.messages_log.append(
        {
            'channel_id'    : channel_id,
            'dm_id'         : -1,
            'handle_string' : get_user(auth_user_id)['handle_string'],
            'time_created'  : time_created,
            'message_id'    : len(data.messages_log),
            'message_string': message,
        }
    )

    return {
        'message_id': 1,
    }

def message_remove_v1(auth_user_id, message_id):
    return {
    }

def message_edit_v1(auth_user_id, message_id, message):
    return {
    }

def message_senddm_v1(token, dm_id, message):
    auth_user_id, _ = decode(token)
    _, dmMembers = get_members(-1, dm_id)
    if auth_user_id not in dmMembers:
        raise AccessError

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
        shared_message_id = message_send_v2(token, channel_id, newMessage)   
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
    
    return {
        shared_message_id
    }

