# file to test functions in src/message.py
import pytest
from src.message import message_send_v1, message_remove_v1, message_edit_v1, message_share_v1, message_senddm_v1
from src.error import InputError, AccessError
import src.channel, src.channels, src.auth
from src.other import clear_v1, SECRET
from datetime import timezone, datetime
import jwt

AuID    = 'auth_user_id'
uID     = 'u_id'
cID     = 'channel_id'
chans   = 'channels'
allMems = 'all_members'
ownMems = 'owner_members'
fName   = 'name_first'
lName   = 'name_last'
token   = 'token'
mID     = 'message_id'
dmID    = 'dm_id'
Name    = 'name'

# message_send_v1
# When message is >1000 characters, InputError is raised
# When authorised user is not part of the channel that they are trying to post in, AccessError is raised
# After the function is sucessfully run, ensure that the return value is correct
def test_message_send():
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

    #* userID2 and userID3 join public channel 'TrumpPence'
    src.channel.channel_join_v1(userID2[token], firstChannel[cID])
    src.channel.channel_join_v1(userID3[token], firstChannel[cID])

    #* Test if a super large message raises an InputError
    message = ''
    for _ in range(1500):
        message += '?'
    with pytest.raises(InputError):
        message_send_v1(userID1[token], firstChannel[cID], message)

    #* Test if a user not in the channel tries to send a message into the channel
    with pytest.raises(AccessError):
        message_send_v1(userID4[token], firstChannel[cID], '?')

    #* Test a message is successfully sent 
    sendOutput = message_send_v1(userID1[token], firstChannel[cID], "Hi")
    messageFound = False
    for messageDict in src.channel.channel_messages_v1(userID1[token], firstChannel[cID], 0)['messages']:
        if sendOutput['message_id'] == messageDict['message_id']:
            messageFound = True
            break
    assert messageFound is True 

    #* Test another messsage is successfully sent
    sendOutput = message_send_v1(userID3[token], firstChannel[cID], "Sup")
    messageFound = False
    for messageDict in src.channel.channel_messages_v1(userID1[token], firstChannel[cID], 0)['messages']:
        if sendOutput['message_id'] == messageDict['message_id']:
            messageFound = True
            break
    assert messageFound is True 

    #! Clearing data
    src.other.clear_v1()

# message_edit_v1
# When message is >1000 characters, InputError is raised
# If there are no messages with matching message_id, InputError is raised
# Ownership permission tests:
    # Owner of Dreams should be able to edit anything
    # Owner of channels should be able to edit anything in channels they own
    # Non-owner of channels should only be able to edit their own messages
# Test if a message has been edited successfully?

# message_remove_v1
# User must be:
    # The user that wrote the message, or
    # The user that owns the channel, or
    # The owner of *Dreams*
