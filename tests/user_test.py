# File to test functions in src/user.py
from src.error import AccessError, InputError
import pytest
from src.user import user_profile_v2, user_setname_v2, user_setemail_v2, user_sethandle_v2, users_all
from src.auth import auth_register_v2, auth_login_v2
from src.other import clear_v1, SECRET
import jwt


@pytest.fixture
def invalid_token():
    return jwt.encode({'session_id': -1, 'user_id': -1}, SECRET, algorithm='HS256')

@pytest.fixture
def user1():
    clear_v1()    
    return auth_register_v2("caricoleman@gmail.com", "1234567", "cari", "coleman")

@pytest.fixture
def user2():
    return auth_register_v2("ericamondy@gmail.com", "1234567", "erica", "mondy")

@pytest.fixture
def user3():
    return auth_register_v2("hilarybently@gmail.com", "1234567", "hillary", "bently") 

@pytest.fixture
def user4():
    return auth_register_v2("kentonwatkins@gmail.com", "1234567", "kenton", "watkins") 

@pytest.fixture
def user5():
    return auth_register_v2("claudiamarley@gmail.com", "1234567", "claudia", "marley")

def test_user_profile_valid(user1,user2):
    token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

    assert user_profile_v2(token, 0) == { 
        'user':
            {
            'u_id': 0, 
            'email': "caricoleman@gmail.com", 
            'name_first': 'cari', 
            'name_last': 'coleman', 
            'handle_str': 'caricoleman'
            }
    }

def test_user_profile_valid_multiple(user1,user2):

    token1 = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token1, 'auth_user_id': 0,}

    token2 = jwt.encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')
    assert auth_login_v2("ericamondy@gmail.com", "1234567") == {'token': token2, 'auth_user_id': 1,}


    assert user_profile_v2(token1, 0) == { 
        'user':
            {
            'u_id': 0, 
            'email': "caricoleman@gmail.com", 
            'name_first': 'cari', 
            'name_last': 'coleman', 
            'handle_str': 'caricoleman'
            }
    }

    assert user_profile_v2(token2, 1) == { 
        'user':
            {
            'u_id': 1, 
            'email': "ericamondy@gmail.com", 
            'name_first': 'erica', 
            'name_last': 'mondy', 
            'handle_str': 'ericamondy'
            }
    }
    

def test_user_profile_invalid_user_id(user1):
    with pytest.raises(InputError):
        token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}
        user_profile_v2(token, 1)

def test_user_setname_valid_first_name(user1):
    token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

    assert user_setname_v2(token, 'kari', 'coleman') == {}

    assert  user_profile_v2(token, 0) == { 
        'user':
            {
            'u_id': 0, 
            'email': "caricoleman@gmail.com", 
            'name_first': 'kari', 
            'name_last': 'coleman', 
            'handle_str': 'caricoleman'
            }
    }

def test_user_setname_valid_last_name(user1):
    token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

    assert user_setname_v2(token, 'cari', 'koleman') == {}

    assert  user_profile_v2(token, 0) == { 
        'user':
            {
            'u_id': 0, 
            'email': "caricoleman@gmail.com", 
            'name_first': 'cari', 
            'name_last': 'koleman', 
            'handle_str': 'caricoleman'
            }
    }

def test_user_setname_valid_both_names(user1):
    token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

    assert user_setname_v2(token, 'kari', 'koleman') == {}

    assert  user_profile_v2(token, 0) == { 
        'user':
            {
            'u_id': 0, 
            'email': "caricoleman@gmail.com", 
            'name_first': 'kari', 
            'name_last': 'koleman', 
            'handle_str': 'caricoleman'
            }
    }

def test_user_setname_valid_multiple(user1,user2):
    token1 = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token1, 'auth_user_id': 0,}
 
    token2 = jwt.encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')
    assert auth_login_v2("ericamondy@gmail.com", "1234567") == {'token': token2, 'auth_user_id': 1,}


    assert user_setname_v2(token1, 'kari', 'koleman') == {}

    assert  user_profile_v2(token1, 0) == {
        'user':
        {
        'u_id': 0, 
        'email': "caricoleman@gmail.com", 
        'name_first': 'kari', 
        'name_last': 'koleman', 
        'handle_str': 'caricoleman'
        }
    }
    
    assert user_setname_v2(token2, 'erika', 'money') == {}

    assert  user_profile_v2(token2, 1) == {
        'user':
        {
        'u_id': 1, 
        'email': "ericamondy@gmail.com", 
        'name_first': 'erika', 
        'name_last': 'money', 
        'handle_str': 'ericamondy'
        }
    }

