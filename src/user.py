from src.error import AccessError, InputError
import re
from src.other import decode, check_session, get_user
import json

def user_profile_v2(token, u_id):
    """ Provided the u_id of an existing user with a valid token, returns information about the user 
        which corresponds with the u_id

        Arguments:
            token (str): The token containing the user_id and session_id of user that called the function
            u_id (int): The user_id of the user whose profile is being returned

        Exceptions:
            InputError : occurs when the inputted u_id does not correspond to a valid user
            AccessError : occurs when the session_id or u_id provided within the token does not 
                          correspond to a valid u_id and session_id
            
        Return Value:
            Returns (dict) containing the information of the user which corresponds to the provided u_id
            The information provided is the user_id, email, first name, last name and handle string of the user 

    """ 

    decode(token)

    return {
        'user': get_user(u_id)
    }

def user_setname_v2(token, name_first, name_last):
    """ Provided with a valid token, the first and last names of the user corresponding to the payload of the token are
        changed to the provided first and last name

        Arguments:
            token (str): The token containing the user_id and session_id of user that called the function
            name_first (str): The new first name of the user
            name_last (str): The new last name of the user

        Exceptions:
            InputError : occurs when the inputted first name has a length that is not between 1 and 50 
                         characters inclusively
            InputError : occurs when the inputted last name has a length that is not between 1 and 50 
                         characters inclusively
            AccessError : occurs when the session_id or u_id provided within the token does not 
                          correspond to a valid u_id and session_id
            
        Return Value:
            Returns an empty dictionary 

    """ 
    data = json.load(open('data.json', 'r'))

    auth_user_id, _ = decode(token)
    
    if len(name_first) > 50 or len(name_first) < 1:
        raise InputError
    if len(name_last) > 50 or len(name_last) < 1:
        raise InputError
        
    for user in data['users']:
        if auth_user_id == user['u_id']:
            user['name_first'] = name_first
            user['name_last'] = name_last

    with open('data.json', 'w') as FILE:
        json.dump(data, FILE)

    return {
    }

def user_setemail_v2(token, email):
    """ Provided with a valid token, the email of the user corresponding to the payload of the token is
        changed to the provided email

        Arguments:
            token (str): The token containing the user_id and session_id of user that called the function
            email (str): The new email of the user
        

        Exceptions:
            InputError : occurs when the inputted email is not a valid email format
            InputError : occurs when the inputted email has already been used by another user
            AccessError : occurs when the session_id or u_id provided within the token does not 
                          correspond to a valid u_id and session_id
            
        Return Value:
            Returns an empty dictionary 

    """ 
    data = json.load(open('data.json', 'r'))

    auth_user_id, _ = decode(token)
    
    if not re.search('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$', email):
        raise InputError
        
    for user in data['users']:
        if email == user['email']:
            raise InputError
            
    for user in data['users']:
        if auth_user_id == user['u_id']:
            user['email'] = email

    with open('data.json', 'w') as FILE:
        json.dump(data, FILE)
             
    return {
    }

def user_sethandle_v2(token, handle_str):
    """ Provided with a valid token, the handle string of the user corresponding to the payload of the token is
        changed to the provided handle string

        Arguments:
            token (str): The token containing the user_id and session_id of user that called the function
            handle_str (str): The new handle string of the user
        

        Exceptions:
            InputError : occurs when the inputted handle string has a length that is not between 3 and 20 
                         characters inclusively
            InputError : occurs when the inputted handle string has already been used by another user
            AccessError : occurs when the session_id or u_id provided within the token does not 
                          correspond to a valid u_id and session_id
            
        Return Value:
            Returns an empty dictionary 

    """ 
    data = json.load(open('data.json', 'r'))

    auth_user_id, _ = decode(token)
    
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError
    
    for user in data['users']:
        if handle_str == user['handle_str']:
            raise InputError
            
    for user in data['users']:
        if auth_user_id == user['u_id']:
            user['handle_str'] = handle_str

    with open('data.json', 'w') as FILE:
        json.dump(data, FILE)
            
    return {
    }

def users_all(token):
    """ Provided with a valid token, returns a list containing information on all registered users

        Arguments:
            token (str): The token containing the user_id and session_id of user that called the function
        
        Exceptions:
            InputError : occurs when the inputted handle string has a length that is not between 3 and 20 
                         characters inclusively
            InputError : occurs when the inputted handle string has already been used by another user
            AccessError : occurs when the session_id or u_id provided within the token does not 
                          correspond to a valid u_id and session_id
            
        Return Value:
            Returns (dict) containing a list of all users which contains dictionaries of information on each user
            The information provided is the user_id, email, first name, last name and handle string of each user 

    """ 
    data = json.load(open('data.json', 'r'))

    decode(token)
    
    user_list = []
    
    for user in data['users']:
        user_list.append(get_user(user['u_id']))
        
    return { 'users': user_list
    
    }
    
    
    
    