# Test if the message is removed??
def test_message_remove():
    #* Ensure database is empty
    #! Clearing data
    src.other.clear_v1()

    #* Setup users and channels and create shorthand for strings for testing code
    userID1 = src.auth.auth_register_v2("ayelmao@gmail.com", "Bl00dO4th", "C", "L")
    userID2 = src.auth.auth_register_v2("lolrofl@gmail.com", "pr3ttynAme", "S", "S")
    userID3 = src.auth.auth_register_v2("zodiac@gmail.com", "T3dCruz", "T", "C")
    userID4 = src.auth.auth_register_v2("ocasio@gmail.com", "Alex4ndr1a", "A", "O")

    # userID2 made public channel 'TrumpPence'
    firstChannel = src.channels.channels_create_v1(userID2[token], 'TrumpPence', True)

    #* userID2 and userID3 join public channel 'TrumpPence'
    src.channel.channel_join_v1(userID1[token], firstChannel[cID])
    src.channel.channel_join_v1(userID3[token], firstChannel[cID])
    src.channel.channel_join_v1(userID4[token], firstChannel[cID])

    #* userID3 sends 4 messages
    message1 = message_send_v1(userID3[token], firstChannel[cID], "Yo yo waz poppin'?")
    message2 = message_send_v1(userID3[token], firstChannel[cID], "Huh?")
    message3 = message_send_v1(userID3[token], firstChannel[cID], "John Cena")
    message4 = message_send_v1(userID3[token], firstChannel[cID], "Ricegum")

    #* Test if userID1 can remove the message
    message_remove_v1(userID1[token], message1['message_id'])
    messageFound = False
    removedMessage = {}
    for messageDict in src.channel.channel_messages_v1(userID1[token], firstChannel[cID], 0)['messages']:
        if message1['message_id'] == messageDict['message_id']:
            removedMessage = messageDict
            messageFound = True
            break
    assert messageFound is True 
    assert removedMessage['message'] == '### Message Removed ###'
    

    #* Test if userID2 can remove the message
    message_remove_v1(userID2[token], message2['message_id'])
    messageFound = False
    removedMessage = {}
    for messageDict in src.channel.channel_messages_v1(userID2[token], firstChannel[cID], 0)['messages']:
        if message2['message_id'] == messageDict['message_id']:
            removedMessage = messageDict
            messageFound = True
            break
    assert messageFound is True 
    assert removedMessage['message'] == '### Message Removed ###'

    #* Test if userID3 can remove the message
    message_remove_v1(userID3[token], message3['message_id'])
    messageFound = False
    removedMessage = {}
    for messageDict in src.channel.channel_messages_v1(userID3[token], firstChannel[cID], 0)['messages']:
        if message3['message_id'] == messageDict['message_id']:
            removedMessage = messageDict
            messageFound = True
            break
    assert messageFound is True 
    assert removedMessage['message'] == '### Message Removed ###'

    #* Test if userID4 cannot remove the message
    with pytest.raises(AccessError):
        message_remove_v1(userID4[token], message4['message_id'])

# search_v1
# When query_str is >1000 characters, InputError is raised
# Test that users can only see messages in channels that they have joined
    # Test if a user who has joined no channels can see any messages



def test_message_share_todm():
    #* Ensure database is empty
    #! Clearing data

    src.other.clear_v1()

    userID1 = src.auth.auth_register_v2("testing4@gmail.com", "PasswordisKewl", "Jeffrey", "Meng")
    userID2 = src.auth.auth_register_v2("imthekewlest@gmail.com", "emfrigoslover123", "Meng", "Jeffrey")
    userID3 = src.auth.auth_register_v2("zodiac@gmail.com", "T3dCruz", "T", "C")
    userID4 = src.auth.auth_register_v2("gmailgmail@gmail.com", "hiiiiii12345", "M", "C")
    
    channelTest = src.channels.channels_create_v1(userID1[token], 'Channel', True)
    src.channel.channel_invite_v1(userID1[token], channelTest[cID], userID2[AuID])
    dmTest = src.dm.dm_create_v1(userID2[token],[userID4[AuID],userID3[AuID]])
    
    ogMessage = message_send_v1(userID1[token],channelTest[cID], "hello jeffrey meng") 

    sharedMessage = message_share_v1(userID2[token], ogMessage[mID],'', -1, dmTest[dmID])

    messageFound = False
    for messageDict in src.dm.dm_messages_v1(userID2[token],dmTest[dmID],0)['messages']:
        if sharedMessage['message_id'] == messageDict['message_id']:
            messageFound = True
            break
    assert messageFound is True 
    
    # userID1 is not in dmTest, raise access error
    with pytest.raises(AccessError):
        message_share_v1(userID1[token], ogMessage[mID], '', -1, dmTest[dmID])



