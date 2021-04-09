# file to test functions in src/message.py
import pytest
from src.message import message_send_v1, message_remove_v1, message_edit_v1, message_share_v1, message_senddm_v1
from src.error import InputError, AccessError
import src.channel, src.channels, src.auth, src.dm
from src.other import clear_v1, SECRET
from datetime import timezone, datetime
import jwt


AuID     = 'auth_user_id'
uID      = 'u_id'
cID      = 'channel_id'
chans    = 'channels'
allMems  = 'all_members'
ownMems  = 'owner_members'
fName    = 'name_first'
lName    = 'name_last'
token    = 'token'
mID      = 'message_id'
dmID     = 'dm_id'
Name     = 'name'
thumbsUp = 1
rID      = 'react_id'

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

@pytest.fixture
def user4():
    return src.auth.auth_register_v2("fourth@gmail.com", "password", "User", "4")

@pytest.fixture
def user5():
    return src.auth.auth_register_v2("fifth@gmail.com", "password", "User", "5")


# message_send_v1
# When message is >1000 characters, InputError is raised
# When authorised user is not part of the channel that they are trying to post in, AccessError is raised
# After the function is sucessfully run, ensure that the return value is correct
def test_message_send(user1, user2, user3, user4):

    # user1 made public channel 'TrumpPence'
    firstChannel = src.channels.channels_create_v1(user1[token], 'TrumpPence', True)

    #* user2 and user3 join public channel 'TrumpPence'
    src.channel.channel_join_v1(user2[token], firstChannel[cID])
    src.channel.channel_join_v1(user3[token], firstChannel[cID])

    #* Test if a super large message raises an InputError
    message = ''
    for _ in range(1500):
        message += '?'
    with pytest.raises(InputError):
        message_send_v1(user1[token], firstChannel[cID], message)

    #* Test if a user not in the channel tries to send a message into the channel
    with pytest.raises(AccessError):
        message_send_v1(user4[token], firstChannel[cID], '?')

    #* Test a message is successfully sent 
    sendOutput = message_send_v1(user1[token], firstChannel[cID], "Hi")
    messageFound = False
    for messageDict in src.channel.channel_messages_v1(user1[token], firstChannel[cID], 0)['messages']:
        if sendOutput['message_id'] == messageDict['message_id']:
            messageFound = True
            break
    assert messageFound is True 

    #* Test another messsage is successfully sent
    sendOutput = message_send_v1(user3[token], firstChannel[cID], "Sup")
    messageFound = False
    for messageDict in src.channel.channel_messages_v1(user1[token], firstChannel[cID], 0)['messages']:
        if sendOutput['message_id'] == messageDict['message_id']:
            messageFound = True
            break
    assert messageFound is True 

    #* All tests passed
    #! Clearing data
    clear_v1()

# message_edit_v1
# When message is >1000 characters, InputError is raised
# If there are no messages with matching message_id, InputError is raised
# Ownership permission tests:
    # Owner of Dreams should be able to edit anything
    # Owner of channels should be able to edit anything in channels they own
    # Non-owner of channels should only be able to edit their own messages
