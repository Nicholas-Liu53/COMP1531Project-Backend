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

@pytest.fixture
def invalid_token():
    return jwt.encode({'session_id': -1, 'user_id': -1}, SECRET, algorithm='HS256')

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

#Ethan
def test_dm_remove():

    #Assumption that when DM is removed other DM id's remain constant

    #Setup
    # * Ensure database is empty
    src.other.clear_v1()

    # Setup user_id
    userID1 = src.auth.auth_register_v1("1531@gmail.com", "123456", "Tom", "Zhang")
    userID2 = src.auth.auth_register_v1("comp@gmail.com", "456789", "Jack", "P")

    # Create public channel by user_id 1
    firstChannel = channels_create_v1(userID1[AuID], 'Yggdrasil', True)

    #send 2 DM's in this channel from user1 to user2, will have dm_id = 0 and 1
    requests.post(f"{url}"dm/create/v1", json = {
        '''
        PUT WHATEVER GOES IN DM DICTIONARY HERE 
        'dm_id' = 0
        '''
        })

    requests.post(f"{url}"dm / create / v1", json = {
        '''
        PUT WHATEVER GOES IN DM DICTIONARY HERE 
        'dm_id' = 1
        '''
        })

    #Testing

    #Test for InputError- when dm_id does not match up i.e if its -1 or 3
    with pytest.raises("InputError"):
        #Change token into the token of user1
        dm_remove_v1(token_user1, 3)
        dm_remove_v1(token_user1, -1)

    #Test for AccessError- when user is not original DM creator
    with pytest.raises("ExceptionError"):
        #Change token into token of user2 and some random number
        dm_remove_v1(token_user2, 2)
        dm_remove_v1(token_420, dm_id)

    #Success Test case
    #Remove first dm sent
    dm_remove_v1(token_user1,0)
    result = requests.get(f"{url}dm/list/v1")
    #Return list of dm's that user1 is a part of
    payload = result.json()
    #Assert that dm1 is not in there, it should now raise input error
    assert payload['MSG1'] == ["WHAT"]
    with pytest.raises("InputError"):
        #Change token into the token of user1
        dm_remove_v1(token_user1, 0)

    pass

#Ethan
def test_dm_invite():


    #Setup
    # * Ensure database is empty
    src.other.clear_v1()

    # Setup user_id
    userID1 = src.auth.auth_register_v1("1531@gmail.com", "123456", "Tom", "Zhang")
    userID2 = src.auth.auth_register_v1("comp@gmail.com", "456789", "Jack", "P")
    userID3 = src.auth.auth_register_v1("hello@gmail.com", "xyz", "Paul", "J")
    userID4 = src.auth.auth_register_v1("goodbye@gmail.com", "1231", "John", "S")

    # Create public channel by user_id 1
    firstChannel = channels_create_v1(userID1[AuID], 'Yggdrasil', True)

    #send 2 DM's in this channel from user1 to user2, will have dm_id = 0 and 1
    requests.post(f"{url}"dm/create/v1", json = {
        '''
        PUT WHATEVER GOES IN DM DICTIONARY HERE 
        'dm_id' = 0
        '''
        })

    requests.post(f"{url}"dm / create / v1", json = {
        '''
        PUT WHATEVER GOES IN DM DICTIONARY HERE 
        'dm_id' = 1
        '''
        })


    #Test for InputError- when dm_id does not refer to an existing dm
    with pytest.raises("InputError"):
        #From first user invite using invalid tokens
        dm_invite_v1(token_user1, 3, userID3)
        dm_invite_v1(token_user1, -1, userID3)

    #Test for AccessError- if authorised user is not a member of the DM
    #change auth_id to userID4 and try to invite 3
    with pytest.raises("AccessError"):
        dm_invite_v1(token_user4, 0, userID3)

    #Success Test case
    #Invite UserID3 to DM with DM_ID 1
    dm_invite_v1(token_user1, 1, userID3)

    '''QUESTION
        
        How to get list of DM's for user three, 
        how does it differentiate what list using JSON?
        is there a way to input parameters into flask 
    
    '''
    result = requests.get(f"{url}dm/list/v1")
    payload = result.json()
    # Assert that DM_list for userID3 has DM with dm_id 1 in it
    assert payload['MSG1'] == ["WHAT"]

    pass

#Ethan
def test_dm_leave():

    #Setup
    # * Ensure database is empty
    src.other.clear_v1()

    # Setup user_id
    userID1 = src.auth.auth_register_v1("1531@gmail.com", "123456", "Tom", "Zhang")
    userID2 = src.auth.auth_register_v1("comp@gmail.com", "456789", "Jack", "P")
    userID3 = src.auth.auth_register_v1("hello@gmail.com", "xyz", "Paul", "J")
    # Create public channel by user_id 1
    firstChannel = channels_create_v1(userID1[AuID], 'Yggdrasil', True)

    #send 2 DM's in this channel from user1 to user2, will have dm_id = 0 and 1
    requests.post(f"{url}"dm/create/v1", json = {
        '''
        PUT WHATEVER GOES IN DM DICTIONARY HERE 
        'dm_id' = 0
        '''
        })

    requests.post(f"{url}"dm / create / v1", json = {
        '''
        PUT WHATEVER GOES IN DM DICTIONARY HERE 
        'dm_id' = 1
        '''
        })


    #Test for InputError- when dm_id does not refer to an existing dm
    with pytest.raises("InputError"):
        #From first user invite using invalid tokens
        dm_leave_v1(token_user1, 3)
        dm_leave_v1(token_user1, -1)

    #Test for AccessError- if authorised user is not a member of the DM
    #change auth_id to userID3 and try to leave
    with pytest.raises("AccessError"):
        dm_leave_v1(token_user3, 0)

    #Success Test case
    dm_leave_v1(token_user1, 1)

    result = requests.get(f"{url}dm/list/v1")
    payload = result.json()
    #Assert that dm_1 list only has user2 and doesn't have user 1
    assert payload['MSG1'] == ["WHAT"]

    pass

def test_dm_messages():
    pass

def test_dm_unauthorised_user(invalid_token):
    #* Test for unauthorised users for all dm functions  
    src.other.clear_v1()
    user1 = src.auth.auth_register_v1("first@gmail.com", "password", "Hotel?", "Trivago")
    user2 = src.auth.auth_register_v1("second@gmail.com", "password", "Hotel?", "Trivago")
    dm1 = dm_create_v1(user1[token], [user2[AuID]])

    with pytest.raises(AccessError):
        dm_details_v1(invalid_token, dm1[dmID])
        dm_list_v1(invalid_token)
        dm_create_v1(invalid_token, [user1[AuID]])