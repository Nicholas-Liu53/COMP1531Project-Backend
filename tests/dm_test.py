from typing import Any

import pytest
import src.data
from src.dm import dm_details_v1, dm_list_v1, dm_create_v1, dm_remove_v1, dm_invite_v1, dm_leave_v1, dm_messages_v1
from src.error import AccessError, InputError
from src.message import message_senddm_v1
from src.other import SECRET
import src.auth, src.channel, src.other
import jwt

AuID    = 'auth_user_id'
uID     = 'u_id'
cID     = 'channel_id'
allMems = 'all_members'
Name    = 'name'
dmName  = 'dm_name'
fName   = 'name_first'
lName   = 'name_last'
chans   = 'channels'
token   = 'token'
dmID    = 'dm_id'
handle  = 'handle_string'

#* Fixture that returns a JWT with invalid u_id and session_id
@pytest.fixture
def invalid_token():
    return jwt.encode({'session_id': -1, 'user_id': -1}, SECRET, algorithm='HS256')

#* Fixture that clears and registers the first user
@pytest.fixture
def user1():
    src.other.clear_v1()    
    return src.auth.auth_register_v2("first@gmail.com", "password", "User", "1")

#* Fixture that registers a second user
@pytest.fixture
def user2():
    return src.auth.auth_register_v2("second@gmail.com", "password", "User", "2")

#* Fixture that registers a third user
@pytest.fixture
def user3():
    return src.auth.auth_register_v2("third@gmail.com", "password", "User", "3")

#* Test that dm_details returns the correct values for valid inputs
def test_dm_details_valid(user1, user2):
    dm1 = dm_create_v1(user1[token], [user2[AuID]])
    expected = {
        Name: 'user1, user2',
        'members': [{
            uID: user1[AuID], 
            fName: "User",
            lName: '1',
            'email': 'first@gmail.com',
            handle: 'user1',
        }, {
            uID: user2[AuID], 
            fName: "User",
            lName: '2',
            'email': 'second@gmail.com',
            handle: 'user2',
        }
        ]
    }

    assert dm_details_v1(user1[token], dm1[dmID]) == expected
    assert dm_details_v1(user2[token], dm1[dmID]) == expected

#* Test that an InputError is raised when a user calls dm_details for a DM they are not in
def test_dm_details_access_error(user1, user2, user3):
    dm1 = dm_create_v1(user1[token], [user2[AuID]])

    with pytest.raises(AccessError):
        dm_details_v1(user3[token], dm1[dmID])

#* Test that an InputError is raised when an invalid dm_id is given
def test_dm_details_input_error(user1):
    invalid_dm_id = -2

    with pytest.raises(InputError):
        dm_details_v1(user1[token], invalid_dm_id)

#* Test when function is called when they are not in any DM
def test_dm_list_none(user1, user2, user3):
    dm_create_v1(user1[token], [user2[AuID]])
    
    assert dm_list_v1(user3[token]) == {'dms': []}

#* Test when function is called when they are in all DMs
def test_dm_list_all(user1, user2):
    dm_create_v1(user1[token], [user2[AuID]])
    
    assert dm_list_v1(user2[token]) == {'dms': [{
        dmID: 0,
        Name: 'user1, user2',
    }]}

#* Test when function is called when they are in some DMs
def test_dm_list_some(user1, user2, user3):
    dm_create_v1(user1[token], [user2[AuID]])
    dm2 = dm_create_v1(user1[token], [user2[AuID], user3[AuID]])
    
    assert dm_list_v1(user3[token]) == {'dms': [{
        dmID: dm2[dmID],
        Name: 'user1, user2, user3',
    }]}

#* Test that dm_create returns the correct values for valid inputs
def test_dm_create_valid(user1, user2):
    assert dm_create_v1(user1[token], [user2[AuID]]) == {
        dmID: 0,
        'dm_name': 'user1, user2',
    }

