# File to test functions in src/channel.py

import pytest
from src.channel import channel_invite_v1, channel_details_v1, channel_messages_v1, channel_leave_v1, channel_join_v1, channel_addowner_v1, channel_removeowner_v1
import src.auth, src.channels, src.other
from src.error import InputError, AccessError

AuID    = 'auth_user_id'
uID     = 'user_id'
cID     = 'channel_id'
chans   = 'channels'
allMems = 'all_members'
fName   = 'name_first'
lName   = 'name_last'

from src.channels import channels_create_v1, channels_list_v1
from src.message import message_send_v1
from src.error import AccessError, InputError

def test_channel_invite():
    #* Ensure database is empty
    #! Clearing data
    src.other.clear_v1()

    #* Create user and channel for user to be invited
    #* Users
    userID1 = src.auth.auth_register_v1("testing1@gmail.com", "Monkey", "Vincent", "Le")
    userID2 = src.auth.auth_register_v1("testing2@gmail.com", "jonkey", "Darius", "Kuan")
    #* Channel create
    privateChannel = src.channels.channels_create_v1(userID1[AuID], 'Coolkids', False)

    #* Test 1: Does userID2 get successfully invited to channel "Coolkids"
    channel_invite_v1(userID1[AuID], privateChannel[cID], userID2[AuID])
    assert {
        uID: userID2[AuID], 
        fName: 'Darius', 
        lName: 'Kuan', 
        'email': "testing2@gmail.com", 
        'handle_string': "dariuskuan"
    } in channel_details_v1(userID1[AuID], privateChannel[cID])[allMems]
    
    #* Test 2: is InputError raised when cID does not refer to valid channel
    with pytest.raises(InputError) as e:
        channel_invite_v1(userID1[AuID], "ThischannelIDdoesNotExist", userID2[AuID])
    
    #* Test 3: is InputError raised when u_id isnt a valid user
    with pytest.raises(InputError) as e:
        channel_invite_v1(userID1[AuID], "ThischannelIDdoesNotExist", "DoesntExist")
    
    #* Test 4: is AccessError raised when auth_uID is not already a member of the channel
    userID3 = src.auth.auth_register_v1("imposter@gmail.com", "g2g2gkden", "Among", "Us")
    with pytest.raises(AccessError) as e:
        channel_invite_v1(userID3[AuID], privateChannel[cID], userID2[AuID])

    #* Finished testing for this function
    #! Clearing data
    src.other.clear_v1()


def test_channel_details():
    #* Ensure database is empty
    #! Clearing data
    src.other.clear_v1()
    
    # Creating users and channels
    userID1 = src.auth.auth_register_v1("testing4@gmail.com", "Monkey1", "Vincentd", "Lee")
    userID2 = src.auth.auth_register_v1("testing3@gmail.com", "jonkey1", "Imposterd", "Kuand")
    realChannel = src.channels.channels_create_v1(userID1[AuID], 'ChannelINFO', True)

    #* Test 1: Using the authorised user, does the channel details get presented for one user in channel
    
    assert channel_details_v1(userID1[AuID], realChannel[cID]) == {
        'channel_name': "ChannelINFO", 
        'owner_members':[{
            'user_id': userID1[AuID], 
            'name_first': "Vincentd",
            'name_last': 'Lee',
            'email': 'testing4@gmail.com',
            'handle_string': 'vincentdlee',
        }],
        'all_members':[{
            'user_id': userID1[AuID], 
            'name_first': "Vincentd",
            'name_last': 'Lee',
            'email': 'testing4@gmail.com',
            'handle_string': 'vincentdlee',
        }]
    }
    
    #* Test 2: Is InputError raised when Channel ID is not a valid channel
    with pytest.raises(InputError) as e:
        channel_details_v1(userID1[AuID], 'InvalidID')

    #* Test 3: Is AccessError raised when the user is not membber of channel with the channel id
    with pytest.raises(AccessError) as e:
        channel_details_v1(userID2[AuID], realChannel[cID])
    
    #* Finished testing for this function
    #! Clearing data
    src.other.clear_v1()


def test_channel_messages():

    #Setup user_id
    userID1 = src.auth.auth_register_v1("1531@gmail.com", "123456", "Tom", "Zhang")
    userID2 = src.auth.auth_register_v1("comp@gmail.com", "456789", "Jack", "P")
    

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
    #* Ensure database is empty
    #! Clearing data
    src.other.clear_v1()

    #* Setup users and channels and create shorthand for strings for testing code
    userID1 = src.auth.auth_register_v1("ayelmao@gmail.com", "Bl00dO4th", "C", "L")
    userID2 = src.auth.auth_register_v1("lolrofl@gmail.com", "pr3ttynAme", "S", "S")
    userID3 = src.auth.auth_register_v1("zodiac@gmail.com", "T3dCruz", "T", "C")
    userID4 = src.auth.auth_register_v1("ocasio@gmail.com", "Alex4ndr1a", "A", "O")

    # userID1 made public channel 'TrumpPence'
    firstChannel = src.channels.channels_create_v1(userID1[AuID], 'TrumpPence', True)
    # userID2 made private channel 'BidenHarris'
    secondChannel = src.channels.channels_create_v1(userID2[AuID], 'BidenHarris', False)

    #* Test 1: If userID3 successfully joins public channel 'TrumpPence'
    channel_join_v1(userID3[AuID], firstChannel[cID])
    assert {
        uID: userID3[AuID],
        fName: 'T',
        lName: "C",
        'email': "zodiac@gmail.com",
        'handle_string': "tc",
    } in channel_details_v1(userID3[AuID], firstChannel[cID])[allMems]

    #* Test 2: If userID4 unsuccessfully joins private channel 'BidenHarris'
    with pytest.raises(AccessError): 
        # Check if AccessError is raised when trying to join a private channel
        channel_join_v1(userID4[AuID], secondChannel[cID])

    #* Test 3: userID3 and userID4 aren't in channels they haven't joined 
    with pytest.raises(AccessError):
        channel_details_v1(userID3[AuID], secondChannel[cID])[allMems]
        channel_details_v1(userID4[AuID], firstChannel[cID])[allMems]

    #* Test 4: Check if InputError is raised when channel does not exist
    #! Clearing data
    src.other.clear_v1()                                    # Channel is deleted
    with pytest.raises(InputError):                         
        channel_join_v1(userID1[AuID], firstChannel[cID])   # userID1 tries to join the non-existent channel

    #* Test 4: Check if InputError is raised when channel does not exist
    #! Clearing data
    src.other.clear_v1()                                    # Channel is deleted
    with pytest.raises(InputError):                         
        channel_join_v1(userID1[AuID], firstChannel[cID])   # userID1 tries to join the non-existent channel

    #* Finished testing for this function
    #! Clearing data
    src.other.clear_v1()

def test_channel_addowner():
    pass
 
def test_channel_removeowner():    
    pass
