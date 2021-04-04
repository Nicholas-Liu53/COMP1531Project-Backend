import pytest
import requests
import json
from src.config import url
from src.error import AccessError, InputError
from src.admin import user_remove_v1, userpermission_change_v1
from src.other import clear_v1
from jwt import encode

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

    channelTest = src.channels.channels_create_v1(user1[token], 'Channel', True)
    src.channel.channel_join_v1(user2[token], channelTest[cID])
    message = src.message.message_send_v1(user2[token], channelTest[cID], 'Hello')

    #* User not an owner
    with pytest.raises(AccessError): 
        user_remove_v1(user2[token], user1[AuID])
    
    user_remove_v1(user1[token], user2[AuID])
    for dictionary in (src.channel.channel_messages_v1(user1[token], channelTest[cID], 0)['messages']):
        if dictionary['message_id'] == message['message_id']:
            assert 'Removed User' in dictionary['message']

    users = src.user.users_all(user1[token])
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
    with pytest.raises(InputError):
        user_remove_v1(user1[token], -1)

    #* Test: the user is currently only owner
    with pytest.raises(InputError): 
        user_remove_v1(user1[token], user1[AuID])

