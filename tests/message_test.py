import pytest
from src.message import message_send_v2, message_remove_v1, message_edit_v1, message_share_v1
from src.error import InputError, AccessError
import src.channel, src.channels, src.auth, src.dm, src.message

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

# AccessError when:
# the authorised user has not joined the channel or DM they are trying to share the message to

def test_message_share():
    #* Ensure database is empty
    #! Clearing data

    src.other.clear_v1()

    userID0 = src.auth.auth_register_v1("ownerDreams@gmail.com", "GodOwner123", "Owner", "Owner")
    userID1 = src.auth.auth_register_v1("testing4@gmail.com", "PasswordisKewl", "Jeffrey", "Meng")
    userID2 = src.auth.auth_register_v1("imthekewlest@gmail.com", "emfrigoslover123", "Meng", "Jeffrey")
    userID3 = src.auth.auth_register_v1("zodiac@gmail.com", "T3dCruz", "T", "C")
    userID4 = src.auth.auth_register_v1("gmailgmail@gmail.com", "hiiiiii12345", "M", "C")
    
    channelTest = src.channels.channels_create_v1(userID1[token], 'Channel', True)
    src.channel.channel_invite_v1(userID1[token], channelTest[cID], userID2[AuID])
    dmTest = src.dm.dm_create_v1(userID2[token],[userID4[AuID],userID3[AuID]])
    
    ogMessage = message_send_v2(userID1[token],channelTest[cID], "hello jeffrey meng") 

    sharedMessage = message_share_v1(userID2[token], ogMessage[mID],'', -1, dmTest[dmID])

    assert {
        mID: sharedMessage[mID],
        uID: userID2[AuID],
        'message': "hello jeffrey meng"
        
    } in



    