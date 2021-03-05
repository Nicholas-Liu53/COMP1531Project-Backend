# File to test functions in src/channels.py

import pytest
from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
from src.error import AccessError, InputError
import src.auth, src.channel, src.other

AuID    = 'auth_user_id'
uID     = 'user_id'
cID     = 'channel_id'
allMems = 'all_members'
cName   = 'channel_name'
fName   = 'name_first'
lName   = 'name_last'

def test_channels_list():
    # Test 1: When calling the function with an invalid auth_user_id should raise an AccessError
    src.other.clear_v1()
    with pytest.raises(AccessError):
        channels_list_v1("wrongid")

    # Setup users and create shorthand for strings for testing code
    userID1 = src.auth.auth_register_v1("first@gmail.com", "password", "D", "C")


    # Test 2: When calling the function with a valid auth_user_id, only the channels that user has joined should appear
    firstChannel = channels_create_v1(userID1[AuID], 'Marmclearot', True)
    assert channels_list_v1(userID1[AuID]) == {'channels': []}
    src.channel.channel_join_v1(userID1[AuID], firstChannel[cID])
    assert channels_list_v1(userID1[AuID]) == {'channels': [{cID: firstChannel[cID], cName: 'Marmot'}]}

def test_channels_listall():
    # Test 1: When calling the function with an invalid auth_user_id should raise an AccessError
    src.other.clear_v1()
    with pytest.raises(AccessError):
        channels_listall_v1("noonehasthis")

    # Setup users and create shorthand for strings for testing code
    userID1 = src.auth.auth_register_v1("first@gmail.com", "password", "D", "C")
    userID2 = src.auth.auth_register_v1("second@gmail.com", "password", "L", "M")

    # Test 2: When calling the function with a valid auth_user_id, both private and public channels are displayed even if the user is not a member
    firstChannel = channels_create_v1(userID1[AuID], 'JS', True)
    secondChannel = channels_create_v1(userID1[AuID], 'NEZ', False)
    assert channels_listall_v1(userID1[AuID]) == {'channels': [{cID: firstChannel[cID], cName: 'JS'}, {cID: secondChannel[cID], cName: 'NEZ'}]}

    # Test 3: When adding users to channels, this should not affect the output of the program
    src.channel.channel_join_v1(userID1[AuID], firstChannel[cID])
    assert channels_listall_v1(userID1[AuID]) == {'channels': [{cID: firstChannel[cID], cName: 'JS'},{cID: secondChannel[cID], cName: 'NEZ'}]}

    # Test 4: When running the function for two different valid auth_user_ids, the return should be the same
    assert channels_listall_v1(userID1[AuID]) == channels_listall_v1(userID2[AuID])

def test_channels_create():
    # # Test 1: Newly created public channel by user_id 1 appears in his channel list
    # firstChannel = channels_create_v1(1, 'Oogway', True)
    # assert {'channel_id': result, 'name': 'Oogway'} in channels_list_v1(1)['channels']

    # # Test 2: 

    # secondChannel = channels_create_v1(2, 'Yayot', False)
    # assert {''}
    pass 