# Test if a message has been edited successfully?
def test_message_edit(user1, user2, user3, user4):

    # user2 made public channel 'TrumpPence'
    firstChannel = src.channels.channels_create_v1(user2[token], 'TrumpPence', True)

    #* user2 and user3 join public channel 'TrumpPence'
    src.channel.channel_join_v1(user1[token], firstChannel[cID])
    src.channel.channel_join_v1(user3[token], firstChannel[cID])
    src.channel.channel_join_v1(user4[token], firstChannel[cID])

    #* user3 sends 4 messages
    message1 = message_send_v1(user3[token], firstChannel[cID], "Yo yo waz poppin'?")
    message2 = message_send_v1(user3[token], firstChannel[cID], "Huh?")
    message3 = message_send_v1(user3[token], firstChannel[cID], "John Cena")
    message4 = message_send_v1(user3[token], firstChannel[cID], "Ricegum")

    #* Test if user1 can edit the message
    message_edit_v1(user1[token], message1['message_id'], 'Jeffrey Meng')
    messageFound = False
    editedMessage = {}
    for messageDict in src.channel.channel_messages_v1(user1[token], firstChannel[cID], 0)['messages']:
        if message1['message_id'] == messageDict['message_id']:
            editedMessage = messageDict
            messageFound = True
            break
    assert messageFound is True 
    assert editedMessage['message'] == 'Jeffrey Meng'
    

    #* Test if user2 can edit the message
    message_edit_v1(user2[token], message2['message_id'], 'Jeffrey Meng')
    messageFound = False
    editedMessage = {}
    for messageDict in src.channel.channel_messages_v1(user2[token], firstChannel[cID], 0)['messages']:
        if message2['message_id'] == messageDict['message_id']:
            editedMessage = messageDict
            messageFound = True
            break
    assert messageFound is True 
    assert editedMessage['message'] == 'Jeffrey Meng'

    #* Test if user3 can edit the message
    message_edit_v1(user3[token], message3['message_id'], 'Jeffrey Meng')
    messageFound = False
    editedMessage = {}
    for messageDict in src.channel.channel_messages_v1(user3[token], firstChannel[cID], 0)['messages']:
        if message3['message_id'] == messageDict['message_id']:
            editedMessage = messageDict
            messageFound = True
            break
    assert messageFound is True 
    assert editedMessage['message'] == 'Jeffrey Meng'

    #* Test if user4 cannot edit the message
    with pytest.raises(AccessError):
        message_edit_v1(user4[token], message4['message_id'], 'Jeffrey Meng')

    #* Test if empty edit removes message
    message_edit_v1(user3[token], message3['message_id'], '')
    messageFound = False
    for messageDict in src.channel.channel_messages_v1(user3[token], firstChannel[cID], 0)['messages']:
        if message3['message_id'] == messageDict['message_id']:
            messageFound = True
            break
    assert messageFound is False

    #* Test if you cannot edit a message that doesn't exist
    with pytest.raises(InputError):
        message_edit_v1(user2[token], -1, "Troll")

    #* Test you cannot edit into a super long message
    tooLong = ""
    for _ in range(1001):
        tooLong += "?"
    with pytest.raises(InputError):
        message_edit_v1(user2[token], message4['message_id'], tooLong) 

    #* Test in dm
    dm1 = src.dm.dm_create_v1(user1[token], [user2[AuID]])
    dmMessage = message_senddm_v1(user1[token], dm1[dmID], "Herp derp")
    with pytest.raises(AccessError):
        message_edit_v1(user2[token], dmMessage['message_id'], 'Jeffrey Meng')

    #* All tests passed
    #! Clearing data
    clear_v1()

# message_remove_v1
# User must be:
    # The user that wrote the message, or
    # The user that owns the channel, or
    # The owner of *Dreams*
# Test if the message is removed??
def test_message_remove(user1, user2, user3, user4):

    # user2 made public channel 'TrumpPence'
    firstChannel = src.channels.channels_create_v1(user2[token], 'TrumpPence', True)

    #* user2 and user3 join public channel 'TrumpPence'
    src.channel.channel_join_v1(user1[token], firstChannel[cID])
    src.channel.channel_join_v1(user3[token], firstChannel[cID])
    src.channel.channel_join_v1(user4[token], firstChannel[cID])

    #* user3 sends 4 messages
    message1 = message_send_v1(user3[token], firstChannel[cID], "Yo yo waz poppin'?")
    message2 = message_send_v1(user3[token], firstChannel[cID], "Huh?")
    message3 = message_send_v1(user3[token], firstChannel[cID], "John Cena")
    message4 = message_send_v1(user3[token], firstChannel[cID], "Ricegum")

    #* Test if user1 can remove the message
    message_remove_v1(user1[token], message1['message_id'])
    messageFound = False
    for messageDict in src.channel.channel_messages_v1(user1[token], firstChannel[cID], 0)['messages']:
        if message1['message_id'] == messageDict['message_id']:
            messageFound = True
            break
    assert messageFound is False
    

    #* Test if user2 can remove the message
    message_remove_v1(user2[token], message2['message_id'])
    messageFound = False
    for messageDict in src.channel.channel_messages_v1(user2[token], firstChannel[cID], 0)['messages']:
        if message2['message_id'] == messageDict['message_id']:
            messageFound = True
            break
    assert messageFound is False

    #* Test if user3 can remove the message
    message_remove_v1(user3[token], message3['message_id'])
    messageFound = False
    for messageDict in src.channel.channel_messages_v1(user3[token], firstChannel[cID], 0)['messages']:
        if message3['message_id'] == messageDict['message_id']:
            messageFound = True
            break
    assert messageFound is False

    #* Test if user4 cannot remove the message
    with pytest.raises(AccessError):
        message_remove_v1(user4[token], message4['message_id'])

    #* Test if you cannot remove a message that doesn't exist
    with pytest.raises(InputError):
        message_remove_v1(user4[token], -1)

    #* All tests passed
    #! Clearing data
    clear_v1()