def test_message_share_tochannel():
    #* Ensure database is empty
    #! Clearing data

    src.other.clear_v1()

    userID0 = src.auth.auth_register_v2("ownerDreams@gmail.com", "GodOwner123", "Owner", "Owner")
    userID1 = src.auth.auth_register_v2("imthekewlest@gmail.com", "emfrigoslover123", "Meng", "Jeffrey")
    userID2 = src.auth.auth_register_v2("zodiac@gmail.com", "T3dCruz", "T", "C")

    channelTest = src.channels.channels_create_v1(userID0[token], 'Channel', True)
    channelTest2 = src.channels.channels_create_v1(userID1[token], 'Channel', True)

    src.channel.channel_invite_v1(userID1[token], channelTest2[cID], userID0[AuID])
    src.channel.channel_invite_v1(userID0[token], channelTest[cID], userID2[AuID])

    ogMessage = message_send_v1(userID0[token],channelTest[cID], "hello jeffrey meng") 

    sharedMessage = message_share_v1(userID0[token], ogMessage[mID],'vincent', channelTest2[cID], -1)

    messageFound = False
    for messageDict in src.channel.channel_messages_v1(userID1[token],channelTest2[cID],0)['messages']:
        if sharedMessage['message_id'] == messageDict['message_id']:
            messageFound = True
            break
    assert messageFound is True 
 
    with pytest.raises(AccessError):
        message_share_v1(userID2[token], ogMessage[mID], '', channelTest2[cID], -1)

def test_message_share_dmtodm():
    
    #* Ensure database is empty
    #! Clearing data

    src.other.clear_v1()

    userID1 = src.auth.auth_register_v2("testing4@gmail.com", "PasswordisKewl", "Jeffrey", "Meng")
    userID2 = src.auth.auth_register_v2("imthekewlest@gmail.com", "emfrigoslover123", "Meng", "Jeffrey")
    userID3 = src.auth.auth_register_v2("zodiac@gmail.com", "T3dCruz", "T", "C")
    userID4 = src.auth.auth_register_v2("gmailgmail@gmail.com", "hiiiiii12345", "M", "C")
    
    dmTest = src.dm.dm_create_v1(userID2[token],[userID4[AuID],userID3[AuID]])
    dmTest2 = src.dm.dm_create_v1(userID1[token],[userID2[AuID]])
    
    ogMessage = message_senddm_v1(userID1[token], dmTest2[dmID], 'hello meng')

    sharedMessage = message_share_v1(userID2[token], ogMessage[mID],'wow', -1, dmTest[dmID])
    messageFound = False
    for messageDict in src.dm.dm_messages_v1(userID4[token],dmTest[dmID],0)['messages']:
        if sharedMessage['message_id'] == messageDict['message_id']:
            messageFound = True
            break
    assert messageFound is True 

    with pytest.raises(AccessError):
        message_share_v1(userID1[token], ogMessage[mID], '', -1, dmTest[dmID])

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

#* Test send functions together with message/send/v2
#? Test if message_id increases correctly

def test_senddm_access_error(user1, user2, user3):
    dm1 = src.dm.dm_create_v1(user1[token], [user2[AuID]])
    
    with pytest.raises(AccessError):
        message_senddm_v1(user3[token], dm1[dmID], '')

def test_senddm_long(user1, user2):
    message = ''
    for _ in range(1500):
        message += 'a'
    dm1 = src.dm.dm_create_v1(user1[token], [user2[AuID]])
    
    with pytest.raises(InputError):
        message_senddm_v1(user1[token], dm1[dmID], message)

def test_senddm_invalid_dm(user1):
    invalid_dm_id = -1

    with pytest.raises(InputError):
        message_senddm_v1(user1[token], invalid_dm_id, '')

def test_senddm_multiple(user1, user2):
    dm1 = src.dm.dm_create_v1(user1[token], [user2[AuID]])
    assert message_senddm_v1(user1[token], dm1[dmID], '') == {'message_id': 0}
    assert message_senddm_v1(user2[token], dm1[dmID], '') == {'message_id': 1}
    assert message_senddm_v1(user2[token], dm1[dmID], '') == {'message_id': 2}
    assert message_senddm_v1(user1[token], dm1[dmID], '') == {'message_id': 3}

def test_dm_unauthorised_user(user1, user2, invalid_token):
    #* All unauthorised user tests
    dm1 = src.dm.dm_create_v1(user1[token], [user2[AuID]])
    
    with pytest.raises(AccessError):
        message_senddm_v1(invalid_token, dm1[dmID], '')
