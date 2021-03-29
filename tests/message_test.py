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

#* Test send functions together with message/send/v2
#? Test if message_id increases correctly

def test_senddm_errors():
    src.other.clear_v1()
    user1 = src.auth.auth_register_v2("first@gmail.com", "password", "Steve", "Irwin")
    user2 = src.auth.auth_register_v2("second@gmail.com", "password", "Jonah", "from Tonga")
    user3 = src.auth.auth_register_v2("third@gmail.com", "password", "Rock", "Sand")
    dm1 = src.dm.dm_create_v1(user1[token], [user2[AuID]])
    
    with pytest.raises(AccessError):
        message_senddm_v1(user3[token], dm1[dmID], '')

    src.other.clear_v1()
    user1 = src.auth.auth_register_v2("first@gmail.com", "password", "Steve", "Irwin")
    invalid_dm_id = -1

    with pytest.raises(InputError):
        message_senddm_v1(user1[token], invalid_dm_id, '')

    src.other.clear_v1()
    message = ''
    for _ in range(1500):
        message += 'a'

    user1 = src.auth.auth_register_v2("first@gmail.com", "password", "Steve", "Irwin")
    user2 = src.auth.auth_register_v2("second@gmail.com", "password", "Jonah", "from Tonga")
    dm1 = src.dm.dm_create_v1(user1[token], [user2[AuID]])
    with pytest.raises(InputError):
        message_senddm_v1(user1[token], dm1[dmID], message)

def test_senddm_multiple():
    src.other.clear_v1()
    user1 = src.auth.auth_register_v2("first@gmail.com", "password", "Steve", "Irwin")
    user2 = src.auth.auth_register_v2("second@gmail.com", "password", "Jonah", "from Tonga")
    dm1 = src.dm.dm_create_v1(user1[token], [user2[AuID]])
    assert message_senddm_v1(user1[token], dm1[dmID], '') == {'message_id': 0}
    assert message_senddm_v1(user1[token], dm1[dmID], '') == {'message_id': 1}
    assert message_senddm_v1(user1[token], dm1[dmID], '') == {'message_id': 2}
    assert message_senddm_v1(user1[token], dm1[dmID], '') == {'message_id': 3}

def test_dm_unauthorised_user(invalid_token):
    #* All unauthorised user tests
    user1 = src.auth.auth_register_v2("first@gmail.com", "password", "Steve", "Irwin")
    user2 = src.auth.auth_register_v2("second@gmail.com", "password", "Jonah", "from Tonga")
    dm1 = src.dm.dm_create_v1(user1[token], [user2[AuID]])
    
    with pytest.raises(AccessError):
        message_senddm_v1(invalid_token, dm1[dmID], '')