def test_message_share_todm(user1, user2, user3, user4):

    channelTest = src.channels.channels_create_v1(user1[token], 'Channel', True)
    src.channel.channel_invite_v1(user1[token], channelTest[cID], user2[AuID])
    dmTest = src.dm.dm_create_v1(user2[token],[user4[AuID],user3[AuID]])
    
    ogMessage = message_send_v1(user1[token],channelTest[cID], "hello jeffrey meng") 

    sharedMessage = message_share_v1(user2[token], ogMessage[mID],'', -1, dmTest[dmID])

    messageFound = False
    for messageDict in src.dm.dm_messages_v1(user2[token],dmTest[dmID],0)['messages']:
        if sharedMessage['message_id'] == messageDict['message_id']:
            messageFound = True
            break
    assert messageFound is True 
    
    # user1 is not in dmTest, raise access error
    with pytest.raises(AccessError):
        message_share_v1(user1[token], ogMessage[mID], '', -1, dmTest[dmID])

def test_message_share_tochannel(user1, user2, user3):

    channelTest = src.channels.channels_create_v1(user1[token], 'Channel', True)
    channelTest2 = src.channels.channels_create_v1(user2[token], 'Channel', True)

    src.channel.channel_invite_v1(user2[token], channelTest2[cID], user1[AuID])
    src.channel.channel_invite_v1(user1[token], channelTest[cID], user3[AuID])

    ogMessage = message_send_v1(user1[token],channelTest[cID], "hello jeffrey meng") 

    sharedMessage = message_share_v1(user1[token], ogMessage[mID],'vincent', channelTest2[cID], -1)

    messageFound = False
    for messageDict in src.channel.channel_messages_v1(user2[token],channelTest2[cID],0)['messages']:
        if sharedMessage['message_id'] == messageDict['message_id']:
            messageFound = True
    assert messageFound is True 

    with pytest.raises(AccessError):
        message_share_v1(user3[token], ogMessage[mID], '', channelTest2[cID], -1)

def test_message_share_dmtodm(user1,user2,user3,user4):
    
    dmTest = src.dm.dm_create_v1(user2[token],[user4[AuID],user3[AuID]])
    dmTest2 = src.dm.dm_create_v1(user1[token],[user2[AuID]])
    
    ogMessage = message_senddm_v1(user1[token], dmTest2[dmID], 'hello meng')

    sharedMessage = message_share_v1(user2[token], ogMessage[mID],'wow', -1, dmTest[dmID])
    messageFound = False
    for messageDict in src.dm.dm_messages_v1(user4[token],dmTest[dmID],0)['messages']:
        if sharedMessage['message_id'] == messageDict['message_id']:
            messageFound = True

    assert messageFound is True 

    with pytest.raises(AccessError):
        message_share_v1(user1[token], ogMessage[mID], '', -1, dmTest[dmID])

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
        
        
        
#Iteration 3
#Test for invalid message id for message_react
def test_message_react_v1__errors_invalid_mID(user1, user2):
    invalid_message_id = -1 
    with pytest.raises(InputError):
        message_react_v1(user1[token], invalid_message_id, thumbsUp) 

#Test for invalid react id for message_react 
def test_message_react_v1_channel_errors_invalid_rID(user1, user2): 
    channel_1 = src.channels.channels_create_v1(user1[token], 'Channel', True)
    message_1 = message_send_v1(user1[token], channel_1[cID], "Hello")
    
    dm_1 = src.dm.dm_create_v1(user1[token], [user2[AuID]])
    message_2 = message.senddm_v1(user1[token], dm_1[dmID], "Goodbye")
    
    invalid_react_id = -1 
    #Invalid rID for channel 
    with pytest.raises(InputError):
        message_react_v1(user1[token], message_1[mID], invalid_react_id) 
        
    #Invalid rID for DM
    with pytest.raises(InputError):
        message_react_v1(user1[token], message_2[mID], invalid_react_id)
    
        