#* Test that dm_id increases correctly
def test_dm_id_linear_increase(user1, user2):
    assert dm_create_v1(user1[token], [user2[AuID]]) == {
        dmID: 0,
        'dm_name': 'user1, user2',
    }

    assert dm_create_v1(user1[token], [user2[AuID]]) == {
        dmID: 1,
        'dm_name': 'user1, user2',
    }

    assert dm_create_v1(user1[token], [user2[AuID]]) == {
        dmID: 2,
        'dm_name': 'user1, user2',
    }

#* Test that a DMs name doesn't change after users join/leave the DM
def test_dm_name(user1, user2, user3):
    dm1 = dm_create_v1(user1[token], [user2[AuID]])

    assert dm1[dmName] == 'user1, user2'

    dm_invite_v1(user1[token], dm1[dmID], user3[AuID])
    result1 = dm_details_v1(user1[token], dm1[dmID])
    
    assert result1[Name] == 'user1, user2'

    dm_leave_v1(user2[token], dm1[dmID])
    result2 = dm_details_v1(user1[token], dm1[dmID])
    
    assert result2[Name] == 'user1, user2'

def test_dm_create_errors(user1):
    invalid_u_id = -1
    
    with pytest.raises(InputError):
        dm_create_v1(user1[token], [invalid_u_id])

#Ethan
def test_dm_remove():
    src.other.clear_v1()
    userID1 = src.auth.auth_register_v2("1531@gmail.com", "123456", "Tom", "Zhang")
    userID2 = src.auth.auth_register_v2("comp@gmail.com", "456789", "Jack", "P")
    dm_0 = dm_create_v1(userID1[token], [userID2[AuID]])
    invalid_dm_id = -2
    with pytest.raises(InputError):
        dm_remove_v1(userID1[token], invalid_dm_id)
    with pytest.raises(AccessError):
        dm_remove_v1(userID2[token], dm_0['dm_id'])
    dm_remove_v1(userID1[token],dm_0['dm_id'])
    assert dm_list_v1(userID1[token]) == {'dms': []}
    assert dm_list_v1(userID2[token]) == {'dms': []}

def test_dm_invite():
    src.other.clear_v1()
    userID1 = src.auth.auth_register_v2("1531@gmail.com", "123456", "Tom", "Zhang")
    userID2 = src.auth.auth_register_v2("comp@gmail.com", "456789", "Jack", "P")
    userID3 = src.auth.auth_register_v2("hello@gmail.com", "xyztfvtf", "Paul", "J")
    dm_0 = dm_create_v1(userID1[token], [userID2[AuID]])
    invalid_dm_id = -2
    with pytest.raises(InputError):
        dm_invite_v1(userID1[token], invalid_dm_id, userID3[AuID])
    with pytest.raises(AccessError):
        dm_invite_v1(userID3[token], dm_0['dm_id'], userID2[AuID])
    dm_invite_v1(userID1[token], dm_0['dm_id'], userID3[AuID])
    assert dm_list_v1(userID3[token]) == {'dms': [{
        'dm_id': dm_0['dm_id'],
        'name': 'jackp, tomzhang',
    }]}

def test_dm_leave():
    src.other.clear_v1()
    userID1 = src.auth.auth_register_v2("1531@gmail.com", "123456", "Tom", "Zhang")
    userID2 = src.auth.auth_register_v2("comp@gmail.com", "456789", "Jack", "P")
    userID3 = src.auth.auth_register_v2("hello@gmail.com", "xyzxyz", "Paul", "J")
    dm_0 = dm_create_v1(userID1[token], [userID2[AuID]])
    invalid_dm_id = -2
    with pytest.raises(InputError):
        dm_leave_v1(userID1[token], invalid_dm_id)
    with pytest.raises(AccessError):
        dm_leave_v1(userID3[token], dm_0['dm_id'])
    dm_leave_v1(userID2[token], dm_0['dm_id'])
    print(dm_list_v1(userID1[token]))
    assert {dmID: dm_0[dmID], Name: 'jackp, tomzhang'} in dm_list_v1(userID1[token])['dms']
    assert dm_list_v1(userID2[token]) == {'dms': []}

