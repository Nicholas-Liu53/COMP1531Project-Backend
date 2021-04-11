# File to test functions in src/user.py
from src.error import AccessError, InputError
import pytest
from src.user import user_profile_v2, user_setname_v2, user_setemail_v2, user_sethandle_v2, users_all
from src.auth import auth_register_v2, auth_login_v2
from src.other import clear_v1, SECRET
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.dm import dm_create_v1
from src.message import message_send_v1
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

# tests the return value when user profile is called from a valid user 
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

# tests the return value when user profile is called from a valid user by multiple users
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
    

# tests the case when the provided token contains an invalid user id
def test_user_profile_invalid_user_id(user1):
    with pytest.raises(InputError):
        token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}
        user_profile_v2(token, 1)

# tests that set name changes the users first and last names to the inputted first and last names
# where only the first name is being changed
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

# tests that set name changes the users first and last names to the inputted first and last names 
# where only the last name is being changed
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

# tests that set name changes the users first and last names to the inputted first and last names 
# where both the first and last names are being changed
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

# tests that set name changes the users first and last names to the inputted first and last names 
# where both the first and last names are being changed
# for multiple users
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

# tests for the case where the inputted first name exceeds the 50 character limit
def test_user_setname_invalid_long_first_name(user1):
    with pytest.raises(InputError):
        token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

        user_setname_v2(token, 'kariiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii', 'koleman') 

# tests for the case where the inputted first name is empty
def test_user_setname_invalid_no_first_name(user1):
    with pytest.raises(InputError):
        token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

        user_setname_v2(token, '', 'koleman') 

# tests for the case where the inputted last name exceeds the 50 character limit
def test_user_setname_invalid_long_last_name(user1):
    with pytest.raises(InputError):
        token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}
        user_setname_v2(token, 'kari', 'kolemaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaan')           

# tests for the case where the inputted last name is empty
def test_user_setname_invalid_no_last_name(user1):
    with pytest.raises(InputError):
        token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

        user_setname_v2(token, 'kari', '') 

# tests that set email changes the users email to the inputted email
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

# tests that set email changes the users email to the inputted email for multiple users
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

# tests the case where the inputted email is of invalid format
def test_user_setemail_invalid_email(user1):
    with pytest.raises(InputError):
        token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

        user_setemail_v2(token, 'karicoleman.com')

# tests the case where the inputted email is already being used by another registerd user
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

# tests that set handle changes the users handle string to the inputted handle string
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

# tests that set handle changes the users handle string to the inputted handle string for multiple users
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

# tests for the case when the inputted handle string has less than 3 characters
def test_user_sethandle_invalid_short_handle(user1):
    with pytest.raises(InputError):
        token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

        user_sethandle_v2(token, 'cc')

# tests for the case when the inputted handle string exceeds the 20 character limit
def test_user_sethandle_invalid_long_handle(user1):
    with pytest.raises(InputError):
        token = jwt.encode({'session_id': 1, 'user_id': 0}, SECRET, algorithm='HS256')
        assert auth_login_v2("caricoleman@gmail.com", "1234567") == {'token': token, 'auth_user_id': 0,}

        user_sethandle_v2(token, 'cariiiiiiiiiiiiiiiiii')

# tests for the case when the inputted handle string is already being used by another user
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

# tests the return value of users_all for when only one user is registered
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

# tests the return value of users_all for when two users are registered
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
    
# tests the return value of users_all for when multiple users are registered
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
    
def test_users_stats_v1(user1, user2):
    channel1 = channels_create_v1(user1['token'], 'Channel1', True)
    dm_create_v1(user1['token'], user2['u_id'])
    message_send_v1(user1['token'], channel1['channel_id', "Heyyyy"])

    output1 = users_stats_v1(user1['token'])

    assert len(output1['dreams_analytics']['num_channels_exists']) == 1
    assert len(output1['dreams_analytics']['num_dms_exist']) == 1
    assert len(output1['dreams_analytics']['num_messages_exist']) == 1
    assert output1['dreams_analytics']['utilization_rate'] == 0

    channel_join_v1(user2[tok], channel1[cID])
    channel2 = channels_create_v1(user1['token'], 'Channel2', True)
    dm_create_v1(user1['token'], user2['u_id'])
    message_send_v1(user1['token'], channel1['channel_id', "Yo wassup"])

    output2 = users_stats_v1(user1['token'])

    assert len(output2['dreams_analytics']['num_channels_exists']) == 2
    assert len(output2['dreams_analytics']['num_dms_exist']) == 2
    assert len(output2['dreams_analytics']['num_messages_exist']) == 2
    assert output2['dreams_analytics']['utilization_rate'] == 0.5

    channel_join_v1(user1[tok], channel2[cID])

    output3 = users_stats_v1(user1['token'])

    assert len(output3['dreams_analytics']['num_channels_exists']) == 2
    assert len(output3['dreams_analytics']['num_dms_exist']) == 2
    assert len(output3['dreams_analytics']['num_messages_exist']) == 2
    assert output3['dreams_analytics']['utilization_rate'] == 1










