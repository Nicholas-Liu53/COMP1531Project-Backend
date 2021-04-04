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

def test_http_message_send(user1, user2, user3, user4):
    c1 = requests.post(f"{url}channels/create/v2", json={
        "token": user1[token],
        "name": "TrumpPence",
        "is_public": True
    })
    requests.post(f"{url}channel/join/v2", json={
        "token": user2[token],
        "channel_id": c1.json()['channel_id']
    })
    requests.post(f"{url}channel/join/v2", json={
        "token": user3[token],
        "channel_id": c1.json()['channel_id']
    })
    message = ''
    for _ in range(1500):
        message += '?'
    assert requests.post(f"{url}message/send/v2", json={
        "token": user1[token],
        "channel_id": c1.json()['channel_id'],
        "message": message
    }).status_code == 400
    assert requests.post(f"{url}message/send/v2", json={
        "token": user4[token],
        "channel_id": c1.json()['channel_id'],
        "message": "?"
    }).status_code == 403
    m1 = requests.post(f"{url}message/send/v2", json={
        "token": user3[token],
        "channel_id": c1.json()['channel_id'],
        "message": "Sup"
    }).json()
    messageFound = False
    for messageDict in requests.get(f"{url}channel/messages/v2", params={
        "token": user1[token],
        "channel_id": c1.json()['channel_id'],
        "start": 0
    }).json()['messages']:
        if m1['message_id'] == messageDict['message_id']:
            messageFound = True
            break
    assert messageFound is True

def test_http_message_edit(user1, user2, user3, user4):
    c1 = requests.post(f"{url}channels/create/v2", json={
        "token": user2[token],
        "name": "TrumpPence",
        "is_public": True
    })
    requests.post(f"{url}channel/join/v2", json={
        "token": user1[token],
        "channel_id": c1.json()['channel_id']
    })
    requests.post(f"{url}channel/join/v2", json={
        "token": user3[token],
        "channel_id": c1.json()['channel_id']
    })
    requests.post(f"{url}channel/join/v2", json={
        "token": user4[token],
        "channel_id": c1.json()['channel_id']
    })
    m1 = requests.post(f"{url}message/send/v2", json={
        "token": user3[token],
        "channel_id": c1.json()['channel_id'],
        "message": "Yo yo waz poppin'?"
    }).json()
    m2 = requests.post(f"{url}message/send/v2", json={
        "token": user3[token],
        "channel_id": c1.json()['channel_id'],
        "message": "Huh?"
    }).json()
    m3 = requests.post(f"{url}message/send/v2", json={
        "token": user3[token],
        "channel_id": c1.json()['channel_id'],
        "message": "John Cena"
    }).json()
    m4 = requests.post(f"{url}message/send/v2", json={
        "token": user3[token],
        "channel_id": c1.json()['channel_id'],
        "message": "Ricegum"
    }).json()
    requests.put(f"{url}message/edit/v2", json={
        "token": user1[token],
        "message_id": m1['message_id'],
        "message": "Jeffrey Meng"
    })
    editedMessage = {}
    for messageDict in requests.get(f"{url}channel/messages/v2", params={
        "token": user1[token],
        "channel_id": c1.json()['channel_id'],
        "start": 0
    }).json()['messages']:
        if m1['message_id'] == messageDict['message_id']:
            editedMessage = messageDict
            break
    assert editedMessage['message'] == 'Jeffrey Meng'
    requests.put(f"{url}message/edit/v2", json={
        "token": user2[token],
        "message_id": m2['message_id'],
        "message": "Jeffrey Meng"
    })
    editedMessage = {}
    for messageDict in requests.get(f"{url}channel/messages/v2", params={
        "token": user2[token],
        "channel_id": c1.json()['channel_id'],
        "start": 0
    }).json()['messages']:
        if m2['message_id'] == messageDict['message_id']:
            editedMessage = messageDict
            break
    assert editedMessage['message'] == 'Jeffrey Meng'
    requests.put(f"{url}message/edit/v2", json={
        "token": user3[token],
        "message_id": m3['message_id'],
        "message": "Jeffrey Meng"
    })
    editedMessage = {}
    for messageDict in requests.get(f"{url}channel/messages/v2", params={
        "token": user3[token],
        "channel_id": c1.json()['channel_id'],
        "start": 0
    }).json()['messages']:
        if m3['message_id'] == messageDict['message_id']:
            editedMessage = messageDict
            break
    assert editedMessage['message'] == 'Jeffrey Meng'
    requests.put(f"{url}message/edit/v2", json={
        "token": user4[token],
        "message_id": m4['message_id'],
        "message": "Jeffrey Meng"
    }).status_code == 403
    requests.put(f"{url}message/edit/v2", json={
        "token": user3[token],
        "message_id": m3['message_id'],
        "message": ""
    })
    messageFound = False
    for messageDict in requests.get(f"{url}channel/messages/v2", params={
        "token": user3[token],
        "channel_id": c1.json()['channel_id'],
        "start": 0
    }).json()['messages']:
        if m3['message_id'] == messageDict['message_id']:
            messageFound = True
            break
    assert messageFound is False
    requests.put(f"{url}message/edit/v2", json={
        "token": user2[token],
        "message_id": -1,
        "message": "Troll"
    }).status_code == 400
    tooLong = ""
    for _ in range(1001):
        tooLong += "?"
    requests.put(f"{url}message/edit/v2", json={
        "token": user2[token],
        "message_id": m4['message_id'],
        "message": tooLong
    }).status_code == 400
    d1 = requests.get(f"{url}dm/create/v1", params={
        "token": user1[token],
        "u_ids": [user2[AuID]]
    }).json()
    dM1 = requests.post(f"{url}message/senddm/v1", json={
        "token": user1[token],
        "dm_id": d1[dmID],
        "message": "Herp derp"
    })
    requests.put(f"{url}message/edit/v2", json={
        "token": user2[token],
        "message_id": dM1['message_id'],
        "message": "Jeffrey Meng"
    }).status_code == 403

def test_http_message_remove(user1, user2, user3, user4):
    pass

def test_http_message_share_todm(user1, user2, user3, user4):
    pass

def test_http_message_share_tochannel(user1, user2, user3, user4):
    pass

def test_http_message_share_dmtodm(user1, user2, user3, user4):
    pass

def test_http_senddm_access_error(user1, user2, user3):
    pass

def test_http_senddm_long(user1, user2):
    dmResponse = requests.post(f"{url}dm/create/v1", json={
        "token": user1[token],
        "u_ids": [user2[AuID]]
    })
    dm1 = dmResponse.json()
    message = 'a'*1001
    response = requests.post(f"{url}message/senddm/v1", json={
        token: user1[token],
        dmID: dm1[dmID],
        'message': message
    })

    assert response.status_code == 400

def test_http_senddm_multiple(user1, user2):
    pass

def test_http_dm_unauthorised_user(user1, user2, invalid_token):
    pass