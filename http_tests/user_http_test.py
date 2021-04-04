import pytest
import requests
import json
from src.config import url
from src.error import AccessError, InputError
from src.user import user_profile_v2, user_setname_v2, user_setemail_v2, user_sethandle_v2, users_all
from src.auth import auth_register_v2, auth_login_v2
from src.other import clear_v1
from jwt import encode

SECRET = "MENG"

def test_http_user_profile_valid():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@gmail.com", "password": "1234567"})
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    response = requests.get(f"{url}user/profile/v2", param={'token': token, 'u_id': 0})
    payload = response.json()
    assert payload == { 
        'user':
            {
            'u_id': 0, 
            'email': "caricoleman@gmail.com", 
            'name_first': 'cari', 
            'name_last': 'coleman', 
            'handle_string': 'caricoleman'
            }
    }
    
def test_http_user_profile_invalid_uid():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@gmail.com", "password": "1234567"})
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    response = requests.get(f"{url}user/profile/v2", param={'token': token, 'u_id': 1})
    assert response.status_code == 400

def test_http_user_setname_valid():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@gmail.com", "password": "1234567"})
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    response_1 = requests.put(f"{url}user/profile/setname/v2", json={'token': token, 'name_first': 'kari', 'name_last': 'koleman'})
    payload_1 = response_1.json()
    assert payload_1 == {}
    response_2 = requests.get(f"{url}user/profile/v2", param={'token': token, 'u_id': 0})
    payload_2 = response_2.json()
    assert payload_2 == { 
        'user':
            {
            'u_id': 0, 
            'email': "caricoleman@gmail.com", 
            'name_first': 'kari', 
            'name_last': 'koleman', 
            'handle_string': 'caricoleman'
            }
    }

def test_http_user_setname_invalid_long_first_name():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@gmail.com", "password": "1234567"})
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    response = requests.put(f"{url}user/profile/setname/v2", json={'token': token, 'name_first': 'kariiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii', 'name_last': 'koleman'})
    payload = response.json()
    assert respons.status_code == 400

def test_http_user_setname_invalid_long_last_name():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@gmail.com", "password": "1234567"})
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    response = requests.put(f"{url}user/profile/setname/v2", json={'token': token, 'name_first': 'kari', 'name_last': 'kolemaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaan'})
    payload = response.json()
    assert respons.status_code == 400

def test_http_user_setname_invalid_no_first_name():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@gmail.com", "password": "1234567"})
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    response = requests.put(f"{url}user/profile/setname/v2", json={'token': token, 'name_first': '', 'name_last': 'koleman'})
    payload = response.json()
    assert respons.status_code == 400    

def test_http_user_setname_invalid_no_last_name():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@gmail.com", "password": "1234567"})
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    response = requests.put(f"{url}user/profile/setname/v2", json={'token': token, 'name_first': 'kari', 'name_last': ''})
    payload = response.json()
    assert respons.status_code == 400    

def test_http_user_setemail_valid():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@gmail.com", "password": "1234567"})
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    response_1 = requests.put(f"{url}user/profile/setemail/v2", json={'token': token, 'email': 'karicoleman@gmail.com'})
    payload_1 = response_1.json()
    assert payload_1 == {}
    response_2 = requests.get(f"{url}user/profile/v2", param={'token': token, 'u_id': 0})
    payload_2 = response_2.json()
    assert payload_2 == {
        'user':
        {
        'u_id': 0, 
        'email': "karicoleman@gmail.com", 
        'name_first': 'cari', 
        'name_last': 'coleman', 
        'handle_string': 'caricoleman'
        }
    }

def test_http_user_setemail_invalid_email():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@gmail.com", "password": "1234567"})
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    response = requests.put(f"{url}user/profile/setemail/v2", json={'token': token, 'email': 'karicoleman.com'})
    payload = response.json()
    assert respons.status_code == 400    

def test_http_user_setemail_invalid_email_in_use():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@gmail.com", "password": "1234567"})
    token_1 = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    requests.post(f"{url}auth/register/v2", json={'email': "eicamondy@gmail.com", "password": "1234567", "name_first": "erica", "name_last": "mondy"})
    requests.post(f"{url}auth/login/v2", json={'email': "ericamondy@gmail.com", "password": "1234567"})
    token_2 = encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')
    requests.put(f"{url}user/profile/setemail/v2", json={'token': token_1, 'email': 'karicoleman.com'})
    reponse = requests.put(f"{url}user/profile/setemail/v2", json={'token': token_2, 'email': 'karicoleman.com'})
    payload = response.json()
    assert respons.status_code == 400    

def test_http_user_sethandle_valid():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@gmail.com", "password": "1234567"})
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    reponse_1 = requests.put(f"{url}user/profile/sethandle/v2", json={'token': token, 'handle_string': 'karikoleman'})
    payload_1 = response_1.json()
    assert payload_1 == {}
    response_2 = requests.get(f"{url}user/profile/v2", param={'token': token, 'u_id': 0})
    payload_2 = response_2.json()
    assert payload_2 == {
        'user':
        {
        'u_id': 0, 
        'email': "caricoleman@gmail.com", 
        'name_first': 'cari', 
        'name_last': 'coleman', 
        'handle_string': 'karikoleman'
        }
    }

def test_http_user_sethandle_invalid_short_handle():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@gmail.com", "password": "1234567"})
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    response = requests.put(f"{url}user/profile/sethandle/v2", json={'token': token, 'handle_string': 'cc'})
    assert response.status_code == 400    

def test_http_user_sethandle_invalid_long_handle():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@gmail.com", "password": "1234567"})
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    response = requests.put(f"{url}user/profile/sethandle/v2", json={'token': token, 'handle_string': 'cariiiiiiiiiiiiiiiiii'})
    assert response.status_code == 400    

def test_http_user_sethandle_invalid_handle_in_use():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@gmail.com", "password": "1234567"})
    token_1 = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    response_1 = requests.put(f"{url}user/profile/sethandle/v2", json={'token': token_1, 'handle_string': 'kari'})
    payload_1 = response_1.json()
    assert payload_1 == {}
    requests.post(f"{url}auth/register/v2", json={'email': "ericamondy@gmail.com", "password": "1234567", "name_first": "erica", "name_last": "mondy"})
    requests.post(f"{url}auth/login/v2", json={'email': "ericamondy@gmail.com", "password": "1234567"})
    token_2 = encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')
    response_2 = requests.put(f"{url}user/profile/sethandle/v2", json={'token': token_2, 'handle_string': 'kari'})
    assert response_2.status_code == 400

def test_http_users_all_valid():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@gmail.com", "password": "1234567"})
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    requests.post(f"{url}auth/register/v2", json={'email': "ericamondy@gmail.com", "password": "1234567", "name_first": "erica", "name_last": "mondy"})
    requests.post(f"{url}auth/login/v2", json={'email': "ericamondy@gmail.com", "password": "1234567"})
    response = requests.get(f"{url}users/all/v1", param={'token': token,})
    payload = response.json()
    assert payload == {
            'users':
            [{
            'u_id': 0, 
            'email': "caricoleman@gmail.com", 
            'name_first': 'cari', 
            'name_last': 'coleman', 
            'handle_string': 'caricoleman'
            },
            {
            'u_id': 1, 
            'email': "ericamondy@gmail.com", 
            'name_first': 'erica', 
            'name_last': 'mondy', 
            'handle_string': 'ericamondy'
            }]
    } 
    


