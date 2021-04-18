#File to test functions in src/standup.py
import pytest
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1
from src.error import InputError, AccessError
from src.other import SECRET, clear_v1
import src.channel
import jwt

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
    
    '''
    NOT TOO SURE ABOUT LENGTH AND THREADING HOW IT WORKS
    DO I NEED TO DO LIKE TIMER.START() thing in MAIN 
    '''
    
    standup_start_v1(user1[token], channel[cID], 1.0)
    with pytest.raises(InputError):
        standup_start_v1(user1[token], channel[cID], 1.0)
    
    #Access error when authorised user is not in channel 
    with pytest.raises(AccessError):
        standup_start_v1(user3[token], channel[cID], 1.0)
    
    #Success case 
    #Check that standup is active in channel dictionary? 

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
    standup_active_v1(user1[token], channel[cID])
    #Same as before? - standup is active in channel dictionary 
    #Can also check that is done
   
#Test that messages can be successfully sent in the standup queue 
def test_standup_send_v1(user1, user2, user3):
    #Input error when Channel ID not a valid channel 
    invalid_cID = -1 
    with pytest.raises(InputError):
        standup_send_v1(user1[token], invalid_cID, 1.0)
    
    channel = src.channels.channels_create_v1(user1[token], 'Marms', False)
    src.channel.channel_invite_v1(user1[token], channel[cID], user2[AuID])
        
    #Message is more than 1000 characters (not including username and colon)
    message = ''
    
    '''
    DO I NEED TO START STANDUP HERE?
    '''
    for _ in range(1500):
        message += '?'
    with pytest.raises(InputError):
        standup_send_v1(user1[token], channel[cID], message)
        
    #Input error when standup is not active in channel 
    with pytest.raises(InputError):
        standup_send_v1(user1[token], channel[cID], "Hello")
    
    
    #Access error when authorised user not a member of channel the message is within 
    with pytest.raises(AccessError):
        standup_send_v1(user3[token], channel[cID], "Hello")
    
    #Success case 
    #Similar to message send, can check that message is in a message log within standups data?
    #Assert len of messages log is only plussed one

