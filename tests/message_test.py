import pytest
from src.message import message_send_v1, message_remove_v1, message_edit_v1
from src.error import InputError, AccessError
import src.channel, src.channels, src.auth
from src.other import clear_v1

AuID    = 'auth_user_id'
uID     = 'u_id'
cID     = 'channel_id'
allMems = 'all_members'
cName   = 'name'
fName   = 'name_first'
lName   = 'name_last'
chans   = 'channels'

# message_send_v1
# When message is >1000 characters, InputError is raised
# When authorised user is not part of the channel that they are trying to post in, AccessError is raised
# After the function is sucessfully run, ensure that the return value is correct
def test_message_send():
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

    #* userID2 and userID3 join public channel 'TrumpPence'
    channel_join_v1(userID2[AuID], firstChannel[cID])
    channel_join_v1(userID3[AuID], firstChannel[cID])

    #* Test if a super large message raises an InputError
    for _ in range(1500):
        message += '?'
    with pytest.raises(InputError):
        message_send_v1(userID1[token], firstChannel[cID], message)

    #* Test if a user not in the channel tries to send a message into the channel
    with pytest.raises(AccessError):
        message_send_v1(userID4[token], firstChannel[cID], '?')

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

# search_v1
# When query_str is >1000 characters, InputError is raised
# Test that users can only see messages in channels that they have joined
    # Test if a user who has joined no channels can see any messages
