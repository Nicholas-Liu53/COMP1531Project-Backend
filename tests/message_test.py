# file to test functions in src/message.py

import pytest
from src.message import message_send_v2, message_remove_v1, message_edit_v1, message_share_v1, message_senddm_v1
from src.error import InputError, AccessError
import src.channel, src.channels, src.auth, src.dm, src.message, src.other
from datetime import timezone, datetime


AuID    = 'auth_user_id'
uID     = 'u_id'
cID     = 'channel_id'
chans   = 'channels'
allMems = 'all_members'
ownMems = 'owner_members'
fName   = 'name_first'
lName   = 'name_last'
token = 'token'
mID = 'message_id'
dmID = 'dm_id'
# message_send_v1
# When message is >1000 characters, InputError is raised
# When authorised user is not part of the channel that they are trying to post in, AccessError is raised
# After the function is sucessfully run, ensure that the return value is correct

# message_edit_v1
# When message is >1000 characters, InputError is raised
# If there are no messages with matching message_id, InputError is raised
# Ownership permission tests:
    # Owner of Dreams should be able to edit anything
    # Owner of channels should be able to edit anything in channels they own
    # Non-owner of channels should only be able to edit their own messages
# Test if a message has been edited successfully?

# search_v1
# When query_str is >1000 characters, InputError is raised
# Test that users can only see messages in channels that they have joined
    # Test if a user who has joined no channels can see any messages



def test_message_share_todm():
    #* Ensure database is empty
    #! Clearing data

    src.other.clear_v1()

    userID1 = src.auth.auth_register_v1("testing4@gmail.com", "PasswordisKewl", "Jeffrey", "Meng")
    userID2 = src.auth.auth_register_v1("imthekewlest@gmail.com", "emfrigoslover123", "Meng", "Jeffrey")
    userID3 = src.auth.auth_register_v1("zodiac@gmail.com", "T3dCruz", "T", "C")
    userID4 = src.auth.auth_register_v1("gmailgmail@gmail.com", "hiiiiii12345", "M", "C")
    
    channelTest = src.channels.channels_create_v1(userID1[token], 'Channel', True)
    src.channel.channel_invite_v1(userID1[token], channelTest[cID], userID2[AuID])
    dmTest = src.dm.dm_create_v1(userID2[token],[userID4[AuID],userID3[AuID]])
    
    ogMessage = message_send_v2(userID1[token],channelTest[cID], "hello jeffrey meng") 

    sharedMessage, now = message_share_v1(userID2[token], ogMessage[mID],'', -1, dmTest[dmID]), datetime.now()

    timestamp = now.replace(tzinfo=timezone.utc).timestamp()

    assert {
        mID: sharedMessage[mID],
        uID: userID2[AuID],
        'message': "hello jeffrey meng",
        'time_created': timestamp,
    } in src.dm.dm_messages_v1(userID2[token],dmTest[dmID],0)['messages']

    # userID1 is not in dmTest, raise access error
    with pytest.raises(AccessError):
        message_share_v1(userID1[token], ogMessage[mID], '', -1, dmTest[dmID])



def test_message_share_tochannel():
    #* Ensure database is empty
    #! Clearing data

    src.other.clear_v1()

    userID0 = src.auth.auth_register_v1("ownerDreams@gmail.com", "GodOwner123", "Owner", "Owner")
    userID1 = src.auth.auth_register_v1("imthekewlest@gmail.com", "emfrigoslover123", "Meng", "Jeffrey")
    userID2 = src.auth.auth_register_v1("zodiac@gmail.com", "T3dCruz", "T", "C")

    channelTest = src.channels.channels_create_v1(userID0[token], 'Channel', True)
    channelTest2 = src.channels.channels_create_v1(userID1[token], 'Channel', True)

    src.channel.channel_invite_v1(userID1[token], channelTest2[cID], userID0[AuID])
    src.channel.channel_invite_v1(userID0[token], channelTest[cID], userID2[AuID])

    ogMessage = message_send_v2(userID0[token],channelTest[cID], "hello jeffrey meng") 

    sharedMessage, now = message_share_v1(userID0[token], ogMessage[mID],'vincent', channelTest2[cID], -1), datetime.now()

    timestamp = now.replace(tzinfo=timezone.utc).timestamp()

    assert {
        mID: sharedMessage[mID],
        uID: userID0[AuID],
        'message': "hello jeffrey meng | vincent",
        'time_created': timestamp,
    } in src.channel.channel_messages_v1(userID1[token],channelTest2[cID],0)['messages']

    with pytest.raises(AccessError):
        message_share_v1(userID2[token], ogMessage[mID], '', channelTest2[cID], -1)

def test_message_share_dmtodm():
    
    #* Ensure database is empty
    #! Clearing data

    src.other.clear_v1()

    userID1 = src.auth.auth_register_v1("testing4@gmail.com", "PasswordisKewl", "Jeffrey", "Meng")
    userID2 = src.auth.auth_register_v1("imthekewlest@gmail.com", "emfrigoslover123", "Meng", "Jeffrey")
    userID3 = src.auth.auth_register_v1("zodiac@gmail.com", "T3dCruz", "T", "C")
    userID4 = src.auth.auth_register_v1("gmailgmail@gmail.com", "hiiiiii12345", "M", "C")
    
    dmTest = src.dm.dm_create_v1(userID2[token],[userID4[AuID],userID3[AuID]])
    dmTest2 = src.dm.dm_create_v1(userID1[token],[userID2[AuID]])

    ogMessage = message_senddm_v1(userID1[token], dmTest2[dmID], 'hello meng')

    sharedMessage, now = message_share_v1(userID2[token], ogMessage[mID],'wow', -1, dmTest[dmID]), datetime.now()

    timestamp = now.replace(tzinfo=timezone.utc).timestamp()

    assert {
        mID: sharedMessage[mID],
        uID: userID2[AuID],
        'message': "hello jeffrey meng | wow",
        'time_created': timestamp,
    } in src.dm.dm_messages_v1(userID4[token],dmTest[dmID],0)['messages']

    with pytest.raises(AccessError):
        message_share_v1(userID1[token], ogMessage[mID], '', -1, dmTest[dmID])






    