#Test that already contains an active react raises input error  
def test_message_react_v1_channel_active_react(user1, user2):
    channel_1 = src.channels.channels_create_v1(user1[token], 'Channel', True)
    message_1 = src.message.message_send_v1(user1[token], channel_1[cID], "Hello")
    react_1 = message_react_v1(user1[token], message_1[mID], thumbsUp)
       
    dm_1 = src.dm.dm_create_v1(user1[token], [user2[AuID]])
    message_2 = message_senddm_v1(user1[token], dm_1[dmID], "Goodbye")
    react_2 = message_react_v1(user1[token], message_2[mID], thumbsUp)
    
    #Already contains react in channel error 
    with pytest.raises(InputError):
        message_react_v1(user1[token], message_1[mID], thumbsUp)
        
    #Already contains react in DM error
    with pytest.raises(InputError):
        message_react_v1(user1[token], message_2[mID], thumbsUp)
    
    
#Test that authorised user not a member of channel or dm raises access error for message_react 
def test_message_react_v1_channel_invalid_user(user1, user2, user3): 
    channel_1 = src.channels.channels_create_v1(user1[token], 'Channel', False)
    message_1 = message_send_v1(user1[token], channel_1[cID], "Hello")
    #Not a member of channel 
    with pytest.raises(AccessError):
        message_react_v1(user2[token], message1[mID], thumbsUp)
        
    #Not a member of DM 
    dm_1 = src.dm.dm_create_v1(user1[token], [user2[AuID]])
    message_2 = message_senddm_v1(user1[token], dm_1[dmID], "Goodbye")
    with pytest.raises(AccessError):
        message_react_v1(user3[token], message2[mID], thumbsUp)


#Test that message_react works for a message in a channel
def test_message_react_v1_valid_channel(user1, user2):
    channel_1 = src.channels.channels_create_v1(user1[token], 'Channel', False)
    src.channel.channel_invite_v1(user1[token], channel_1[cID], user2[AuID])
    message_1 = message_send_v1(user1[token], channel_1[cID], "Hello")
    react_1 = message_react_v1(user1[token], message_1[mID], thumbsUp)
    
    #Test 1: check that react_1 comes up in "messages"
    result = src.channel.channel_messages_v1(user1[token], channel_1[cID], 0)
    
    #Create for loop that finds message looking for 
    for current_message in range(len(result[messages])): 
        if result['messages'][mID] == message_1[mID]]: 
            #Now that the message is found, can assert that our user has reacted to it
            assert user1[uID] in result['messages'][current_message]['reacts']['u_ids'] 
    
    
    #Test 2: check that is given a notification for "reacted message"
    



#Test that message_react works for a dm 
def test_message_react_v1_valid_dm(user1, user2):
    dm_1 = src.dm.dm_create_v1(user1[token], [user2[AuID]])
    message_1 = message_senddm_v1(user1[token], dm_1[dmID], "Goodbye")
    react_1 = message_react_v1(user1[token], message_1[mID], thumbsUp)
    
    #Test 1: check that reacts comes up in "messages"
    result = src.dm.dm_messages_v1(user1[token], dm_1[dmID], 0)
    #Create for loop that finds message looking for 
    for current_message in range(len(result[messages])): 
        if result['messages'][mID] == message_1[mID]]: 
            #Now that the message is found, can assert that our user has reacted to it
            assert user1[uID] in result['messages'][current_message]['reacts']['u_ids'] 
    
    #Test 2: check that is given a notification for "reacted message"



#Test that message_unreact raises appropriate errors 
def test_message_unreact_v1_errors():

    #Input error 1: message_id not a valid message within channel or DM
    
    
    #Input error 2: react_id is not a valid id 
    invalid_react_id = -1
    
    
    #Input error 3: Message with ID message_id does not contain an active react from the authorised user 
    
    
    #Access Error 1: The authorised user is not a member of channel or DM the message is within 
    



#Test that message_unreact works for a message in a channel 
def test_message_uncreact_v1_valid_channel():
#Remove a react for a message within a channel or a dm the authorised user is part of 

#Test: check that reacts no longer comes up in "messages"

#Assumption: initial notification for is not removed 



#Test that message_unreact works for a message in a dm 
def test_message_uncreact_v1_valid_dm():
#Remove a react for a message within a channel or a dm the authorised user is part of 

#Test: check that reacts no longer comes up in "messages"

#Assumption: initial notification for is not removed 

