# File to test functions in src/channels.py

import pytest
from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
import src.auth, src.channel

def test_channels_list():
    pass

def test_channels_listall():
    pass

def test_channels_create():
    #? Setup users and create shorthand for strings for testing code
    userID1 = auth.auth_register_v1("ayelmao@gmail.com", "Bl00dO4th", "C", "L")
    userID2 = auth.auth_register_v1("lolrofl@gmail.com", "pr3ttynAme", "S", "S")
    
    uID   = 'auth_user_id'
    cID   = 'channel_id'
    chans = 'channels'

    # Test 1: Newly created public channel by userID1 appears in both of his channel list
    firstChannel = channels_create_v1(userID1[uID], 'Oogway', True)
    assert {cID: firstChannel, 'name': 'Oogway'} is in channels_list_v1(userID1[uID])[chans]
    assert {cID: firstChannel, 'name': 'Oogway'} is in channels_listall_v1(userID1[uID])[chans]

    # Test 2: Make sure this channel doesn't appear in userID2's channel list, but does in listall
    assert {cID: firstChannel, 'name': 'Oogway'} is not in channels_list_v1(userID2[uID])[chans]
    assert {cID: firstChannel, 'name': 'Oogway'} is in channels_listall_v1(userID2[uID])[chans]

    # Test 3: Newly created private channel by userID2 appears in his channel list
    secondChannel = channels_create_v1(userID2[uID], 'Yayot', False)
    assert {cID: secondChannel, 'name': 'Yayot'} is in channels_list_v1(userID2[uID])[chans]
    assert {cID: secondChannel, 'name': 'Yayot'} is in channels_listall_v1(userID2[uID])[chans]

    # Test 4: Make sure this channel doesn't appear in either of userID1's channel lists
    assert {cID: secondChannel, 'name': 'Yayot'} is not in channels_list_v1(userID1[uID])[chans]
    assert {cID: secondChannel, 'name': 'Yayot'} is not in channels_listall_v1(userID1[uID])[chans]