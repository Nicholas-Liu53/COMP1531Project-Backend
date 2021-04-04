import src.data
import jwt
import json
from src.error import AccessError, InputError

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
SECRET    = 'MENG'

def clear_v1():
    '''
    Clears the entire database

    Arguments: 
        None
    
    Exceptions:
        None

    Return value:
        None
    '''
    with open('data.json', 'w') as FILE:
        json.dump({
            'users': [],
            'channels': [],
            'dms': [],
            'messages_log': [],
            'notifs': {}
        }, FILE)

    src.data.users = []
    src.data.channels = []
    src.data.dms = []
    src.data.messages_log = []
    src.data.notifs = {}

def search_v1(token, query_str):
    '''
    Takes in a user's token and query string to return a list of messages that contains details about the message
    The search is not case-sensitive

    Arguments: 
        token      (str) - The JWT containing user_id and session_id of the user that is to view their notifs
        querty_str (str) - The string which the user inputted to find messages
    
    Exceptions:
        InputError - Occurs when the query_str is greater than 1000 characters

    Return value:
        Returns a dictionary containing a list of notifications with key 'messages'
            Contains:
                message_id,
                user_id,
                message string, and
                time_created.
    '''
    #* Decode the token
    auth_user_id, _ = decode(token)

    # When query_str is >1000 characters, InputError is raised
    if len(query_str) > 1000:
        raise InputError

    channelList = []
    #* Check which channels the user is in
    for channel in src.data.channels:
        if auth_user_id in channel[allMems]:
            channelList.append(channel[cID])
    
    DMList = []
    #* Check which DMs the user is in
    for dm in src.data.dms:
        if auth_user_id in dm[allMems]:
            DMList.append(dm['dm_id'])

    messages = []

    #* Add in every message in the channel/DM that contains query_str
    for message in src.data.messages_log:
        if (message[cID] in channelList or message['dm_id'] in DMList) and query_str.lower() in message['message'].lower():
            messages.append(
                {
                    'message_id': message['message_id'],
                    uID: message[uID],
                    'message': message['message'],
                    'time_created': message['time_created'],
                }
            )

    return {
        'messages': messages,
    }

########################################################################################
###                                                                                  ###
###                              Helper Functions below                              ###
###                                                                                  ###
########################################################################################

def decode(token):
    payload = jwt.decode(token, SECRET, algorithms='HS256')
    auth_user_id, session_id = payload.get('user_id'), payload.get('session_id')
    check_session(auth_user_id, session_id)
    return auth_user_id, session_id

def check_session(auth_user_id, session_id):
    data = json.load(open('data.json', 'r'))
    for user in data['users']:
        if auth_user_id == user[uID]:
            if session_id in user['session_id']:
                return
    raise AccessError

def get_channel(channel_id):
    data = json.load(open('data.json', 'r'))
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            return channel
    raise InputError

def get_user(user_id):
    data = json.load(open('data.json', 'r'))
    for user in data['users']:
        if user_id == user[uID]:
            return {
                uID: user[uID],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_string': user['handle_string'],
            }
    raise InputError

def get_members(channel_id, dm_id):
    data = json.load(open('data.json', 'r'))
    if dm_id == -1:
        for chanDetails in data['channels']:
            if channel_id == chanDetails[cID]:
                return chanDetails[Name], chanDetails[allMems]
        raise InputError
    else:
        for dmDetails in data['dms']:
            if dm_id == dmDetails[dmID]:
                return dmDetails[Name], dmDetails[allMems]
        raise InputError

def message_count(channel_id, dm_id):
    counter = 0
    data = json.load(open('data.json', 'r'))
    if dm_id == -1:
        for message in data['messages_log']:
            if channel_id == message[cID]:
                counter += 1
    else:
        for message in data['messages_log']:
            if dm_id == message[dmID]:
                counter += 1
    
    return counter

def get_user_permissions(user_id):
    data = json.load(open('data.json', 'r'))
    for user in data['users']:
        if user_id == user[uID]:
            return user['permission_id']
    raise InputError

def get_user_from_handlestring(handlestring):
    data = json.load(open('data.json', 'r'))
    for user in data['users']:
        if handlestring == user['handle_string']:
            return {
                uID: user[uID],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_string': user['handle_string'],
            }
    raise InputError

def get_message(message_id):
    data = json.load(open('data.json', 'r'))
    for message in data['message_log']:
        if message_id == message['message_id']:
            return message
    raise InputError

def get_dm(dm_id):
    data = json.load(open('data.json', 'r'))
    for dm in data['dms']:
        if dm_id == dm['dm_id']:
            return dm
    raise InputError

def push_tagged_notifications(auth_user_id, channel_id, dm_id, message):
    if channel_id == -1 and dm_id == -1:
        raise InputError
    elif channel_id != -1 and dm_id != -1:
        raise InputError
    taggerHandle = get_user(auth_user_id)['handle_string']
    if channel_id != -1:
        channelDMname = get_channel(channel_id)['name']
    else:
        channelDMname = get_dm(dm_id)['name']
    messageWords = message.split()
    atHandlesList = []
    for word in messageWords:
        if word.startswith('@') and word != '@':
            atHandlesList.append(word[1:])
    taggedUsersList = []
    for atHandle in atHandlesList:
        try:
            taggedUsersList.append(get_user_from_handlestring(atHandle)[uID])
        except:
            pass
    notification = {
        'channel_id': channel_id,
        'dm_id': dm_id,
        'notification_message': f"{taggerHandle} tagged you in {channelDMname}: {message[0:20]}"
    }
    for taggedUser in taggedUsersList:
        try:
            src.data.notifs[taggedUser].insert(0, notification)
        except:
            src.data.notifs[taggedUser] = []
            src.data.notifs[taggedUser].append(notification)

def push_added_notifications(auth_user_id, user_id, channel_id, dm_id):
    if channel_id == -1 and dm_id == -1:
        raise InputError
    elif channel_id != -1 and dm_id != -1:
        raise InputError
    taggerHandle = get_user(auth_user_id)['handle_string']
    if channel_id != -1:
        channelDMname = get_channel(channel_id)['name']
    else:
        channelDMname = get_dm(dm_id)['name']
    get_user(user_id)       # Checking if user_id is valid
    notification = {
        'channel_id': channel_id,
        'dm_id': dm_id,
        'notification_message': f"{taggerHandle} added you to {channelDMname}"
    }
    try:
        src.data.notifs[user_id].insert(0, notification)
    except:
        src.data.notifs[user_id] = []
        src.data.notifs[user_id].append(notification)
