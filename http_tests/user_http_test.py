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
    clear_v1()
    requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@gmail.com", "password": "1234567"})
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    r = requests.get(f"{url}user/profile/v2", param={'token': token, 'u_id': 0})
    payload = r.json()
    assert payload['user']['uid'] == 0
    assert payload['user']['email'] == 'caricoleman@gmail.com'
    assert payload['user']['name_first'] == 'cari'
    assert payload['user']['name_last'] == 'coleman'
    assert payload['user']['handle_string'] == 'caricoleman'
    
def test_http_user_profile_invalid_uid():
    clear_v1()
    requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@gmail.com", "password": "1234567"})
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    requests.get(f"{url}user/profile/v2", param={'token': token, 'u_id': 1})
    

