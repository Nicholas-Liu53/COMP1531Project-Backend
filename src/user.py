import src.data
from src.error import AccessError, InputError
import re
from src.other import decode, check_session, get_user

def user_profile_v2(token, u_id):
    auth_user_id, session_id = decode(token)

    return {
        'user': get_user(u_id)
    }

def user_profile_setname_v1(auth_user_id, name_first, name_last):
    return {
    }

def user_profile_setemail_v1(auth_user_id, email):
    return {
    }

def user_profile_sethandle_v1(auth_user_id, handle_str):
    return {
    }