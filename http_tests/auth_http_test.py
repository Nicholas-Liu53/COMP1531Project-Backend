import pytest
import requests
import json
from src.config import url
from src.error import AccessError, InputError
from src.auth import auth_login_v2, auth_register_v2
from src.other import clear_v1
from jwt import encode

import src.data

#400 for InputError    
#403 for AccessError

SECRET = "MENG"

def test_http_auth_login_valid():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={"email": "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    r = requests.post(f"{url}auth/login/v2", json={"email": "caricoleman@gmail.com", "password": "1234567"})
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    payload = r.json()
    assert payload['token'] == token
    assert payload['auth_user_id'] == 0

def test_http_auth_login_invalid_email():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={"email": "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    response = requests.post(f"{url}auth/login/v2", json={"email": "caricoleman.com", "password": "1234567"})
    assert response.status_code == 400

def test_http_auth_login_invalid_not_registered_email():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/login/v2", json={"email": "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    response = requests.post(f"{url}auth/login/v2", json={"email": "caricoleman@yahoo.com", "password": "1234567"})
    assert response.status_code == 400

def test_http_auth_login_invalid_incorrect_password():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={"email": "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    response = requests.post(f"{url}auth/login/v2", json={"email": "caricoleman@gmail.com", "password": "789101112"})
    assert response.status_code == 400

def test_http_auth_register_valid():
    requests.delete(f"{url}clear/v1")
    print(src.data.users)
    r = requests.post(f"{url}auth/register/v2", json={"email": "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    token = encode({'session_id': 0, 'user_id': 0}, SECRET, algorithm='HS256')
    payload = r.json()
    assert payload["token"] == token
    assert payload['auth_user_id'] == 0

def test_http_auth_register_invalid_email():
    requests.delete(f"{url}clear/v1")
    response = requests.post(f"{url}auth/register/v2", json={"email": "caricoleman.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    assert response.status_code == 400

def test_http_auth_register_invalid_email_in_use():
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={"email": "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    response = requests.post(f"{url}auth/register/v2", json={"email": "caricoleman@gmail.com", "password": "1234567", "name_first": "erica", "name_last": "mondy"})
    assert response.status_code == 400

def test_http_auth_register_invalid_password():
    requests.delete(f"{url}clear/v1")
    response = requests.post(f"{url}auth/register/v2", json={"email": "caricoleman@gmail.com", "password": "123", "name_first": "cari", "name_last": "coleman"})
    assert response.status_code == 400

def test_http_auth_register_invalid_empty_first_name():
    requests.delete(f"{url}clear/v1")
    response = requests.post(f"{url}auth/register/v2", json={"email": "caricoleman@gmail.com", "password": "1234567", "name_first": "", "name_last": "coleman"})
    assert response.status_code == 400

def test_http_auth_register_invalid_long_first_name():
    requests.delete(f"{url}clear/v1")
    response = requests.post(f"{url}auth/register/v2", json={"email": "caricoleman@gmail.com", "password": "1234567", "name_first": "cariiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii", "name_last": "coleman"})
    assert response.status_code == 400

def test_http_auth_register_invalid_empty_last_name():
    requests.delete(f"{url}clear/v1")
    response = requests.post(f"{url}auth/register/v2", json={"email": "caricoleman@gmail.com", "password": "1234567", "name_first": "", "name_last": ""})
    assert response.status_code == 400

def test_http_auth_register_invalid_long_last_name():
    requests.delete(f"{url}clear/v1")
    response = requests.post(f"{url}auth/register/v2", json={"email": "caricoleman@gmail.com", "password": "1234567", "name_first": "", "name_last": "colemaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaan"})
    assert response.status_code == 400






