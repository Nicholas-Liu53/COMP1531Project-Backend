import src.data
from src.error import AccessError, InputError

def auth_login_v1(email, password):
    try:
        for user in src.data.users:
            if email == user[email] and password == user['password']:
                return {
                    'auth_user_id': user['user_id'],
                }
    except: Exception(InputError) 



def auth_register_v1(email, password, name_first, name_last):
    src.data.users.append({
        'email' : email,
        'password' : password,
        'name_first' : name_first,
        'name_last' : name_last,
        'user_id' : name_first + name_last
    })
    return {
        'auth_user_id': name_first + name_last,
    }
