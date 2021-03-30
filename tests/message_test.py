import pytest
from src.message import message_send_v1, message_remove_v1, message_edit_v1, message_senddm_v1
from src.error import InputError, AccessError
import src.channel, src.channels, src.auth, src.dm
import jwt
from src.other import SECRET

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