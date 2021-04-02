# File to test functions in src/channel.py

import pytest
from src.channel import channel_invite_v1, channel_details_v1, channel_messages_v1, channel_leave_v1, channel_join_v1, channel_addowner_v1, channel_removeowner_v1
import src.auth, src.channels, src.other
from src.error import InputError, AccessError
from src.channels import channels_create_v1, channels_list_v2
from src.message import message_send_v1

AuID    = 'auth_user_id'
uID     = 'u_id'
cID     = 'channel_id'
chans   = 'channels'
allMems = 'all_members'
ownMems = 'owner_members'
fName   = 'name_first'
lName   = 'name_last'
token   = 'token'

@pytest.fixture
def invalid_token():
    return jwt.encode({'session_id': -1, 'user_id': -1}, SECRET, algorithm='HS256')

@pytest.fixture
def user1():
    src.other.clear_v1()    
    return src.auth.auth_register_v2("first@gmail.com", "password", "User", "1")

@pytest.fixture
def user2():
    return src.auth.auth_register_v2("second@gmail.com", "password", "User", "2")

@pytest.fixture
def user3():
    return src.auth.auth_register_v2("third@gmail.com", "password", "User", "3")

@pytest.fixture
def user4():
    return src.auth.auth_register_v2("fourth@gmail.com", "password", "User", "4")

@pytest.fixture
def user5():
    return src.auth.auth_register_v2("fifth@gmail.com", "password", "User", "5")

def test_channel_invite(user1,user2, user3):
 
    privateChannel = src.channels.channels_create_v1(user1[token], 'Coolkids', False)

    #* Test 1: Does user2 get successfully invited to channel "Coolkids"
    channel_invite_v1(user1[token], privateChannel[cID], user2[AuID])
    assert {
        fName: 'User', 
        lName: '2', 
        'email': "second@gmail.com", 
        'handle_string': "user2",
        uID: user2[AuID],
    } in channel_details_v1(user1[token], privateChannel[cID])[allMems]
    
    #* Test 2: is InputError raised when cID does not refer to valid channel
    with pytest.raises(InputError):
        channel_invite_v1(user1[token], "ThischannelIDdoesNotExist", user2[AuID])
    
    #* Test 3: is InputError raised when u_id isnt a valid user
    with pytest.raises(InputError):
        channel_invite_v1(user1[token], "ThischannelIDdoesNotExist", "DoesntExist")
    
    #* Test 4: is AccessError raised when auth_uID is not already a member of the channel
    with pytest.raises(AccessError):
        channel_invite_v1(user3[token], privateChannel[cID], user2[AuID])


def test_channel_details(user1, user2):

    realChannel = src.channels.channels_create_v1(user1[token], 'ChannelINFO', True)

    #* Test 1: Using the authorised user, does the channel details get presented for one user in channel
    
    assert channel_details_v1(user1[token], realChannel[cID]) == {
        'name': "ChannelINFO",
        'is_public': True, 
        'owner_members':[{
            'u_id': user1[AuID],
            'name_first': "User",
            'name_last': '1',
            'email': 'first@gmail.com',
            'handle_string': 'user1',
        }],
        'all_members':[{
            'u_id': user1[AuID], 
            'name_first': "User",
            'name_last': '1',
            'email': 'first@gmail.com',
            'handle_string': 'user1',
        }]
    }
    
    #* Test 2: Is InputError raised when Channel ID is not a valid channel
    with pytest.raises(InputError):
        channel_details_v1(user1[token], 'InvalidID')

    #* Test 3: Is AccessError raised when the user is not membber of channel with the channel id
    with pytest.raises(AccessError):
        channel_details_v1(user2[token], realChannel[cID])
    

def test_channel_messages():
    #* Ensure database is empty
    #! Clearing data
    src.other.clear_v1()
    #Setup user_id
    userID1 = src.auth.auth_register_v2("1531@gmail.com", "123456", "Tom", "Zhang")
    userID2 = src.auth.auth_register_v2("comp@gmail.com", "456789", "Jack", "P")
    

    #Create public channel by user_id 1
    firstChannel = channels_create_v1(userID1[token], 'Yggdrasil', True)
    
    #Send one message in channel 
    message_send_v1(userID1[token], firstChannel[cID], "First Message")

    with pytest.raises(InputError):
        #* Test 1: returns input error when start is greater than total number of 
        #* messages in channel
        channel_messages_v1(userID1[token], firstChannel[cID], 4)
        
        #* Test 2: Raises input error when channel_id is invalid 
        channel_messages_v1(userID1[token], -1, 0) 
        
    with pytest.raises(AccessError):
        #* Test 3: returns access error when authorised user not a member of channel
        channel_messages_v1(userID2[token], firstChannel[cID], 0)

        
    with pytest.raises(AccessError):
        #Test 3: returns access error when authorised user not a member of channel
        channel_messages_v1(userID2[token], firstChannel[cID], 0)

        
    #Test 4: if there are less than 50 messages, returns -1 in "end"
    assert channel_messages_v1(userID1[token], firstChannel[cID], 0)["end"] == -1
    
    #Test 5: if there are more than 50 messages, returns "start+50" as "end"
    #first need to write 50 messages in channel 
    counter = 0
    while counter < 51:
        message_send_v1(userID1[token], firstChannel[cID], "Spam :)")
        counter += 1  
    
    #Now there should be 52 messages in our channel (1 from start + 51 from while loop)
    assert channel_messages_v1(userID1[token], firstChannel[cID], 1)['end'] == 51
    assert channel_messages_v1(userID1[token], firstChannel[cID], 1)['start'] == 1
    assert len(channel_messages_v1(userID1[token], firstChannel[cID], 1)['messages']) == 50