def test_user_setname_invalid_long_first_name(user1):
    with pytest.raises(InputError):
        token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

        user_setname_v2(token, 'kariiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii', 'koleman') 

def test_user_setname_invalid_no_first_name(user1):
    with pytest.raises(InputError):
        token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

        user_setname_v2(token, '', 'koleman') 

def test_user_setname_invalid_long_last_name(user1):
    with pytest.raises(InputError):
        token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}
        user_setname_v2(token, 'kari', 'kolemaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaan')           

def test_user_setname_invalid_no_last_name(user1):
    with pytest.raises(InputError):
        token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

        user_setname_v2(token, 'kari', '') 

def test_user_setemail_valid(user1):
    token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

    assert user_setemail_v2(token, 'karicoleman@gmail.com') == {}

    assert user_profile_v2(token, 0) == {
        'user':
        {
        'u_id': 0, 
        'email': "karicoleman@gmail.com", 
        'name_first': 'cari', 
        'name_last': 'coleman', 
        'handle_str': 'caricoleman'
        }
    }

def test_user_setemail_valid_multiple(user1,user2):
    token1 = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token1, 'auth_user_id': 0,}

    token2 = jwt.encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')
    assert auth_login_v2("ericamondy@gmail.com", "1234567") == {'token': token2, 'auth_user_id': 1,}


    assert user_setemail_v2(token1, 'karicoleman@gmail.com') == {}

    assert  user_profile_v2(token1, 0) == {
        'user':
        {
        'u_id': 0, 
        'email': "karicoleman@gmail.com", 
        'name_first': 'cari', 
        'name_last': 'coleman', 
        'handle_str': 'caricoleman'
        }
    }
    
    assert user_setemail_v2(token2, 'erikamoney@gmail.com') == {}

    assert  user_profile_v2(token2, 1) == {
        'user':
        {
        'u_id': 1, 
        'email': "erikamoney@gmail.com", 
        'name_first': 'erica', 
        'name_last': 'mondy', 
        'handle_str': 'ericamondy'
        }
    }

def test_user_setemail_invalid_email(user1):
    with pytest.raises(InputError):
        token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

        user_setemail_v2(token, 'karicoleman.com')

def test_user_setemail_invalid_email_in_use(user1,user2):
    with pytest.raises(InputError):
        token1 = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token1, 'auth_user_id': 0,}

        token2 = jwt.encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')
        assert auth_login_v2("ericamondy@gmail.com", "1234567") == {'token': token2, 'auth_user_id': 1,}


        assert user_setemail_v2(token1, 'karicoleman@gmail.com') == {}

        assert  user_profile_v2(token1, 0) == {
            'user':
            {
            'u_id': 0, 
            'email': "karicoleman@gmail.com", 
            'name_first': 'cari', 
            'name_last': 'coleman', 
            'handle_str': 'caricoleman'
            }
        }
        
        user_setemail_v2(token2, 'karicoleman@gmail.com') 

def test_user_sethandle_valid(user1):
    token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

    assert user_sethandle_v2(token, 'karikoleman') == {}

    assert user_profile_v2(token, 0) == {
        'user':
        {
        'u_id': 0, 
        'email': "caricoleman@gmail.com", 
        'name_first': 'cari', 
        'name_last': 'coleman', 
        'handle_str': 'karikoleman'
        }
    }

def test_user_sethandle_valid_multiple(user1,user2):
    token1 = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token1, 'auth_user_id': 0,}

    token2 = jwt.encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')
    assert auth_login_v2("ericamondy@gmail.com", "1234567") == {'token': token2, 'auth_user_id': 1,}


    assert user_sethandle_v2(token1, 'karikoleman') == {}

    assert  user_profile_v2(token1, 0) == {
        'user':
        {
        'u_id': 0, 
        'email': "caricoleman@gmail.com", 
        'name_first': 'cari', 
        'name_last': 'coleman', 
        'handle_str': 'karikoleman'
        }
    }
    
    assert user_sethandle_v2(token2, 'erikamoney') == {}

    assert  user_profile_v2(token2, 1) == {
        'user':
        {
        'u_id': 1, 
        'email': "ericamondy@gmail.com", 
        'name_first': 'erica', 
        'name_last': 'mondy', 
        'handle_str': 'erikamoney'
        }
    }

