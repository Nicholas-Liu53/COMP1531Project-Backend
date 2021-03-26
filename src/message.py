import src.data
from src.error import AccessError, InputError
import jwt

def check_session(auth_user_id, session_id):
    for user in src.data.users:
        if auth_user_id == user['u_id']:
            if session_id in user['session_id']:
                return
    raise AccessError


def decode(token):
    payload = jwt.decode(token, "MENG", algorithms = 'HS256')
    auth_user_id, session_id = payload.get('session_id'), payload.get('user_id')
    check_session(auth_user_id, session_id)
    return auth_user_id, session_id

def message_send_v2(auth_user_id, channel_id, message):
    return {
        'message_id': 1,
    }

def message_remove_v1(auth_user_id, message_id):
    return {
    }

def message_edit_v1(auth_user_id, message_id, message):
    return {
    }

def message_share_v1(token, og_message_id, message, channel_id, dm_id):

    # the authorised user has not joined the channel or DM they are trying to share the message to
    auth_user_id, _ = decode(token)
    
  
    
    return {
        shared_message_id
    }