def test_channel_leave():
    #* Ensure database is empty
    #! Clearing data
    src.other.clear_v1()

    #* Setup users and channels and create shorthand for strings for testing code
    userID1 = src.auth.auth_register_v2("ayelmao@gmail.com", "Bl00dO4th", "C", "L")
    userID2 = src.auth.auth_register_v2("lolrofl@gmail.com", "pr3ttynAme", "S", "S")
    userID3 = src.auth.auth_register_v2("zodiac@gmail.com", "T3dCruz", "T", "C")
    userID4 = src.auth.auth_register_v2("ocasio@gmail.com", "Alex4ndr1a", "A", "O")

    # userID1 made public channel 'TrumpPence'
    firstChannel = src.channels.channels_create_v1(userID1[token], 'TrumpPence', True)

    #* userID2, userID3 and userID4 join public channel 'TrumpPence'
    channel_join_v1(userID2[token], firstChannel[cID])
    channel_join_v1(userID3[token], firstChannel[cID])
    channel_join_v1(userID4[token], firstChannel[cID])

    #* Make sure they joined
    assert {
        uID: userID2[AuID],
        fName: 'S',
        lName: "S",
        'email': "lolrofl@gmail.com",
        'handle_string': "ss",
    } in channel_details_v1(userID2[token], firstChannel[cID])[allMems]
    assert {
        uID: userID3[AuID],
        fName: 'T',
        lName: "C",
        'email': "zodiac@gmail.com",
        'handle_string': "tc",
    } in channel_details_v1(userID3[token], firstChannel[cID])[allMems]
    assert {
        uID: userID4[AuID],
        fName: 'A',
        lName: "O",
        'email': "ocasio@gmail.com",
        'handle_string': "ao",
    } in channel_details_v1(userID4[token], firstChannel[cID])[allMems]

    #* One of them gets removed
    channel_leave_v1(userID3[token], firstChannel[cID])
    assert {
        uID: userID3[token],
        fName: 'T',
        lName: "C",
        'email': "zodiac@gmail.com",
        'handle_string': "tc",
    } not in channel_details_v1(userID1[token], firstChannel[cID])[allMems]

    #* Another gets removed 
    channel_leave_v1(userID4[token], firstChannel[cID])
    assert {
        uID: userID4[token],
        fName: 'A',
        lName: "O",
        'email': "ocasio@gmail.com",
        'handle_string': "ao",
    } not in channel_details_v1(userID1[token], firstChannel[cID])[allMems]

    #* Finished testing for this function
    #! Clearing data
    src.other.clear_v1()


def test_channel_join():
    #* Ensure database is empty
    #! Clearing data
    src.other.clear_v1()

    #* Setup users and channels and create shorthand for strings for testing code
    userID1 = src.auth.auth_register_v2("ayelmao@gmail.com", "Bl00dO4th", "C", "L")
    userID2 = src.auth.auth_register_v2("lolrofl@gmail.com", "pr3ttynAme", "S", "S")
    userID3 = src.auth.auth_register_v2("zodiac@gmail.com", "T3dCruz", "T", "C")
    userID4 = src.auth.auth_register_v2("ocasio@gmail.com", "Alex4ndr1a", "A", "O")

    # userID1 made public channel 'TrumpPence'
    firstChannel = src.channels.channels_create_v1(userID1[token], 'TrumpPence', True)
    # userID2 made private channel 'BidenHarris'
    secondChannel = src.channels.channels_create_v1(userID2[token], 'BidenHarris', False)

    #* Test 1: If userID3 successfully joins public channel 'TrumpPence'
    channel_join_v1(userID3[token], firstChannel[cID])
    assert {
        uID: userID3[AuID],
        'email': "zodiac@gmail.com",
        fName: "T",
        lName: "C",
        'handle_string': 'tc'
    } in channel_details_v1(userID3[token], firstChannel[cID])[allMems]

    #* Test 2: If userID4 unsuccessfully joins private channel 'BidenHarris'
    with pytest.raises(AccessError): 
        # Check if AccessError is raised when trying to join a private channel
        channel_join_v1(userID4[token], secondChannel[cID])

    #* Test 3: userID3 and userID4 aren't in channels they haven't joined 
    with pytest.raises(AccessError):
        channel_details_v1(userID3[token], secondChannel[cID])[allMems]
        channel_details_v1(userID4[token], firstChannel[cID])[allMems]

    #* Test 4: Check if InputError is raised when channel does not exist
    #! Clearing data
    src.other.clear_v1()                                    # Channel is deleted
    with pytest.raises(InputError):                         
        channel_join_v1(userID1[token], firstChannel[cID])   # userID1 tries to join the non-existent channel

    #* Test 4: Check if InputError is raised when channel does not exist
    #! Clearing data
    src.other.clear_v1()                                    # Channel is deleted
    with pytest.raises(InputError):                         
        channel_join_v1(userID1[token], firstChannel[cID])   # userID1 tries to join the non-existent channel

    #* Finished testing for this function
    #! Clearing data
    #   src.other.clear_v1()

