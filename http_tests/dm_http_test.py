import pytest
import requests
import src.other, src.auth
from src.dm import dm_create_v1
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
handle  = 'handle_str'

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
        "name_last": "2"}
    )
    return response.json()

#* Fixture that registers a third user
@pytest.fixture
def user3():
    response = requests.post(f"{url}auth/register/v2", json={
        "email": "third@gmail.com",
        "password": "password",
        "name_first": "User",
        "name_last": "3"}
    )
    return response.json()

#* Fixture that returns a JWT with invalid u_id and session_id
@pytest.fixture
def invalid_token():
    return jwt.encode({'session_id': -1, 'user_id': -1}, SECRET, algorithm='HS256')


def test_http_dm_details_valid(user1, user2):
    dmResponse = requests.post(f"{url}dm/create/v1", json={
        "token": user1[token],
        "u_ids": [user2[AuID]]
    })
    dm1 = dmResponse.json()
    expected = {
        Name: 'user1, user2',
        'members': [{
            uID: user1[AuID], 
            fName: "User",
            lName: '1',
            'email': 'first@gmail.com',
            handle: 'user1',
        }, {
            uID: user2[AuID], 
            fName: "User",
            lName: '2',
            'email': 'second@gmail.com',
            handle: 'user2',
        }
        ]
    }
    responseUser1 = requests.get(f"{url}dm/details/v1", params = {'token': user1[token], 'dm_id': dm1[dmID]})
    responseUser2 = requests.get(f"{url}dm/details/v1", params = {'token': user2[token], 'dm_id': dm1[dmID]})

    assert responseUser1.json() == expected
    assert responseUser2.json() == expected

def test_http_dm_details_invalid_dm_id(user1):
    invalid_dmID = -2
    response = requests.get(f"{url}dm/details/v1", params = {'token': user1[token], 'dm_id': invalid_dmID})
    assert response.status_code == 400

def test_http_dm_details_not_in_dm(user1, user2, user3):
    responseDM = requests.post(f"{url}dm/create/v1", json={
        "token": user1[token],
        "u_ids": [user2[AuID]]
    })
    dm1 = responseDM.json()
    response = requests.get(f"{url}dm/details/v1", params = {'token': user3[token], 'dm_id': dm1[dmID]})
    
    assert response.status_code == 403

def test_http_dm_list_none(user1):
    response = requests.get(f"{url}dm/list/v1", params = {'token': user1[token]})
    assert response.json() == {'dms': []}

def test_http_dm_list(user1, user2, user3):
    requests.post(f"{url}dm/create/v1", json={
        "token": user1[token],
        "u_ids": [user2[AuID]]
    })
    dmResponse = requests.post(f"{url}dm/create/v1", json={
        "token": user1[token],
        "u_ids": [user3[AuID]]
    })

    dm2 = dmResponse.json()
    response = requests.get(f"{url}dm/list/v1", params = {'token': user3[token]})
    assert response.json() == {'dms': [{
        dmID: dm2[dmID],
        Name: 'user1, user3'
    }]}

def test_http_dm_create(user1, user2):
    dmResponse = requests.post(f"{url}dm/create/v1", json={
        "token": user1[token],
        "u_ids": [user2[AuID]]
    })

    assert dmResponse.json() == {
        dmID: 0,
        'dm_name': 'user1, user2',
    }

def test_http_dm_create_invalid_u_ids(user1):
    invalid_u_id = -1
    dmResponse = requests.post(f"{url}dm/create/v1", json={
        "token": user1[token],
        "u_ids": [invalid_u_id]
    })

    assert dmResponse.status_code == 400

def test_dm_remove():
    pass

def test_dm_invite():
    pass

def test_dm_leave():
    pass

def test_dm_messages():
    pass

def test_http_dm_invalid_user(invalid_token):
    pass