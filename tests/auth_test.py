# File to test functions in src/auth.py
from src.error import AccessError, InputError
import pytest
from src.auth import auth_login_v2, auth_register_v2
import src.channel, src.channels
from src.other import clear_v1
from jwt import encode

SECRET = 'MENG'

def test_auth_login_valid():
    clear_v1()
    auth_register_v2("caricoleman@gmail.com", "1234567", "cari", "coleman")
    token = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

def test_auth_login_valid_multiple():
    clear_v1()
    auth_register_v2("caricoleman@gmail.com", "1234567", "cari", "coleman")
    token1 = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    auth_register_v2("ericamondy@gmail.com", "1234567", "erica", "mondy") 
    token2 = encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')

    assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token1, 'auth_user_id': 0,}  
    assert auth_login_v2("ericamondy@gmail.com", "1234567") == {'token': token2, 'auth_user_id': 1,}

def test_auth_login_valid_sessions():
    clear_v1()
    auth_register_v2("caricoleman@gmail.com", "1234567", "cari", "coleman")
    token1 = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')    
    token2 = encode({'session_id': 2, 'user_id': 0}, SECRET, algorithm='HS256')

    assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token1, 'auth_user_id': 0,}  
    assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token2, 'auth_user_id': 0,}

def test_auth_login_valid_multiple_sessions():
    clear_v1()
    auth_register_v2("caricoleman@gmail.com", "1234567", "cari", "coleman")
    token1 = encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
    token2 = encode({'session_id': 2, 'user_id': 0}, SECRET, algorithm='HS256')

    auth_register_v2("ericamondy@gmail.com", "1234567", "erica", "mondy") 
    token3 = encode({'session_id': 1, 'user_id': 1}, SECRET, algorithm='HS256')
    token4 = encode({'session_id': 2, 'user_id': 1}, SECRET, algorithm='HS256')

    assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token1, 'auth_user_id': 0,}  
    assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token2, 'auth_user_id': 0,}
    assert auth_login_v2("ericamondy@gmail.com", "1234567") == {'token': token3, 'auth_user_id': 1,}
    assert auth_login_v2("ericamondy@gmail.com", "1234567") == {'token': token4, 'auth_user_id': 1,}

def test_auth_login_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2("caricoleman@gmail.com", "1234567", "cari", "coleman")
        auth_login_v2("caricoleman.com", "1234567")

def test_auth_login_invalid_not_registered_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2("caricoleman@gmail.com", "1234567", "cari", "coleman")
        auth_login_v2("caricolema@gmail.com", "1234567") 
        auth_login_v2("ericamondy@gmail.com", "1234567")  

def test_auth_login_invalid_empty():
    clear_v1()
    with pytest.raises(InputError):        
        auth_login_v2("caricolema@gmail.com", "1234567") 

def test_auth_login_invalid_incorrect_password():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2("caricoleman@gmail.com", "1234567", "cari", "coleman")
        auth_login_v2("caricoleman@gmail.com", "12345")

