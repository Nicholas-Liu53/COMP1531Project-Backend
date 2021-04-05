import pytest
import requests
import json
from src.config import url
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

def test_http_auth_logout_valid():
    requests.delete(f"{url}clear/v1")
    response_1 = requests.post(f"{url}auth/register/v2", json={"email": "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})
    payload_1 = response_1.json()
    response_2 = requests.post(f"{url}auth/login/v2", json={"email": "caricoleman@gmail.com", "password": "1234567"})
    payload_2 = response_2.json()
    
    reponse_3 = requests.delete(f"{url}auth/logout/v1", json={'token': payload_1['token']})
    payload_3 = response_3.json()
    assert payload_3['is_success'] = True

    with pytest.raises(AccessError):
        check_session(0, 0)

    reponse_4 = requests.delete(f"{url}auth/logout/v1", json={'token': payload_2['token']})
    payload_4 = response_4.json()
    assert payload_4['is_success'] = True

    with pytest.raises(AccessError):
        check_session(0, 1)

def test_http_auth_logout_v1_invalid():   
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json={"email": "caricoleman@gmail.com", "password": "1234567", "name_first": "cari", "name_last": "coleman"})

    token_1 = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')

    reponse_3 = requests.delete(f"{url}auth/logout/v1", json={'token': token_1})
    payload_3 = response_3.json()
    assert payload_3['is_success'] = False
    