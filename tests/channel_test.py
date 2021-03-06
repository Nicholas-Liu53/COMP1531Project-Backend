# File to test functions in src/channel.py

import pytest
from src.channel import channel_invite_v1, channel_details_v1, channel_messages_v1, channel_leave_v1, channel_join_v1, channel_addowner_v1, channel_removeowner_v1
import src.auth, src.channels, src.other

AuID    = 'auth_user_id'
uID     = 'u_id'
cID     = 'channel_id'
chans   = 'channels'
allMems = 'all_members'
fName   = 'name_first'
lName   = 'name_last'

def test_channel_invite():
    pass

def test_channel_details():
    pass

def test_channel_messages():
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
    # print(firstChannel)
    channel_join_v1(userID3[AuID], firstChannel[cID])
    assert {uID: userID3[AuID], fName: 'T', lName: "C"} in channel_details_v1(userID3[AuID], firstChannel[cID])[allMems]

    #* Test 2: If userID4 unsuccessfully joins private channel 'BidenHarris'
    channel_join_v1(userID4[AuID], firstChannel[cID])
    assert {uID: userID4[AuID], fName: 'A', lName: "O"} not in channel_details_v1(userID4[AuID], secondChannel[cID])[allMems]

    #* Test 3: userID3 and userID4 aren't in channels they haven't joined 
    assert {uID: userID3[AuID], fName: 'T', lName: "C"} not in channel_details_v1(userID3[AuID], secondChannel[cID])[allMems]
    assert {uID: userID4[AuID], fName: 'A', lName: "O"} not in channel_details_v1(userID4[AuID], firstChannel[cID])[allMems]

    #* Finished testing for this function
    #! Clearing data
    src.other.clear_v1()

def test_channel_addowner():
    pass

def test_channel_removeowner():
    pass