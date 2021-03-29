import src.data
import jwt
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

    src.data.users = []

    src.data.channels = []

def search_v1(auth_user_id, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }

def decode(token):
    payload = jwt.decode(token, SECRET, algorithms='HS256')
    auth_user_id, session_id = payload.get('user_id'), payload.get('session_id')
    check_session(auth_user_id, session_id)
    return auth_user_id, session_id

def check_session(auth_user_id, session_id):
    for user in src.data.users:
        if auth_user_id == user[uID]:
            if session_id in user['session_id']:
                return
    raise AccessError

def get_channel(channel_id):
    for channel in src.data.channels:
        if channel_id == channel['channel_id']:
            return channel
    raise InputError

def get_user(user_id):
    for user in src.data.users:
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
    if dm_id == -1:
        for chanDetails in src.data.channels:
            if channel_id == chanDetails[cID]:
                return chanDetails[Name], chanDetails[allMems]
        raise InputError
    else:
        for dmDetails in src.data.dms:
            if dm_id == dmDetails[dmID]:
                return dmDetails[Name], dmDetails[allMems]
        raise InputError

def message_count(channel_id, dm_id):
    counter = 0
    if dm_id == -1:
        for message in src.data.messages_log:
            if channel_id == src.data.messages_log[cID]:
                counter += 1
    else:
        for message in src.data.messages_log:
            if dm_id == src.data.messages_log[dmID]:
                counter += 1
    return counter
