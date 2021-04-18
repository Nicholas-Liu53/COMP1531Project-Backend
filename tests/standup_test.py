#File to test functions in src/standup.py
import pytest
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1
from src.error import InputError, AccessError
from src.other import SECRET, clear_v1
import src.channel
from src.channel import channel_messages_v1
import jwt
import time
from datetime import datetime 

AuID     = 'auth_user_id'
uID      = 'u_id'
cID      = 'channel_id'
chans    = 'channels'
token    = 'token'

@pytest.fixture
def invalid_token():
    return jwt.encode({'session_id': -1, 'user_id': -1}, SECRET, algorithm='HS256')

@pytest.fixture
def user1():
    clear_v1()    
    return src.auth.auth_register_v2("first@gmail.com", "password", "User", "1")

@pytest.fixture
def user2():
    return src.auth.auth_register_v2("second@gmail.com", "password", "User", "2")

@pytest.fixture
def user3():
    return src.auth.auth_register_v2("third@gmail.com", "password", "User", "3")
    

#Test that a standup can be started in a valid channel 
def test_standup_start_v1(user1, user2, user3):
    invalid_cID = -1 
    #Input Error when Channel ID not a valid channel 
    with pytest.raises(InputError):
        standup_start_v1(user1[token], invalid_cID, 1.0)
    
    #Input Error when Standup is already running in channel 
    channel = src.channels.channels_create_v1(user1[token], 'Marms', False)
    src.channel.channel_invite_v1(user1[token], channel[cID], user2[AuID])
        
    result = standup_start_v1(user1[token], channel[cID], 1.0)
    with pytest.raises(InputError):
        standup_start_v1(user1[token], channel[cID], 1.0)
    
    #Access error when authorised user is not in channel 
    with pytest.raises(AccessError):
        standup_start_v1(user3[token], channel[cID], 1.0)
    
    #Success case 
    #Assert that time_finish is correct
    now = datetime.now()
    time_finish = int(now.strftime("%s")) + 1
    assert result['time_finish'] == time_finish

#Test whether there is a standup active in a channel currently 
def test_standup_active_v1(user1, user2):
    #Input Error when Channel ID not a valid channel 
    invalid_cID = -1 
    with pytest.raises(InputError):
        standup_active_v1(user1[token], invalid_cID)
    
    #Input Error when Standup is already running in channel 
    channel = src.channels.channels_create_v1(user1[token], 'Marms', False)
    src.channel.channel_invite_v1(user1[token], channel[cID], user2[AuID])
    standup_start_v1(user1[token], channel[cID], 1.0)
    
    #Success Case 
    result = standup_active_v1(user1[token], channel[cID])
    #Same as before? - standup is active in channel dictionary 
    assert result['is_active'] 
    
    #Can also check that once standup is done: is no longer active 
    time.sleep(1.0)
    result1 = standup_active_v1(user1[token], channel[cID])
    assert not result1['is_active'] 
       
#Test that messages can be successfully sent in the standup queue 
def test_standup_send_v1(user1, user2, user3):
    #Input error when Channel ID not a valid channel 
    invalid_cID = -1 
    with pytest.raises(InputError):
        standup_send_v1(user1[token], invalid_cID, 1.0)
    
    channel = src.channels.channels_create_v1(user1[token], 'Marms', False)
    src.channel.channel_invite_v1(user1[token], channel[cID], user2[AuID])
        
    #Message is more than 1000 characters (not including username and colon)
    message = '?' * 1001
    with pytest.raises(InputError):
        standup_send_v1(user1[token], channel[cID], message)
        
    #Input error when standup is not active in channel 
    with pytest.raises(InputError):
        standup_send_v1(user1[token], channel[cID], "Hello")
    
    
    #Access error when authorised user not a member of channel the message is within 
    with pytest.raises(AccessError):
        standup_send_v1(user3[token], channel[cID], "Hello")
    
    #Success case 
    standup_start_v1(user1[token], channel[cID], 1.0)
    standup_send_v1(user1[token], channel[cID], "Hello")
        
    #Assert that correct message appears in channel_messages after standup 
    time.sleep(1.0)
    result = channel_messages_v1(user1[token], channel[cID], 0)
    assert len(result['messages']) == 1
    for messages in result['messages']: 
        assert "user1: Hello" in messages['message']
    
    #Now do for two messages, assert that the 2 messages are appended as one message 
    channel2 = src.channels.channels_create_v1(user1[token], 'Yggdrasil', False)
    src.channel.channel_invite_v1(user1[token], channel2[cID], user2[AuID])
    standup_start_v1(user1[token], channel2[cID], 1.0)
    standup_send_v1(user1[token], channel2[cID], "Hello")
    standup_send_v1(user2[token], channel2[cID], "Goodbye")
    time.sleep(1.0)
    result2 = channel_messages_v1(user1[token], channel2[cID], 0)

    assert len(result2['messages']) == 1
    for messages in result2['messages']: 
        assert "user1: Hello\nuser2: Goodbye" in messages['message'] 
    