def test_dm_messages():
    src.other.clear_v1()
    userID1 = src.auth.auth_register_v2("1531@gmail.com", "123456", "Tom", "Zhang")
    userID2 = src.auth.auth_register_v2("comp@gmail.com", "456789", "Jack", "P")
    userID3 = src.auth.auth_register_v2("hello@gmail.com", "135769", "Harry", "J")
    dm_0 = dm_create_v1(userID1[token], [userID2[AuID]])
    dm_1 = dm_create_v1(userID2[token], [userID3[AuID]])
    invalid_dm_id = -2

    #Input error when DM ID not valid or start is greater than # of messages in DM
    with pytest.raises(InputError):
        #Start greater than # of messages in DM
        dm_messages_v1(userID1[token], dm_0['dm_id'], 1)
    with pytest.raises(InputError):
        #DM ID not valid
        dm_messages_v1(userID1[token], invalid_dm_id, 0)
        

    #Access error when Authorised user is not a member of DM with dm_id
    with pytest.raises(AccessError):
        dm_messages_v1(userID3[token], dm_0['dm_id'], 0)

    assert dm_messages_v1(userID1[token], dm_0['dm_id'], 0) == {
        'messages': [],
        'start': 0,
        'end': -1,
    }

    #Send DM to dm_1 to make sure that it is sending to the correct dm
    message_senddm_v1(userID2[token], dm_1['dm_id'], "Lawl")

    #Add certain number of DMs to dm_0 e.g. 10
    message_counter = 0
    while message_counter < 10:
        message_senddm_v1(userID1[token], dm_0['dm_id'], f"{message_counter}")
        message_counter += 1

    #Check dm_0 is correct
    return_dict = dm_messages_v1(userID1[token], dm_0['dm_id'],0)
    assert len(return_dict['messages']) == 10
    assert return_dict['start'] == 0
    assert return_dict['end'] == -1

    #Check dm_1 is unaffected
    return_dict_dm_1 = dm_messages_v1(userID1[token], dm_0['dm_id'],0)
    assert len(return_dict_dm_1['messages']) == 1
    assert return_dict_dm_1['start'] == 0
    assert return_dict_dm_1['end'] == -1

    #add so that there are 51 messages in DM
    while message_counter < 51:
        message_senddm_v1(userID1[token], dm_0[dmID], f"{message_counter}")
        message_counter += 1

    return_dict2 = dm_messages_v1(userID1[token], dm_0['dm_id'], 0)
    assert len(return_dict2['messages']) == 50
    assert return_dict2['start'] == 0
    assert return_dict2['end'] == 50

    #Case when start is not equal to 0 but there are 51 messages in DM
    #If start is 20, there should be 32 messages in dictionary
    return_dict3 = dm_messages_v1(userID1[token], dm_0['dm_id'], 20)
    assert len(return_dict3['messages']) == 31
    assert return_dict3['start'] == 20
    assert return_dict3['end'] == -1

#* Test for unauthorised users for all dm functions
def test_dm_unauthorised_user(user1, user2, invalid_token):
    dm1 = dm_create_v1(user1[token], [user2[AuID]])

    with pytest.raises(AccessError):
        dm_details_v1(invalid_token, dm1[dmID])
        dm_list_v1(invalid_token)
        dm_create_v1(invalid_token, [user1[AuID]])
        dm_remove_v1(invalid_token, dm1[dmID])
        dm_invite_v1(invalid_token, dm1[dmID], user2[AuID])
        dm_leave_v1(invalid_token, dm1[dmID])
        dm_messages_v1(invalid_token, dm1[dmID], 0)
