import src.data
from src.error import AccessError, InputError
import src.auth
import jwt

SECRET = 'MENG'

AuID      = 'auth_user_id'
uID       = 'u_id'
cID       = 'channel_id'
creatorID = 'creator_id'
allMems   = 'all_members'
cName     = 'name'
fName     = 'name_first'
lName     = 'name_last'
chans     = 'channels'
handle    = 'handle_string'
dmID      = 'dm_id'
seshID    = 'session_id'

def dm_details_v1(token, dm_id):
    pass

def dm_list_v1(token):
    pass

def dm_create_v1(token, u_ids):
    creator_id, _ = decode(token)

    if len(src.data.dms) == 0:
        dmID = 0
    else:
        dmID = src.data.dms[-1][dmID] + 1

    dmUsers = u_ids.append(creator_id)
    handles = []
    for user in dmUsers:
        handles.append(get_handle(user))
    handles.sort()
    dm_name = ', '.join(handles)

    return {
        'dm_id': dmID,
        'dm_name': dm_name
    }

def dm_remove_v1(token, dm_id):
    pass

def dm_invite_v1(token, dm_id, u_id):
    pass

def dm_leave_v1(token, dm_id):
    pass

def dm_messages_v1(token, dm_id, start):
    pass

def decode(token):
    auth_user_id, session_id = jwt.decode(token, SECRET, algorithm='HS256')
    check_session(auth_user_id, session_id)
    return auth_user_id, session_id

def check_session(auth_user_id, session_id):
    for user in src.data.users:
        if auth_user_id == user[uID]:
            if session_id in user[session_id]:
                return
    raise AccessError

def get_handle(user_id):
    for user in src.data.users:
        if user_id == user[uID]:
            return user[handle]
    raise InputError