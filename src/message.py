import src.data
from src.error import AccessError, InputError
import src.auth
from src.other import decode, get_members
from datetime import datetime
import jwt

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

def message_send_v1(auth_user_id, channel_id, message):
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
