import pytest
import requests
import src.other, src.auth
from src.dm import dm_create_v1
from src import config

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
    src.other.clear_v1()    
    return src.auth.auth_register_v2("first@gmail.com", "password", "User", "1")

#* Fixture that registers a second user
@pytest.fixture
def user2():
    return src.auth.auth_register_v2("second@gmail.com", "password", "User", "2")

#* Fixture that registers a third user
@pytest.fixture
def user3():
    return src.auth.auth_register_v2("third@gmail.com", "password", "User", "3")

def test_dm_details_empty(user1, user2):
    # dmResponse = requests.post(f"{config.url}dm/create/v1", json={
    #     'token': user1[token],
    #     'u_ids': [user2[AuID]]
    # })
    # dm1 = dmResponse.json()
    # expected = {
    #     Name: 'user1, user2',
    #     'members': [{
    #         uID: user1[AuID], 
    #         fName: "User",
    #         lName: '1',
    #         'email': 'first@gmail.com',
    #         handle: 'user1',
    #     }, {
    #         uID: user2[AuID], 
    #         fName: "User",
    #         lName: '2',
    #         'email': 'second@gmail.com',
    #         handle: 'user2',
    #     }
    #     ]
    # }
    # assert requests.get(f"{config.url}dm/details/v1", params = {'token': user1[token], 'dm_id': dm1[dmID]}) == expected
    # assert requests.get(f"{config.url}dm/details/v1", params = {'token': user1[token], 'dm_id': dm1[dmID]}) == expected
    pass

def test_dm_details_invalid_dm_id(user1):
    # invalid_dmID = -2
    # response = requests.get(f"{config.url}dm/details/v1", params = {'token': user1[token], 'dm_id': invalid_dmID})
    # assert response.status_code == 400
    pass

def test_dm_details_not_in_dm(user1, user2, user3):
    dm1 = dm_create_v1(user1[token], [user2[AuID]])
    response = requests.get(f"{config.url}dm/details/v1", params = {'token': user3[token], 'dm_id': dm1[dmID]})
    assert response.status_code == 404

def test_dm_list():
    pass

def test_dm_create(user1, user2):
    # dmResponse = requests.post(f"{config.url}dm/create/v1", json={
    #     'token': user1[token],
    #     'u_ids': [user2[AuID]]
    # })

    # assert dmResponse.json() == {
    #     dmID: 0,
    #     'dm_name': 'user1, user2',
    # }


def test_dm_remove():
    pass

def test_dm_invite():
    pass

def test_dm_leave():
    pass

def test_dm_messages():
    pass