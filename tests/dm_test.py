import pytest
import src.data
from src.dm import dm_details_v1, dm_list_v1, dm_create_v1, dm_remove_v1, dm_invite_v1, dm_leave_v1, dm_messages_v1
from src.error import AccessError, InputError
import src.auth, src.channel, src.other
import jwt

AuID    = 'auth_user_id'
uID     = 'u_id'
cID     = 'channel_id'
allMems = 'all_members'
Name   = 'name'
fName   = 'name_first'
lName   = 'name_last'
chans   = 'channels'
token   = 'token'
dmID    = 'dm_id'

SECRET = 'MENG'

#! Make sure to clear before every test

def test_dm_details_valid():
    src.other.clear_v1()
    user1 = src.auth.auth_register_v1("first@gmail.com", "password", "Steve", "Irwin")
    user2 = src.auth.auth_register_v1("second@gmail.com", "password", "Jonah", "from Tonga")
    dm1 = dm_create_v1(user1[token], [user2[AuID]])
    expected = {
        dmID: 0,
        Name: 'jonahfromtonga, steveirwin',
    }

    assert dm_details_v1(user1[token], dm1[dmID]) == expected
    assert dm_details_v1(user2[token], dm1[dmID]) == expected

def test_dm_details_errors():
    src.other.clear_v1()
    invalid_dm_id = -1
    user1 = src.auth.auth_register_v1("first@gmail.com", "password", "Steve", "Irwin")
    user2 = src.auth.auth_register_v1("second@gmail.com", "password", "Jonah", "from Tonga")

    with pytest.raises(InputError):
        dm_details_v1(user1[token], invalid_dm_id)

    src.other.clear_v1()
    user1 = src.auth.auth_register_v1("first@gmail.com", "password", "Steve", "Irwin")
    user2 = src.auth.auth_register_v1("second@gmail.com", "password", "Jonah", "from Tonga")
    user3 = src.auth.auth_register_v1("third@gmail.com", "password", "Rock", "Sand")
    dm1 = dm_create_v1(user1[token], [user2[AuID]])

    with pytest.raises(AccessError):
        dm_details_v1(user3[token], dm1[dmID])

def test_dm_list():
    src.other.clear_v1()
    user1 = src.auth.auth_register_v1("first@gmail.com", "password", "Steve", "Irwin")
    user2 = src.auth.auth_register_v1("second@gmail.com", "password", "Jonah", "from Tonga")
    user3 = src.auth.auth_register_v1("third@gmail.com", "password", "Rock", "Sand")
    dm_create_v1(user1[token], [user2[AuID]])
    
    assert dm_list_v1(user3[token]) == {'dms': []}
    
    src.other.clear_v1()
    user1 = src.auth.auth_register_v1("first@gmail.com", "password", "Steve", "Irwin")
    user2 = src.auth.auth_register_v1("second@gmail.com", "password", "Jonah", "from Tonga")
    dm_create_v1(user1[token], [user2[AuID]])
    
    assert dm_list_v1(user3[token]) == {'dms': [{
        dmID: 0,
        Name: 'jonahfromtonga, steveirwin',
    }]}

    src.other.clear_v1()
    user1 = src.auth.auth_register_v1("first@gmail.com", "password", "Steve", "Irwin")
    user2 = src.auth.auth_register_v1("second@gmail.com", "password", "Jonah", "from Tonga")
    user3 = src.auth.auth_register_v1("third@gmail.com", "password", "Rock", "Sand")
    dm_create_v1(user1[token], [user2[AuID]])
    dm_create_v1(user1[token], [user2[AuID], user3[AuID]])
    
    assert dm_list_v1(user3[token]) == {'dms': [{
        dmID: 1,
        Name: 'jonahfromtonga, steveirwin',
    }]}

def test_dm_create_valid():
    src.other.clear_v1()
    user1 = src.auth.auth_register_v1("first@gmail.com", "password", "Steve", "Irwin")
    user2 = src.auth.auth_register_v1("second@gmail.com", "password", "Jonah", "from Tonga")
    
    assert dm_create_v1(user1[token], [user2[AuID]]) == {
        dmID: 0,
        Name: 'jonahfromtonga, steveirwin',
    }

