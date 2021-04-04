import pytest
import requests
import src.other, src.auth
import json
from src import config
from src.config import url
from src.other import SECRET
import jwt


from src.channels import channels_create_v1
from src.message import message_send_v1

from src.dm import dm_create_v1


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
    
#* Fixture that returns invalid cID
@pytest.fixture
def invalid_cID():
    return -1
    
def test_http_channel_invite():
    pass
    
def test_http_channel_messages(user1, user2):
    #Create a private channel by user 1
    response = requests.post(f"{url}channels/create/v2", json={
        "token": user1[token],
        "name": "channel_1",
        "is_public": False,
    })
    
    channel1 = response.json()
    
    #Send one message in channel 
    requests.post(f"{url}message/send/v2", json={
        "token": user1[token],
        cID: channel1[cID],
        "message": "first message :)",
    })

    #Test for input errors
    #channel ID not a valid channel 
    invalid_channel = requests.get(f"{url}channel/messages/v2", json={
        "token": user1[token],
        cID: invalid_cID,
        'start' : 0,
    })
    
    #when start is greater than # of messages in channel
    invalid_start = requests.get(f"{url}channel/messages/v2", json={
        "token": user1[token],
        cID: channel1[cID],
        'start': 2,
    })
    
    assert invalid_channel.status_code == 400
    assert invalid_start.status_code == 400  

    #Access error when authorised user not a member of channel 
    access_error = requests.get(f"{url}channel/messages/v2", json={
        "token": user2[token],
        cID: channel1[cID],
        'start': 0,
    })
    assert access_error.status_code == 403 
    
    
    #Now can do success case 
    #Success Case 1: less than 50 messages returns end as -1
    
    #Send one message in channel  
    requests.post(f"{url}message/send/v2", json={
        "token": user1[token],
        cID: channel1[cID],
        "message" : "First message :)",
    })
        
    #Success case 1: Less than 50 messages returns end as -1 
    result = requests.get(f"{url}channel/messages/v2", json={
        "token": user1[token],
        cID: channel1[cID],
        'start': 0
    })
    
    responseUser1 = result.json()
    '''
    
    
    #FROM HERE NOT TOO SURE NEED TO CHECK 
    
    
    
    '''
    
    expected = {
        "len_messages": 1,
        "start" : 0,
        "end": -1,
    }
    
    assert len(responseUser1['messages']) == expected['len_messages']
    assert responseUser1['start'] == expected['start']
    assert responseUser1['end'] == expected['end']
    
    #Success case 2: More than 50 messages returns end as start + 50     
    #Send 50 messages into dm_0 
    message_counter = 1
    while message_counter < 51:
        requests.post(f"{url}message/send/v2", json={
            "token": user1[token],
            cID: channel1[cID],
            "message" : f"{message_counter}",
        })
        message_counter += 1
        
    result2 = requests.get(f"{url}channel/messages/v2", json={
        "token": user2[token],
        cID: channel1[cID],
        'start': 1
    })
    
    response_2 = result2.json()
        
    expected_2 = {
        "len_messages": 50,
        "start" : 1,
        "end": 51,
    }
    
    assert len(response_2['messages']) == expected_2['len_messages']
    assert response_2['start'] == expected_2['stsart']
    assert response_2['end'] == expected_2['end']
    
    
    
    
    
    
    


