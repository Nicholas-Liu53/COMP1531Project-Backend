import src.data
from src.error import AccessError, InputError
import jwt
from src.other import decode, get_channel, get_members, get_user, SECRET


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


def user_remove_v1():
    pass

def userpermission_change_v1(token, u_id, permission_id):

    auth_user_id, _ = decode(token)

    validUser = False
    validOwner = False
    for user in src.data.users:
        if user[uID] == u_id:
            validUser = True
        if user[uID] == auth_user_id:
            if user['permission_id'] == 1:
                validOwner = True
    if not validUser:
        raise InputError
    if not validOwner:
        raise AccessError
    
    if permission_id != 1 or permission_id != 2:
        raise InputError

    for user in src.data.user:
        if user[uID] == u_id:
            user['permission_id'] = permission_id

    return {
    }

def notifications_get_v1():
    pass