def test_dm_id_increasing():
    src.other.clear_v1()
    user1 = src.auth.auth_register_v1("first@gmail.com", "password", "Steve", "Irwin")
    user2 = src.auth.auth_register_v1("second@gmail.com", "password", "Jonah", "from Tonga")
    
    assert dm_create_v1(user1[token], [user2[AuID]]) == {
        dmID: 0,
        Name: 'jonahfromtonga, steveirwin',
    }

    assert dm_create_v1(user1[token], [user2[AuID]]) == {
        dmID: 1,
        Name: 'jonahfromtonga, steveirwin',
    }

    assert dm_create_v1(user1[token], [user2[AuID]]) == {
        dmID: 2,
        Name: 'jonahfromtonga, steveirwin',
    }

    src.other.clear_v1()
    user1 = src.auth.auth_register_v1("first@gmail.com", "password", "Steve", "Irwin")
    user2 = src.auth.auth_register_v1("second@gmail.com", "password", "Jonah", "from Tonga")
    dm_create_v1(user1[token], [user2[AuID]])
    dm2 = dm_create_v1(user1[token], [user2[AuID]])
    dm_create_v1(user1[token], [user2[AuID]])
    dm_remove_v1(user1[token], dm2[dmID])
    
    assert dm_create_v1(user1[token], [user2[AuID]]) == {
        dmID: 3,
        Name: 'jonahfromtonga, steveirwin',
    }

    src.other.clear_v1()
    user1 = src.auth.auth_register_v1("first@gmail.com", "password", "Steve", "Irwin")
    user2 = src.auth.auth_register_v1("second@gmail.com", "password", "Jonah", "from Tonga")
    dm_create_v1(user1[token], [user2[AuID]])
    dm2 = dm_create_v1(user1[token], [user2[AuID]])
    dm_remove_v1(user1[token], dm2[dmID])
    
    assert dm_create_v1(user1[token], [user2[AuID]]) == {
        dmID: 2,
        Name: 'jonahfromtonga, steveirwin',
    }

def test_dm_name():
    src.other.clear_v1()
    user1 = src.auth.auth_register_v1("first@gmail.com", "password", "Steve", "Irwin")
    user2 = src.auth.auth_register_v1("second@gmail.com", "password", "Jonah", "from Tonga")
    user3 = src.auth.auth_register_v1("third@gmail.com", "password", "Rock", "Sand")
    dm1 = dm_create_v1(user1[token], [user2[AuID]])

    assert dm1[Name] == 'jonahfromtonga, steveirwin'

    dm_invite_v1(user1[token], dm1[dmID], user3[AuID])
    result1 = dm_details_v1(user1[token], dm1[dmID])
    
    assert result1[Name] == 'jonahfromtonga, steveirwin'

    dm_leave_v1(user2[token], dm1[dmID])
    result2 = dm_details_v1(user1[token], dm1[dmID])
    
    assert result2[Name] == 'jonahfromtonga, steveirwin'

def test_dm_create_errors():
    src.other.clear_v1()
    user1 = src.auth.auth_register_v1("first@gmail.com", "password", "Maccas", "Mckenzie")
    invalid_u_id = -1
    
    with pytest.raises(InputError):
        dm_create_v1(user1[token], [invalid_u_id])

def test_dm_remove():
    pass

def test_dm_invite():
    pass

def test_dm_leave():
    pass

def test_dm_messages():
    pass

def test_dm_unauthorised_user():
    #* Test for unauthorised users for all dm functions
    removedUser = src.auth.auth_register_v1("removed@gmail.com", "password", "Yusuf", "Bideen")   
    src.other.clear_v1()
    user1 = src.auth.auth_register_v1("first@gmail.com", "password", "Hotel?", "Trivago")
    user2 = src.auth.auth_register_v1("second@gmail.com", "password", "Hotel?", "Trivago")
    dm1 = dm_create_v1(user1[token], [user2[AuID]])

    with pytest.raises(AccessError):
        dm_details_v1(removedUser[token], dm1[dmID])
        dm_list_v1(removedUser[token])
        dm_create_v1(removedUser[token], [user1[AuID]])