def test_channel_addowner(user1, user2,user3,user4, user5):

    channelTest = src.channels.channels_create_v1(user2[token], 'Channel', False)

    # Test 1: Testing for whether added user now appears in both owner list and all members list of private chan
    channel_addowner_v1(user2[token], channelTest[cID], user3[AuID])
    assert {
        uID: user3[AuID],        
        fName: 'User',
        lName: '3',
        'email': 'third@gmail.com',
        'handle_string': 'user3',
    } in channel_details_v1(user2[token], channelTest[cID])[ownMems]
    assert {
        uID: user3[AuID],
        fName: 'User',
        lName: '3',
        'email': 'third@gmail.com',
        'handle_string': 'user3',
    } in channel_details_v1(user2[token], channelTest[cID])[allMems]

    channelTest2 = src.channels.channels_create_v1(user1[token], 'Channel2', True)

    # Test 2: Testing for whether added user now appears in both owner list and all members list of public chan
    channel_addowner_v1(user1[token], channelTest2[cID], user3[AuID])
    assert {
        uID: user3[AuID],
        fName: 'User',
        lName: '3',
        'email': 'third@gmail.com',
        'handle_string': 'user3',
    } in channel_details_v1(user3[token], channelTest2[cID])[ownMems]
    assert {
        uID: user3[AuID],
        fName: 'User',
        lName: '3',
        'email': 'third@gmail.com',
        'handle_string': 'user3',
    } in channel_details_v1(user3[token], channelTest2[cID])[allMems]

    # Test 3: for invalid channel, raising input error
    with pytest.raises(InputError): 
        channel_addowner_v1(user2[token], 999, user4[AuID])
    
    # Test 4: for user already in owner list
    with pytest.raises(InputError):
        channel_addowner_v1(user2[token], channelTest[cID], user3[AuID])

    # Test 5: User with no permission to add owner
    with pytest.raises(AccessError):
        channel_addowner_v1(user4[token], channelTest[cID], user5[AuID])
    
        

def test_channel_removeowner(user1, user2, user3, user4):

    channelTest = src.channels.channels_create_v1(user2[token], 'Channel', True)

    # Test 1: adding a owner into channel and testing if they are successfully removed
    channel_addowner_v1(user2[token], channelTest[cID], user3[AuID])

    channel_removeowner_v1(user3[token], channelTest[cID], user2[AuID])
    # check to see if user2 has been removed from owners, but remains in all members
    assert {
        uID: user3[AuID],
        fName: 'User',
        lName: '3',
        'email': 'third@gmail.com',
        'handle_string': 'user3',
    } in channel_details_v1(user2[token], channelTest[cID])[ownMems]
    assert {
        uID: user3[AuID],
        fName: 'User',
        lName: '3',
        'email': 'third@gmail.com',
        'handle_string': 'user3',
    } in channel_details_v1(user2[token], channelTest[cID])[allMems]
    assert{
        uID: user2[AuID],
        fName: 'User',
        lName: '2',
        'email': 'second@gmail.com',
        'handle_string': 'user2',
    } in channel_details_v1(user2[token], channelTest[cID])[allMems]

    # Test 2: with an invalid Channel ID, tests for Input Error being raised
    with pytest.raises(InputError):
        channel_removeowner_v1(user3[token], 9999, user2[AuID])

    # Test 3: Raise Input error successful for user not in the owner members
    with pytest.raises(InputError):
        channel_removeowner_v1(user3[token], channelTest[cID], user4[AuID])
    
    # Test 4: With only one member in owner left, does not remove them, raising input error
    with pytest.raises(InputError):
        channel_removeowner_v1(user1[token], channelTest[cID], user2[AuID])

    # Test 5: Non-owner trying to remove, raising access Error
    with pytest.raises(AccessError):
        channel_removeowner_v1(user4[token], channelTest[cID], user3[AuID])
    


