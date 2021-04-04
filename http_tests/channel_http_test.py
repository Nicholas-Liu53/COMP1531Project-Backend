import pytest
import requests
import json
from src.config import url
from src.other import SECRET
import jwt

AuID    = 'auth_user_id'
uID     = 'u_id'
cID     = 'channel_id'
allMems = 'all_members'
Name    = 'name'
dmName  = 'dm_name'
fName   = 'name_first'
lName   = 'name_last'
chans   = 'channels'
token   = 'token'
dmID    = 'dm_id'
handle  = 'handle_string'

#* Fixture that clears and registers the first user
@pytest.fixture
def user1():
    requests.delete(f"{url}clear/v1")    
    response = requests.post(f"{url}auth/register/v2", json={
        "email": "first@gmail.com",
        "password": "password",
        "name_first": "User",
        "name_last": "1"
    })
    return response.json()

#* Fixture that registers a second user
@pytest.fixture
def user2():
    response = requests.post(f"{url}auth/register/v2", json={
        "email": "second@gmail.com",
        "password": "password",
        "name_first": "User",
        "name_last": "2"
    })
    return response.json()

#* Fixture that registers a third user
@pytest.fixture
def user3():
    response = requests.post(f"{url}auth/register/v2", json={
        "email": "third@gmail.com",
        "password": "password",
        "name_first": "User",
        "name_last": "3"
    })
    return response.json()

#* Fixture that registers a fourth user
@pytest.fixture
def user4():
    response = requests.post(f"{url}auth/register/v2", json={
        "email": "fourth@gmail.com",
        "password": "password",
        "name_first": "User",
        "name_last": "4"
    })
    return response.json()

#* Fixture that returns a JWT with invalid u_id and session_id
@pytest.fixture
def invalid_token():
    return jwt.encode({'session_id': -1, 'user_id': -1}, SECRET, algorithm='HS256')

def test_http_channel_invite():
    pass

def test_http_channel_leave(user1, user2, user3, user4):
    pass

def test_http_channel_join(user1, user2, user3, user4):
    c1 = requests.post(f"{url}channels/create/v2", json={
        "token": user1[token],
        "name": "TrumpPence",
        "is_public": True
    })
    c2 = requests.post(f"{url}channels/create/v2", json={
        "token": user2[token],
        "name": "BidenHarris",
        "is_public": False
    })
    requests.post(f"{url}channel/join/v2", json={
        "token": user3[token],
        "channel_id": c1.json()['channel_id']
    })
    assert requests.get(f"{url}channel/details/v2", params={'token': user3[token], 'channel_id': c1.json()['channel_id']}).json() == {
        "name": "TrumpPence",
        "is_public": True,
        "owner_members": [
            {
                uID: user1[AuID],
                'email': "first@gmail.com",
                fName: "User",
                lName: "1",
                'handle_str': "user1"
            }
        ],
        "all_members": [
            {
                uID: user3[AuID],
                'email': "third@gmail.com",
                fName: "User",
                lName: "3",
                'handle_str': "user3"
            }
        ]
    }