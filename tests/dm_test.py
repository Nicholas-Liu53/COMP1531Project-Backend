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

def test_dm_details_access_error(user1, user2, user3):
    dm1 = dm_create_v1(user1[token], [user2[AuID]])

    with pytest.raises(AccessError):
        dm_details_v1(user3[token], dm1[dmID])

def test_dm_details_input_error(user1, user2):
    invalid_dm_id = -1

    with pytest.raises(InputError):
        dm_details_v1(user1[token], invalid_dm_id)

def test_dm_list_none(user1, user2, user3):
    dm_create_v1(user1[token], [user2[AuID]])
    
    assert dm_list_v1(user3[token]) == {'dms': []}

def test_dm_list_all(user1, user2):
    dm_create_v1(user1[token], [user2[AuID]])
    
    assert dm_list_v1(user2[token]) == {'dms': [{
        dmID: 0,
        Name: 'user1, user2',
    }]}

def test_dm_list_some(user1, user2, user3):
    dm_create_v1(user1[token], [user2[AuID]])
    dm2 = dm_create_v1(user1[token], [user2[AuID], user3[AuID]])
    
    assert dm_list_v1(user3[token]) == {'dms': [{
        dmID: dm2[dmID],
        Name: 'user1, user2, user3',
    }]}

def test_dm_create_valid(user1, user2):
    assert dm_create_v1(user1[token], [user2[AuID]]) == {
        dmID: 0,
        'dm_name': 'user1, user2',
    }

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

def test_dm_id_delete_middle(user1, user2):
    dm_create_v1(user1[token], [user2[AuID]])
    dm2 = dm_create_v1(user1[token], [user2[AuID]])
    dm_create_v1(user1[token], [user2[AuID]])
    dm_remove_v1(user1[token], dm2[dmID])

    assert dm_create_v1(user1[token], [user2[AuID]]) == {
        dmID: 3,
        'dm_name': 'user1, user2',
    }

def test_dm_id_delete_end(user1, user2):
    dm_create_v1(user1[token], [user2[AuID]])
    dm2 = dm_create_v1(user1[token], [user2[AuID]])
    dm_remove_v1(user1[token], dm2[dmID])
    
    assert dm_create_v1(user1[token], [user2[AuID]]) == {
        dmID: 2,
        dmName: 'user1, user2',
    }

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
    invalid_dm_id = -1
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
    userID3 = src.auth.auth_register_v2("hello@gmail.com", "xyz", "Paul", "J")
    dm_0 = dm_create_v1(userID1[token], [userID2[AuID]])
    invalid_dm_id = -1
    with pytest.raises(InputError):
        dm_invite_v1(userID1[token], invalid_dm_id, userID3)
    with pytest.raises(AccessError):
        dm_invite_v1(userID4[token], dm_0['dm_id'], userID3)
    dm_invite_v1(userID1[token], dm_0['dm_id'], userID3)
    assert dm_list_v1(userID1[token]) == {'dms': [dm_0['dm_id']]}
    assert  dm_list_v1(userID2[token]) == {'dms': [dm_0['dm_id']]}
    assert dm_list_v1(userID3[token]) == {'dms': [dm_0['dm_id']]}

def test_dm_leave():
    src.other.clear_v1()
    userID1 = src.auth.auth_register_v2("1531@gmail.com", "123456", "Tom", "Zhang")
    userID2 = src.auth.auth_register_v2("comp@gmail.com", "456789", "Jack", "P")
    userID3 = src.auth.auth_register_v2("hello@gmail.com", "xyzxyz", "Paul", "J")
    dm_0 = dm_create_v1(userID1[token], [userID2[AuID]])
    invalid_dm_id = -1
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
    invalid_dm_id = -1

    #Input error when DM ID not valid or start is greater than # of messages in DM
    with pytest.raises(InputError):
        #DM ID not valid
        dm_messages_v1(userID1[token], invalid_dm_id, 0)
        #Start greater than # of messages in DM
        dm_messages_v1(userID1[token], dm_0['dm_id'], 1)

    #Access error when Authorised user is not a member of DM with dm_id
    with pytest.raises(AccessError):
        dm_messages_v1(userID3[token], dm_0['dm_id'], 0)

    assert dm_messages_v1(userID1[token], dm_0['dm_id'], 0) == {
        'messages': [],
        'start': 0,
        'end': -1,
    }
    #Add certain number of DMs to dm_0 e.g. 10
    message_counter = 0
    while message_counter < 10:
        
        message_counter += 1

    assert dm_messages_v1(userID1[token], dm_0['dm_id'],0) == {
        'messages': ['0','1','2','3','4','5','6','7','8','9','10'],
        'start': 0,
        'end': -1,
    }
covera
    #add so that there are 51 messages in DM
    while message_counter < 51:
        message_senddm_v1()
        message_senddm_v1(userID1[token], dm_0[dmID], '')
        message_counter += 1

    assert dm_messages_v1(userID1[token], dm_0['dm_id'], 0) == {
        'messages: ['0','1','2','3','4','5','6','7','8','9','10','11','12', '13','14','15','16','17','18','19','20','21','22','23', '24','25','26','27','28','29','30','31','32','33','34', '35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50'],
        'start': 0,
        'end': 50,
    }

def test_dm_unauthorised_user(user1, user2, invalid_token):
    #* Test for unauthorised users for all dm functions  
    dm1 = dm_create_v1(user1[token], [user2[AuID]])

    with pytest.raises(AccessError):
        dm_details_v1(invalid_token, dm1[dmID])
        dm_list_v1(invalid_token)
        dm_create_v1(invalid_token, [user1[AuID]])
        dm_remove_v1(invalid_token, dm1[dmID])
        dm_invite_v1(invalid_token, dm1[dmID], user2[AuID])
        dm_leave_v1(invalid_token, dm1[dmID])
        dm_messages_v1(invalid_token, dm1[dmID], 0)