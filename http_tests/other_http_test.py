import pytest
import requests
import json
from src.config import url
from src.other import SECRET
import jwt

AuID    = 'auth_user_id'
uID     = 'u_id'
cID     = 'channel_id'
mID     = 'message_id'
allMems = 'all_members'
Name    = 'name'
dmName  = 'dm_name'
fName   = 'name_first'
lName   = 'name_last'
chans   = 'channels'
token   = 'token'
dmID    = 'dm_id'
handle  = 'handle_string'
ownMems = 'owner_members'
notifs  = 'notifications'
nMess   = 'notification_message'

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

#* Fixture that registers a fifth user
@pytest.fixture
def user5():
    response = requests.post(f"{url}auth/register/v2", json={
        "email": "fifth@gmail.com",
        "password": "password",
        "name_first": "User",
        "name_last": "5"
    })
    return response.json()

#* Fixture that registers the first channel
@pytest.fixture
def channel1(user1):
    return requests.post(f"{url}channels/create/v2", json={
        "token": user1[token],
        "name": "TrumpPence",
        "is_public": True
    }).json

#* Fixture that registers a second channel
@pytest.fixture
def channel2(user2):
    return requests.post(f"{url}channels/create/v2", json={
        "token": user2[token],
        "name": "BidenHarris",
        "is_public": False
    }).json

#* Fixture that registers a dm
@pytest.fixture
def dm1(user1, user2):
    return requests.post(f"{url}dm/create/v1", json={
        "token": user1[token],
        "u_ids": [user2[AuID]]
    }).json()


#* Fixture that returns a JWT with invalid u_id and session_id
@pytest.fixture
def invalid_token():
    return jwt.encode({'session_id': -1, 'user_id': -1}, SECRET, algorithm='HS256')

def test_http_search_channels(user1, user2, user3, user4, channel1, channel2):
    pass

def test_http_search_dms(user1, user2, user3, dm1):
    pass