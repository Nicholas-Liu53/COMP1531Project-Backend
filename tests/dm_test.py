import src.data
from src.dm import dm_details_v1, dm_list_v1, dm_create_v1, dm_remove_v1, dm_invite_v1, dm_leave_v1, dm_messages_v1
from src.error import AccessError, InputError

def test_dm_details():
    pass

def test_dm_list():
    pass

def test_dm_create():
    pass

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
