import pytest
import requests
import json
from src.config import url

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

def test_http_admin_user_remove_valid(user1, user2):

    chan = requests.post(f"{url}channels/create/v2", json={
        "token": user1[token],
        "name": "Channel",
        "is_public": True
    })
    channelTest = chan.json()

    requests.post(f"{url}channel/join/v2", json={
        "token": user2[token],
        "channel_id": channelTest[cID]
    })

    msg = requests.post(f"{url}message/send/v2", json={
        "token": user2[token],
        "channel_id": channelTest[cID],
        "message": 'Hello'
    })
    message = msg.json()

    #* User not an owner
    response_1 = requests.post(f"{url}admin/user/removing/v2", json={
        "token": user2[token],
        "u_id": user1[AuID]
    })    
    assert response_1.status_code == 403

    requests.post(f"{url}admin/user/removing/v2", json={
        "token": user1[token],
        "u_id": user2[AuID]
    })    

    msg_data = requests.get(f"{url}channel/messages/v2", params={
        "token": user1[token],
        "channel_id": channelTest[cID],
        "start": 0
    })
    message_data = msg_data.json()

    for dictionary in (message_data['messages']):
        if dictionary['message_id'] == message['message_id']:
            assert 'Removed User' in dictionary['message']

    users_data = requests.get(f"{url}users/all/v1", params={
        "token": user1[token]
    })
    users = users_data.json()

    assert users == {
            'users':
            [{
            'u_id': 0, 
            'email': "first@gmail.com", 
            'name_first': 'User', 
            'name_last': '1', 
            'handle_str': 'user1'
            },
            {
            'u_id': 1, 
            'email': "second@gmail.com", 
            'name_first': 'Removed', 
            'name_last': 'User', 
            'handle_str': 'user2'
            },]
    } 

    #* Test: u_id does not refer to a valid user
    response_2 = requests.post(f"{url}admin/user/removing/v2", json={
        "token": user1[token],
        "u_id": -1
    })    
    assert response_2.status_code == 400

    #* Test: the user is currently only owner    
    response_3 = requests.post(f"{url}admin/user/removing/v2", json={
        "token": user1[token],
        "u_id": user1[AuID]
    })    
    assert response_3.status_code == 400


