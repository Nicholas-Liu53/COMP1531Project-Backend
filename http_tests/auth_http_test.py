import pytest
import requests
import json
from src.config import url
from src.error import AccessError, InputError
from src.auth import auth_login_v2, auth_register_v2
from src.other import clear_v1
from jwt import encode

SECRET = "MENG"

def test_http_auth_login_valid():
    clear_v1()
    requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    r = requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@gmail.com", "password": "1234567"})
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    payload = r.json()
    assert payload['token'] == token
    assert payload['auth_user_id'] == 0

def test_http_auth_login_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
        requests.post(f"{url}auth/login/v2", json={'email': "caricoleman.com", "password": "1234567"})

def test_http_auth_login_invalid_not_registered_email():
    clear_v1()
    with pytest.raises(InputError):
        requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
        requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@yahoo.com", "password": "1234567"})

def test_http_auth_login_invalid_incorrect_password():
    clear_v1()
    with pytest.raises(InputError):
        requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
        requests.post(f"{url}auth/login/v2", json={'email': "caricoleman@gmail.com", "password": "789101112"})

def test_http_auth_register_valid():
    clear_v1()
    r = requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    token = encode({'session_id': 0, 'user_id': 0}, SECRET, algorithm='HS256')
    payload = r.json()
    assert payload['token'] == token
    assert payload['auth_user_id'] == 0

def test_http_auth_register_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        requests.post(f"{url}auth/register/v2", json={'email': "caricoleman.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})

def test_http_auth_register_invalid_email_in_use():
    clear_v1()
    with pytest.raises(InputError):
        requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
        requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "erica", "name_last": "mondy"})
            
def test_http_auth_register_invalid_password():
    clear_v1()
    with pytest.raises(InputError):
        requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "123", "name_first": "cari", "name_last": "coleman"})

def test_http_auth_register_invalid_empty_first_name():
    clear_v1()
    with pytest.raises(InputError):
        requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "", "name_last": "coleman"})

def test_http_auth_register_invalid_long_first_name():
    clear_v1()
    with pytest.raises(InputError):
        requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "cariiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii", "name_last": "coleman"})

def test_http_auth_register_invalid_empty_last_name():
    clear_v1()
    with pytest.raises(InputError):
        requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "", "name_last": ""})

def test_http_auth_register_invalid_long_last_name():
    clear_v1()
    with pytest.raises(InputError):
        requests.post(f"{url}auth/register/v2", json={'email': "caricoleman@gmail.com", "password": "1234567", "name_first": "", "name_last": "colemaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaan"})






