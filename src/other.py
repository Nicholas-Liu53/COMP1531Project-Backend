import src.data
import jwt

SECRET = 'MENG'

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
    auth_user_id, session_id = payload.get('session_id'), payload.get('user_id')
    check_session(auth_user_id, session_id)
    return auth_user_id, session_id

def check_session(auth_user_id, session_id):
    for user in src.data.users:
        if auth_user_id == user[uID]:
            if session_id in user[session_id]:
                return
    raise AccessError