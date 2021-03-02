# File to test functions in src/auth.py

import pytest
from src.auth import auth_login_v1, auth_register_v1
import src.channel, src.channels

def test_auth_login_valid():
    return_val = auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    assert auth_login_v1("caricoleman@gmail.com", "1234567") == "caricoleman"

def test_auth_login_valid_multiple():
    return_val1 = auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    return_val2 = auth_register_v1("ericamondy@gmail.com", "1234567", "erica", "mondy") 

    assert auth_login_v1("caricoleman@gmail.com", "1234567") == "caricoleman"  
    assert auth_login_v1("ericamondy@gmail.com", "1234567") == "ericamondy"

def test_auth_login_invalid_email():
    with pytest.raises(InputError):
    return_val = auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    auth_login_v1("caricoleman.com", "1234567")

def test_auth_login_invalid_not_registered_email():
    with pytest.raises(InputError):
    return_val = auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    auth_login_v1("caricolema@gmail.com", "1234567") 
    auth_login_v1("ericamondy@gmail.com", "1234567")  

def test_auth_login_invalid_incorrect_password():
    with pytest.raises(InputError):
    return_val = auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman")
    auth_login_v1("caricoleman@gmail.com", "12345")

def test_auth_register_valid():
    assert auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman") == "caricoleman"

def test_auth_register_valid_multiple():
    assert auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman") == "caricoleman"
    assert auth_register_v1("ericamondy@gmail.com", "1234567", "erica", "mondy") == "ericamondy"
    assert auth_register_v1("hilarybently@gmail.com", "1234567", "hilary", "bently") == "hilarybently"
    assert auth_register_v1("kentonwatkins@gmail.com", "1234567", "kenton", "watkins") == "kentonwatkins"
    assert auth_register_v1("caludiamarley@gmail.com", "1234567", "claudia", "marley") == "claudiamarley"    

def test_auth_register_valid_same_name():
    assert auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman") == "caricoleman"
    assert auth_register_v1("caricoleman@hotmail.com", "1234567", "cari", "coleman") == "caricoleman1"

def test_auth_register_valid_same_name_multiple():
    assert auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman") == "caricoleman"
    assert auth_register_v1("caricoleman@hotmail.com", "1234567", "cari", "coleman") == "caricoleman0"
    assert auth_register_v1("caricoleman@yahoo.com", "1234567", "cari", "coleman") == "caricoleman1"

def test_auth_register_valid_front_capatilised():
    assert auth_register_v1("caricoleman@gmail.com", "1234567", "Cari", "Coleman") == "caricoleman"
    
def test_auth_register_valid_random_capatilised():
    assert auth_register_v1("caricoleman@gmail.com", "1234567", "CaRi", "coLemaN") == "caricoleman"

def test_auth_register_valid_whitespace():
    assert auth_register_v1("caricoleman@gmail.com", "1234567", " cari", "coleman ") == "caricoleman"

def test_auth_register_valid_at_symbol():
    assert auth_register_v1("caricoleman@gmail.com", "1234567", "cari@", "coleman") == "caricoleman"

def test_auth_register_valid_long_name():
    assert auth_register_v1("caricoleman@gmail.com", "1234567", "cariiiiiiiiiiiiiii", "coleman") == "cariiiiiiiiiiiiiiico"

def test_auth_register_valid_long_name_multiple():
    assert auth_register_v1("caricoleman@gmail.com", "1234567", "cariiiiiiiiiiiiiii", "coleman") == "cariiiiiiiiiiiiiiico"
    assert auth_register_v1("caricoleman@hotmail.com", "1234567", "cariiiiiiiiiiiiiii", "coleman") == "cariiiiiiiiiiiiiiico0"

def test_auth_register_invalid_email():
    with pytest.raises(InputError):
    auth_register_v1("caricoleman.com", "1234567", "cari", "coleman") 
    
def test_auth_register_invalid_same_email():
    with pytest.raises(InputError):
    assert auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "coleman") == "caricoleman"
    auth_register_v1("caricoleman@yahoo.com", "1234567", "erica", "mondy")

def test_auth_register_invalid_password():
    with pytest.raises(InputError):
    auth_register_v1("caricoleman@gmail.com", "1234", "cari", "coleman") 

def test_auth_register_invalid_long_first_name():
    with pytest.raises(InputError):
    auth_register_v1("caricoleman@gmail.com", "1234567", "cariiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii", "coleman") 

def test_auth_register_invalid_long_last_name():
    with pytest.raises(InputError):
    auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "colemaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaan") 

def test_auth_register_invalid_no_first_name():
    with pytest.raises(InputError):
    auth_register_v1("caricoleman@gmail.com", "1234567", "", "coleman") 

def test_auth_register_invalid_no_last_name():
    with pytest.raises(InputError):
    auth_register_v1("caricoleman@gmail.com", "1234567", "cari", "") 

   