def test_auth_register_valid():
    clear_v1()
    token = encode({'session_id': 0, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_register_v2("caricoleman@gmail.com", "1234567", "cari", "coleman") == {'token': token, 'auth_user_id': 0,}

def test_auth_register_valid_multiple():
    clear_v1()
    token1 = encode({'session_id': 0, 'user_id': 0}, SECRET, algorithm='HS256')
    token2 = encode({'session_id': 0, 'user_id': 1}, SECRET, algorithm='HS256')
    token3 = encode({'session_id': 0, 'user_id': 2}, SECRET, algorithm='HS256')
    token4 = encode({'session_id': 0, 'user_id': 3}, SECRET, algorithm='HS256')
    token5 = encode({'session_id': 0, 'user_id': 4}, SECRET, algorithm='HS256')
    
    assert auth_register_v2("caricoleman@gmail.com", "1234567", "cari", "coleman") == {'token': token1, 'auth_user_id': 0,}
    assert auth_register_v2("ericamondy@gmail.com", "1234567", "erica", "mondy") == {'token': token2, 'auth_user_id': 1,}
    assert auth_register_v2("hilarybently@gmail.com", "1234567", "hilary", "bently") == {'token': token3, 'auth_user_id': 2,}
    assert auth_register_v2("kentonwatkins@gmail.com", "1234567", "kenton", "watkins") == {'token': token4, 'auth_user_id': 3,}
    assert auth_register_v2("claudiamarley@gmail.com", "1234567", "claudia", "marley") == {'token': token5, 'auth_user_id': 4,}    

def test_auth_register_valid_same_name():
    clear_v1()
    token1 = encode({'session_id': 0, 'user_id': 0}, SECRET, algorithm='HS256')
    token2 = encode({'session_id': 0, 'user_id': 1}, SECRET, algorithm='HS256')
    
    assert auth_register_v2("caricoleman@gmail.com", "1234567", "cari", "coleman") == {'token': token1, 'auth_user_id': 0,}
    assert auth_register_v2("caricoleman@hotmail.com", "1234567", "cari", "coleman") == {'token': token2, 'auth_user_id': 1,}

def test_auth_register_valid_same_name_multiple():
    clear_v1()
    token1 = encode({'session_id': 0, 'user_id': 0}, SECRET, algorithm='HS256')
    token2 = encode({'session_id': 0, 'user_id': 1}, SECRET, algorithm='HS256')
    token3 = encode({'session_id': 0, 'user_id': 2}, SECRET, algorithm='HS256')
    token4 = encode({'session_id': 0, 'user_id': 3}, SECRET, algorithm='HS256')
    
    assert auth_register_v2("caricoleman@gmail.com", "1234567", "cari", "coleman") == {'token': token1, 'auth_user_id': 0,}
    assert auth_register_v2("caricoleman@hotmail.com", "1234567", "cari", "coleman") == {'token': token2, 'auth_user_id': 1,}
    assert auth_register_v2("caricoleman@yahoo.com", "1234567", "cari", "coleman") == {'token': token3, 'auth_user_id': 2,}
    assert auth_register_v2("caricoleman@bing.com", "1234567", "cari", "coleman") == {'token': token4, 'auth_user_id': 3,}

def test_auth_register_valid_front_capatilised():
    clear_v1()
    token = encode({'session_id': 0, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_register_v2("caricoleman@gmail.com", "1234567", "Cari", "Coleman") == {'token': token, 'auth_user_id': 0, }
    
def test_auth_register_valid_random_capatilised():
    clear_v1()
    token = encode({'session_id': 0, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_register_v2("caricoleman@gmail.com", "1234567", "CaRi", "coLemaN") == {'token': token, 'auth_user_id': 0, }

def test_auth_register_valid_whitespace():
    clear_v1()
    token = encode({'session_id': 0, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_register_v2("caricoleman@gmail.com", "1234567", " cari", "coleman ") == {'token': token, 'auth_user_id': 0, }

def test_auth_register_valid_at_symbol():
    clear_v1()
    token = encode({'session_id': 0, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_register_v2("caricoleman@gmail.com", "1234567", "cari@", "coleman") == {'token': token, 'auth_user_id': 0, }

def test_auth_register_valid_long_name():
    clear_v1()
    token = encode({'session_id': 0, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_register_v2("caricoleman@gmail.com", "1234567", "cariiiiiiiiiiiiiii", "coleman") == {'token': token, 'auth_user_id': 0,}
    
def test_auth_register_valid_long_first_name():
    clear_v1()
    token = encode({'session_id': 0, 'user_id': 0}, SECRET, algorithm='HS256')
    assert auth_register_v2("caricoleman@gmail.com", "1234567", "cariiiiiiiiiiiiiiiiiii", "coleman") == {'token': token, 'auth_user_id': 0,}

def test_auth_register_valid_long_name_multiple():
    clear_v1()
    token1 = encode({'session_id': 0, 'user_id': 0}, SECRET, algorithm='HS256')
    token2 = encode({'session_id': 0, 'user_id': 1}, SECRET, algorithm='HS256')
    
    assert auth_register_v2("caricoleman@gmail.com", "1234567", "cariiiiiiiiiiiiiii", "coleman") == {'token': token1, 'auth_user_id': 0, }
    assert auth_register_v2("caricoleman@hotmail.com", "1234567", "cariiiiiiiiiiiiiii", "coleman") == {'token': token2, 'auth_user_id': 1, }

def test_auth_register_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2("caricoleman.com", "1234567", "cari", "coleman") 
    
def test_auth_register_invalid_same_email():
    clear_v1()
    with pytest.raises(InputError):
        token = encode({'session_id': 0, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_register_v2("caricoleman@gmail.com", "1234567", "cari", "coleman") == {'token': token, 'auth_user_id': 0,}
        auth_register_v2("caricoleman@gmail.com", "1234567", "erica", "mondy")

def test_auth_register_invalid_password():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2("caricoleman@gmail.com", "1234", "cari", "coleman") 

def test_auth_register_invalid_long_first_name():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2("caricoleman@gmail.com", "1234567", "cariiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii", "coleman") 

def test_auth_register_invalid_long_last_name():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2("caricoleman@gmail.com", "1234567", "cari", "colemaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaan") 

def test_auth_register_invalid_no_first_name():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2("caricoleman@gmail.com", "1234567", "", "coleman") 

def test_auth_register_invalid_no_last_name():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2("caricoleman@gmail.com", "1234567", "cari", "") 
