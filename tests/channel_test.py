# File to test functions in src/channel.py

import pytest
from src.channel import channel_invite_v1, channel_details_v1, channel_messages_v1, channel_leave_v1, channel_join_v1, channel_addowner_v1, channel_removeowner_v1
import src.auth, src.channels

from src.channels import channels_create_v1, channels_list_v1
from src.message import message_send_v1
from src.error import AccessError, InputError

def test_channel_invite():
    pass

def test_channel_details():
    pass


def test_channel_messages():

    #Setup user_id
    userID1 = src.auth.auth_register_v1("1531@gmail.com", "123", "Tom", "Zhang")
    userID2 = src.auth.auth_register_v1("comp@gmail.com", "456", "Jack", "P")
    

    #Create public channel by user_id 1
    firstChannel = channels_create_v1(1, 'Yggdrasil', True)
    
    #Send one message in channel 
    message_send_v1(1, "Yggdrasil", "First Message")
    
    with pytest.raises(InputError):
        #Test 1: returns input error when start is greater than total number of 
        # messages in channel
        channel_messages_v1(1, "Yggdrasil", 4)
        
        #Test 2: Raises input error when channel_id is invalid 
        channel_messages_v1(1, "fakeChannel", 0) 
        
    with pytest.raises(AccessError):
        #Test 3: returns access error when authorised user not a member of channel
        channel_messages_v1(2, "Yggdrasil", 0)

        
    #Test 4: if there are less than 50 messages, returns -1 in "end"
    assert channel_messages_v1(1, "Yggdrasil", 0) == -1
    
    #Test 5: if there are more than 50 messages, returns "start+50" as "end"
    #first need to write 50 messages in channel 
    counter = 0
    while counter < 51:
        message_send_v1(1, "Yggdrasil", "Spam :)")
        counter += 1  
    
    #Now there should be 52 messages in our channel (1 from start + 51 from while loop)
    assert channel_messages_v1(1, "Yggdrasil", 1) == 51

    pass

def test_channel_leave():
    pass

def test_channel_join():    
    pass

def test_channel_addowner():
    pass
 
def test_channel_removeowner():    
    pass
