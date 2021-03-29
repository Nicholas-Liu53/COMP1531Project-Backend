# File to test functions in src/admin.py
import pytest
from src.admin import user_remove_v1, userpermission_change_v1, notifications_get_v1
from src.error import AccessError, InputError
import src.channel, src.channels, src.auth, src.dm, src.message, src.other

AuID    = 'auth_user_id'
uID     = 'u_id'
cID     = 'channel_id'
chans   = 'channels'
allMems = 'all_members'
ownMems = 'owner_members'
fName   = 'name_first'
lName   = 'name_last'
token = 'token'


def test_user_remove():
    pass

def test_userpermissions_change():
    #* Ensure database is empty
    #! Clearing data

    src.other.clear_v1()

    #first is always owner
    userID0 = src.auth.auth_register_v2("ownerDreams@gmail.com", "GodOwner123", "Owner", "Owner")

    userID1 = src.auth.auth_register_v2("testing4@gmail.com", "PasswordisKewl", "Jeffrey", "Meng")
    userID2 = src.auth.auth_register_v2("peasantnotOwner@gmail.com", "emfrigoslover123", "Owner", "Not")


    # Test if the user gets the permissions
    userpermission_change_v1(userID0[token], userID1[AuID], 1)

    channelTest = src.channels.channels_create_v1(userID2[token], 'Channel', False)

    src.channel.channel_join_v1(userID1[AuID], channelTest[cID])

    assert {
        uID: userID1[AuID],        
        fName: 'Meng',
        lName: 'Jeffrey',
        'email': 'testing4@gmail.com',
        'handle_string': 'mengjeffrey',
    } in channel_details_v1(userID1[token], channelTest[cID])[allMems]

    src.channel.channel_addowner_v1(userID1[token], channelTest[cID], userID1[AuID])

    assert {
        uID: userID1[AuID],        
        fName: 'Meng',
        lName: 'Jeffrey',
        'email': 'testing4@gmail.com',
        'handle_string': 'mengjeffrey',
    } in channel_details_v1(userID1[token], channelTest[cID])[ownMems]

    src.channel.channel_removeowner_v1(userID1[token], channelTest[cID], userID2[AuID])

    assert {
        uID: userID1[AuID],        
        fName: 'Not',
        lName: 'Owner',
        'email': 'peasantnotOwner@gmail.com',
        'handle_string': 'notowner',
    } not in channel_details_v1(userID1[token], channelTest[cID])[ownMems]

    assert {
        uID: userID1[AuID],        
        fName: 'Not',
        lName: 'Owner',
        'email': 'peasantnotOwner@gmail.com',
        'handle_string': 'notowner',
    } in channel_details_v1(userID1[token], channelTest[cID])[allMems]

    with pytest.raises(InputError):
        userpermission_change_v1(userID0[token], userID1[AuID], -1)
    
    with pytest.raises(InputError):
        userpermission_change_v1(userID0[token], 9999, 0)

    with pytest.raises(AccessError):
        userpermission_change_v1(userID2[token], 9999, 0)

def test_notifications_get():
    pass