def test_user_sethandle_invalid_short_handle(user1):
    with pytest.raises(InputError):
        token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

        user_sethandle_v2(token, 'cc')

def test_user_sethandle_invalid_long_handle(user1):
    with pytest.raises(InputError):
        token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

        user_sethandle_v2(token, 'cariiiiiiiiiiiiiiiiii')

def test_user_sethandle_invalid_handle_in_use(user1,user2):
    with pytest.raises(InputError):
        token1 = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token1, 'auth_user_id': 0,}

        token2 = jwt.encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')
        assert auth_login_v2("ericamondy@gmail.com", "1234567") == {'token': token2, 'auth_user_id': 1,}


        assert user_sethandle_v2(token1, 'kari') == {}

        assert  user_profile_v2(token1, 0) == {
            'user':
            {
            'u_id': 0, 
            'email': "caricoleman@gmail.com", 
            'name_first': 'cari', 
            'name_last': 'coleman', 
            'handle_str': 'kari'
            }
        }
        
        user_sethandle_v2(token2, 'kari') 

def test_users_all_v1_one(user1):
    token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

    assert users_all(token) == {
            'users':
            [{
            'u_id': 0, 
            'email': "caricoleman@gmail.com", 
            'name_first': 'cari', 
            'name_last': 'coleman', 
            'handle_str': 'caricoleman'
            }]
    }


def test_users_all_v1_two(user1,user2):
    token1 = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token1, 'auth_user_id': 0,}

    token2 = jwt.encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')
    assert auth_login_v2("ericamondy@gmail.com", "1234567") == {'token': token2, 'auth_user_id': 1,}

    assert users_all(token1) == {
            'users':
            [{
            'u_id': 0, 
            'email': "caricoleman@gmail.com", 
            'name_first': 'cari', 
            'name_last': 'coleman', 
            'handle_str': 'caricoleman'
            },
            {
            'u_id': 1, 
            'email': "ericamondy@gmail.com", 
            'name_first': 'erica', 
            'name_last': 'mondy', 
            'handle_str': 'ericamondy'
            }]
    } 
    

def test_users_all_v1_multiple(user1, user2, user3, user4, user5):
    token1 = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token1, 'auth_user_id': 0,}

    token2 = jwt.encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')
    assert auth_login_v2("ericamondy@gmail.com", "1234567") == {'token': token2, 'auth_user_id': 1,}

    token3 = jwt.encode({'session_id': 1, 'user_id': 2}, SECRET, algorithm='HS256')
    assert auth_login_v2("hilarybently@gmail.com", "1234567") == {'token': token3, 'auth_user_id': 2,}
 
    token4 = jwt.encode({'session_id': 1, 'user_id': 3}, SECRET, algorithm='HS256')
    assert auth_login_v2("kentonwatkins@gmail.com", "1234567") == {'token': token4, 'auth_user_id': 3,}
 
    token5 = jwt.encode({'session_id': 1, 'user_id': 4}, SECRET, algorithm='HS256')
    assert auth_login_v2("claudiamarley@gmail.com", "1234567") == {'token': token5, 'auth_user_id': 4,}

    assert users_all(token1) == {   
            'users':
            [{
            'u_id': 0, 
            'email': "caricoleman@gmail.com", 
            'name_first': 'cari', 
            'name_last': 'coleman', 
            'handle_str': 'caricoleman'
            },
            {
            'u_id': 1, 
            'email': "ericamondy@gmail.com", 
            'name_first': 'erica', 
            'name_last': 'mondy', 
            'handle_str': 'ericamondy'
            },
            {
            'u_id': 2, 
            'email': "hilarybently@gmail.com", 
            'name_first': 'hillary', 
            'name_last': 'bently', 
            'handle_str': 'hillarybently'
            },
            {
            'u_id': 3, 
            'email': "kentonwatkins@gmail.com", 
            'name_first': 'kenton', 
            'name_last': 'watkins', 
            'handle_str': 'kentonwatkins'
            },
            {
            'u_id': 4, 
            'email': "claudiamarley@gmail.com", 
            'name_first': 'claudia', 
            'name_last': 'marley', 
            'handle_str': 'claudiamarley'
            },]
        } 
    

