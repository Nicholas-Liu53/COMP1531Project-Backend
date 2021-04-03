import src.data
from src.error import AccessError, InputError
import re
from src.other import decode, check_session, get_user

def user_profile_v2(token, u_id):
    auth_user_id, session_id = decode(token)

    return {
        'user': get_user(u_id)
    }

def user_setname_v2(token, name_first, name_last):
    auth_user_id, session_id = decode(token)
    
    if len(name_first) > 50 or len(name_first) < 1:
        raise InputError
    if len(name_last) > 50 or len(name_last) < 1:
        raise InputError
        
    for user in src.data.users:
        if auth_user_id == user['u_id']:
            user['name_first'] = name_first
            user['name_last'] = name_last
    return {
    }

def user_setemail_v2(token, email):
    auth_user_id, session_id = decode(token)
    
    if not re.search('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$', email):
        raise InputError
        
    for user in src.data.users:
        if email == user['email']:
            raise InputError
            
    for user in src.data.users:
        if auth_user_id == user['u_id']:
            user['email'] = email
             
    return {
    }

def user_sethandle_v2(token, handle_str):
    auth_user_id, session_id = decode(token)
    
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError
    
    for user in src.data.users:
        if handle_str == user['handle_string']:
            raise InputError
            
    for user in src.data.users:
        if auth_user_id == user['u_id']:
            user['handle_string'] = handle_str
            
    return {
    }

def users_all(token):
    auth_user_id, session_id = decode(token)
    
    user_list = []
    
    for user in src.data.users:
        user_list.append(get_user(user['u_id']))
        
    return { 'users': user_list
    
    }
    
    
    
    
