# File to test functions in src/user.py
from src.error import AccessError, InputError
import pytest
from src.auth import auth_login_v2, auth_register_v2
import src.channel, src.channels
from src.other import clear_v1
from jwt import encode

SECRET = 'meng'
'''
def test_user_profile_valid():
    clear_v1()
    auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

    assert user_profile_v2(token, 0) == {
        'u_id': 0, 
        'email': "caricoleman@gmail.com", 
        'first name': 'cari', 
        'last name': 'coleman', 
        'handle': 'caricoleman'
        }

def test_user_profile_valid_multiple():
    clear_v1()
    auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    token1 = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token1, 'auth_user_id': 0,}

    auth_register_v1("ericamondy@gmail.com", "1234567", "erica", "mondy") 
    token2 = encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')
    assert auth_login_v1("ericamondy@gmail.com", "1234567") == {'token': token2, 'auth_user_id': 1,}


    assert user_profile_v2(token1, 0) == {
        'u_id': 0, 
        'email': "caricoleman@gmail.com", 
        'first name': 'cari', 
        'last name': 'coleman', 
        'handle': 'caricoleman'
        }

    assert user_profile_v2(token2, 0) == {
        'u_id': 1, 
        'email': "ericamondy@gmail.com", 
        'first name': 'erica', 
        'last name': 'mondy', 
        'handle': 'ericamondy'
    }    

def test_user_profile_invalid_user_id():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
        token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}
        user_profile_v2(token, 1)

def test_user_setname_valid_first_name():
    clear_v1()
    auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

    assert user_setname_v2(token, 'kari', 'coleman') == {}

    assert  user_profile_v2(token, 0) == {
        'u_id': 0, 
        'email': "caricoleman@gmail.com", 
        'first name': 'kari', 
        'last name': 'coleman', 
        'handle': 'caricoleman'
    }

def test_user_setname_valid_last_name():
    clear_v1()
    auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

    assert user_setname_v2(token, 'cari', 'koleman') == {}

    assert  user_profile_v2(token, 0) == {
        'u_id': 0, 
        'email': "caricoleman@gmail.com", 
        'first name': 'cari', 
        'last name': 'koleman', 
        'handle': 'caricoleman'
    }

def test_user_setname_valid_both_names():
    clear_v1()
    auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

    assert user_setname_v2(token, 'kari', 'koleman') == {}

    assert  user_profile_v2(token, 0) == {
        'u_id': 0, 
        'email': "caricoleman@gmail.com", 
        'first name': 'kari', 
        'last name': 'koleman', 
        'handle': 'caricoleman'
    }

def test_user_setname_valid_multiple():
    clear_v1()
    auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    token1 = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token1, 'auth_user_id': 0,}

    auth_register_v1("ericamondy@gmail.com", "1234567", "erica", "mondy") 
    token2 = encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')
    assert auth_login_v1("ericamondy@gmail.com", "1234567") == {'token': token2, 'auth_user_id': 1,}


    assert user_setname_v2(token1, 'kari', 'koleman') == {}

    assert  user_profile_v2(token1, 0) == {
        'u_id': 0, 
        'email': "caricoleman@gmail.com", 
        'first name': 'kari', 
        'last name': 'koleman', 
        'handle': 'caricoleman'
    }
    
    assert user_setname_v2(token2, 'erika', 'money') == {}

    assert  user_profile_v2(token2, 1) == {
        'u_id': 1, 
        'email': "ericamondy@gmail.com", 
        'first name': 'erika', 
        'last name': 'money', 
        'handle': 'ericamondy'
    }

def test_user_setname_invalid_long_first_name():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
        token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

        user_setname_v2(token, 'kariiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii', 'koleman') 

def test_user_setname_invalid_no_first_name():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
        token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

        user_setname_v2(token, '', 'koleman') 

def test_user_setname_invalid_long_last_name():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
        token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

        user_setname_v2(token, 'kari', 'kolemaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaan')           

def test_user_setname_invalid_no_last_name():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
        token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

        user_setname_v2(token, 'kari', '') 

def test_user_setemail_valid():
    clear_v1()
    auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

    assert user_setemail_v2(token, 'karicoleman@gmail.com')

    assert user_profile_v2(token, 0) == {
        'u_id': 0, 
        'email': "karicoleman@gmail.com", 
        'first name': 'cari', 
        'last name': 'coleman', 
        'handle': 'caricoleman'
        }

def test_user_setname_valid_multiple():
    clear_v1()
    auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    token1 = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token1, 'auth_user_id': 0,}

    auth_register_v1("ericamondy@gmail.com", "1234567", "erica", "mondy") 
    token2 = encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')
    assert auth_login_v1("ericamondy@gmail.com", "1234567") == {'token': token2, 'auth_user_id': 1,}


    assert user_setemail_v2(token1, 'karicoleman@gmail.com') == {}

    assert  user_profile_v2(token1, 0) == {
        'u_id': 0, 
        'email': "karicoleman@gmail.com", 
        'first name': 'cari', 
        'last name': 'coleman', 
        'handle': 'caricoleman'
    }
    
    assert user_setname_v2(token2, 'erikamoney@gmail.com') == {}

    assert  user_profile_v2(token2, 1) == {
        'u_id': 1, 
        'email': "erikamoney@gmail.com", 
        'first name': 'erica', 
        'last name': 'mondy', 
        'handle': 'ericamondy'
    }

def test_user_setemail_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
        token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

        user_setemail_v2(token, 'karicoleman.com')

def test_user_setemail_invalid_email_in_use():
    clear_v1()
    auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    token1 = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token1, 'auth_user_id': 0,}

    auth_register_v1("ericamondy@gmail.com", "1234567", "erica", "mondy") 
    token2 = encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')
    assert auth_login_v1("ericamondy@gmail.com", "1234567") == {'token': token2, 'auth_user_id': 1,}


    assert user_setemail_v2(token1, 'karicoleman@gmail.com') == {}

    assert  user_profile_v2(token1, 0) == {
        'u_id': 0, 
        'email': "karicoleman@gmail.com", 
        'first name': 'cari', 
        'last name': 'coleman', 
        'handle': 'caricoleman'
    }
    
    user_setname_v2(token2, 'karicoleman@gmail.com') 

def test_user_sethandle_valid():
    clear_v1()
    auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

    assert user_sethandle_v2(token, 'karikoleman')

    assert user_profile_v2(token, 0) == {
        'u_id': 0, 
        'email': "caricoleman@gmail.com", 
        'first name': 'cari', 
        'last name': 'coleman', 
        'handle': 'karikoleman'
        }

def test_user_sethandle_valid_multiple():
    clear_v1()
    auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    token1 = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token1, 'auth_user_id': 0,}

    auth_register_v1("ericamondy@gmail.com", "1234567", "erica", "mondy") 
    token2 = encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')
    assert auth_login_v1("ericamondy@gmail.com", "1234567") == {'token': token2, 'auth_user_id': 1,}


    assert user_sethandle_v2(token1, 'karikoleman') == {}

    assert  user_profile_v2(token1, 0) == {
        'u_id': 0, 
        'email': "caricoleman@gmail.com", 
        'first name': 'cari', 
        'last name': 'coleman', 
        'handle': 'karikoleman'
    }
    
    assert user_sethandle_v2(token2, 'erikamoney') == {}

    assert  user_profile_v2(token2, 1) == {
        'u_id': 1, 
        'email': "ericamondy@gmail.com", 
        'first name': 'erica', 
        'last name': 'mondy', 
        'handle': 'erikamoney'
    }

def test_user_sethandle_invalid_short_handle():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
        token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

        user_sethandle_v2(token, 'cc')

def test_user_sethandle_invalid_long_handle():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
        token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

        user_sethandle_v2(token, 'cariiiiiiiiiiiiiiiiii')

def test_user_sethandle_invalid_handle_in_use():
    clear_v1()
    auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    token1 = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token1, 'auth_user_id': 0,}

    auth_register_v1("ericamondy@gmail.com", "1234567", "erica", "mondy") 
    token2 = encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')
    assert auth_login_v1("ericamondy@gmail.com", "1234567") == {'token': token2, 'auth_user_id': 1,}


    assert user_sethandle_v2(token1, 'kari') == {}

    assert  user_profile_v2(token1, 0) == {
        'u_id': 0, 
        'email': "karicoleman@gmail.com", 
        'first name': 'cari', 
        'last name': 'coleman', 
        'handle': 'kari'
    }
    
    user_setname_v2(token2, 'kari') 

def test_users_all_v1_one():
    clear_v1()
    auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

    assert users_all(token) == [
        {
        'u_id': 0, 
        'email': "caricoleman@gmail.com", 
        'first name': 'cari', 
        'last name': 'coleman', 
        'handle': 'caricoleman'
        }
    ]

def test_users_all_v1_two():
    clear_v1()
    auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    token1 = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token1, 'auth_user_id': 0,}

    auth_register_v1("ericamondy@gmail.com", "1234567", "erica", "mondy") 
    token2 = encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')
    assert auth_login_v1("ericamondy@gmail.com", "1234567") == {'token': token2, 'auth_user_id': 1,}

    assert users_all(token1) == [
        {
        'u_id': 0, 
        'email': "caricoleman@gmail.com", 
        'first name': 'cari', 
        'last name': 'coleman', 
        'handle': 'caricoleman'
        },
        {
        'u_id': 1, 
        'email': "ericamondy@gmail.com", 
        'first name': 'erica', 
        'last name': 'mondy', 
        'handle': 'ericamondy'
        }
    ]

def test_users_all_v1_multiple():
    clear_v1()
    auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    token1 = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v1("caricoleman@gmail.com", "1234567") == {'token': token1, 'auth_user_id': 0,}

    auth_register_v1("ericamondy@gmail.com", "1234567", "erica", "mondy") 
    token2 = encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')
    assert auth_login_v1("ericamondy@gmail.com", "1234567") == {'token': token2, 'auth_user_id': 1,}

    auth_register_v1("hilarybently@gmail.com", "1234567", "hillary", "bently") 
    token3 = encode({'session_id': 1, 'user_id': 2}, SECRET, algorithm='HS256')
    assert auth_login_v1("hilarybently@gmail.com", "1234567") == {'token': token3, 'auth_user_id': 2,}

    auth_register_v1("kentonwatkins@gmail.com", "1234567", "kenton", "watkins") 
    token4 = encode({'session_id': 1, 'user_id': 3}, SECRET, algorithm='HS256')
    assert auth_login_v1("kentonwatkins@gmail.com", "1234567") == {'token': token4, 'auth_user_id': 3,}

    auth_register_v1("claudiamarley@gmail.com", "1234567", "claudia", "marley") 
    token5 = encode({'session_id': 1, 'user_id': 4}, SECRET, algorithm='HS256')
    assert auth_login_v1("caludiamarley@gmail.com", "1234567") == {'token': token5, 'auth_user_id': 4,}

    assert users_all(token1) == [
        {
        'u_id': 0, 
        'email': "caricoleman@gmail.com", 
        'first name': 'cari', 
        'last name': 'coleman', 
        'handle': 'caricoleman'
        },
        {
        'u_id': 1, 
        'email': "ericamondy@gmail.com", 
        'first name': 'erica', 
        'last name': 'mondy', 
        'handle': 'ericamondy'
        },
        {
        'u_id': 2, 
        'email': "hilarybently@gmail.com", 
        'first name': 'hillary', 
        'last name': 'bentley', 
        'handle': 'hillarybentley'
        },
        {
        'u_id': 3, 
        'email': "kentonwatkins@gmail.com", 
        'first name': 'kenton', 
        'last name': 'watkins', 
        'handle': 'kentonwatkins'
        },
        {
        'u_id': 4, 
        'email': "claudiamarley@gmail.com", 
        'first name': 'claudia', 
        'last name': 'marley', 
        'handle': 'claudiamarley'
        },
    ]
'''
