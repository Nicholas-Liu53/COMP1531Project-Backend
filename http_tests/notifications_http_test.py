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

#* Fixture that returns a JWT with invalid u_id and session_id
@pytest.fixture
def invalid_token():
    return jwt.encode({'session_id': -1, 'user_id': -1}, SECRET, algorithm='HS256')

def test_http_notifications_get_in_channels(user1, user2, user3, user4):
    c1 = requests.post(f"{url}channels/create/v2", json={
        "token": user1[token],
        "name": "TrumpPence",
        "is_public": True
    })
    requests.post(f"{url}channel/invite/v2", json={
        "token": user1[token],
        "channel_id": c1.json()[cID],
        "u_id": user2[AuID]
    })
    notifFound = False
    for notif in requests.get(f"{url}notifications/get/v1", params={
        "token": user2[token]
    }).json()[notifs]:
        if notif[nMess] == "user1 added you to TrumpPence":
            notifFound = True
    assert notifFound is True
    requests.post(f"{url}message/send/v2", json={
        "token": user2[token],
        "channel_id": c1.json()['channel_id'],
        "message": "Hello @user1"
    })
    notifFound = False
    for notif in requests.get(f"{url}notifications/get/v1", params={
        "token": user1[token]
    }).json()[notifs]:
        if notif[nMess] == f"user2 tagged you in TrumpPence: Hello @user1":
            notifFound = True
    assert notifFound is True

    i = 0
    while i < 22:
        requests.post(f"{url}message/send/v2", json={
            "token": user1[token],
            "channel_id": c1.json()['channel_id'],
            "message": "Hi @user2"
        })
        i += 1
    notifFound = False
    for notif in requests.get(f"{url}notifications/get/v1", params={
        "token": user2[token]
    }).json()[notifs]:
        if notif[nMess] == "user1 added you to TrumpPence":
            notifFound = True
    assert notifFound is False

    requests.post(f"{url}message/send/v2", json={
        "token": user1[token],
        "channel_id": c1.json()['channel_id'],
        "message": "Dooo dooo dooo dooo @user2"
    })
    notifFound = False
    for notif in requests.get(f"{url}notifications/get/v1", params={
        "token": user2[token]
    }).json()[notifs]:
        if notif[nMess] == "user1 tagged you in TrumpPence: Dooo dooo dooo dooo ":
            notifFound = True
    assert notifFound is True

    requests.post(f"{url}message/send/v2", json={
        "token": user1[token],
        "channel_id": c1.json()['channel_id'],
        "message": "@Joe_Biden"
    })
    notifFound = False
    for notif in requests.get(f"{url}notifications/get/v1", params={
        "token": user2[token]
    }).json()[notifs]:
        if notif[nMess] == "user1 tagged you in TrumpPence: @Joe_Biden":
            notifFound = True
    assert notifFound is False

def test_http_notifications_dms_added(user1, user2, user3):
    pass

def test_http_valid_dm_tag(user1, user2):
    dmResponse = requests.post(f"{url}dm/create/v1", json={
        "token": user1[token],
        "u_ids": [user2[AuID]]
    })
    dm1 = dmResponse.json()

    requests.post(f"{url}message/senddm/v1", json={
        token: user1[token],
        dmID: dm1[dmID],
        'message': 'Hi @user2'
    })

    requests.post(f"{url}message/senddm/v1", json={
        token: user2[token],
        dmID: dm1[dmID],
        'message': 'Hi @user1'
    })

    response0 = requests.get(f"{url}notifications/get/v1", params={
        "token": user1[token]
    })
    notifs0 = response0.json()
    response1 = requests.get(f"{url}notifications/get/v1", params={
        "token": user2[token]
    })
    notifs1 = response1.json()

    assert len(notifs0['notifications']) == 1
    assert len(notifs1['notifications']) == 2

def test_http_valid_dm_20_chars(user1, user2):
    dmResponse = requests.post(f"{url}dm/create/v1", json={
        "token": user1[token],
        "u_ids": [user2[AuID]]
    })
    dm1 = dmResponse.json()
    message = '@user2' + ' ' + f"{'a'*25}"
    requests.post(f"{url}message/senddm/v1", json={
        token: user1[token],
        dmID: dm1[dmID],
        'message': message
    })
    response1 = requests.get(f"{url}notifications/get/v1", params={
        "token": user2[token]
    })
    notifs = response1.json()

    assert {
        cID : -1,
        dmID: dm1[dmID],
        nMess : f"user1 tagged you in user1, user2: {message[0:20]}",
    } in notifs['notifications']


def test_http_dm_no_tag(user1, user2, user3):
    dmResponse = requests.post(f"{url}dm/create/v1", json={
        "token": user1[token],
        "u_ids": [user2[AuID]]
    })
    dm1 = dmResponse.json()
    requests.post(f"{url}message/senddm/v1", json={
        token: user1[token],
        dmID: dm1[dmID],
        'message': 'Hi @user3'
    })
    response1 = requests.get(f"{url}notifications/get/v1", params={
        "token": user3[token]
    })
    notifs = response1.json()

    assert notifs['notifications'] == []

def test_http_dm_20_notifs(user1, user2):
    pass

def test_http_dm_edit_notif(user1, user2):
    pass