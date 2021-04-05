from flask import Flask, request
import src.data
from src.error import AccessError, InputError
from src.other import decode, get_user, get_dm, message_count, get_user_from_handlestring, push_added_notifications, check_removed
import src.auth
import json
import jwt

APP = Flask(__name__)

AuID      = 'auth_user_id'
uID       = 'u_id'
cID       = 'channel_id'
creatorID = 'creator_id'
allMems   = 'all_members'
Name      = 'name'
dmName    = 'dm_name'
fName     = 'name_first'
lName     = 'name_last'
chans     = 'channels'
handle    = 'handle_str'
dmID      = 'dm_id'
seshID    = 'session_id'

def dm_details_v1(token, dm_id):
    '''
    Users that are part of a DM can view basic information about the DM

    Arguments:
        token (str): JWT containing { u_id, session_id }
        dm_id (int): dm_id of the DM that the authorised user is trying to access the DM's details

    Exceptions:
        InputError
            - Raised when the dm_id inputed is not valid

        AccessError
            - Raised when an invalid token is given
            - Raised when the authorised user is not a member of the DM corresponding to the dm_id

    Return Value:
        Returns a dictionary with key 'names' and 'members' when sucessful
    '''
    auth_user_id, _ = decode(token)
    dm_name, dmMembers = get_dm(dm_id)['name'], get_dm(dm_id)[allMems]
    if auth_user_id not in dmMembers:
        raise AccessError
    mOutput = []
    for user in dmMembers:
        mOutput.append(get_user(user))

    return {
        Name: dm_name,
        'members': mOutput,
    }

def dm_list_v1(token):
    '''
    Returns the list of DMs that the user is a member of

    Arguments:
        token (str): JWT containing { u_id, session_id }

    Exceptions:
        AccessError
            - Raised when an invalid token is given

    Return Value:
        Returns a dictionary with key 'dms' mapping to a list of DMs that the user is a member of
        Each DM is represented by a dictionary containing types { dm_id, name }
    '''
    data = json.load(open('data.json', 'r'))
    auth_user_id, _ = decode(token)
    output = []
    for dmDetails in data['dms']:
        if auth_user_id in dmDetails['all_members']:
            dm = {}
            dm[dmID] = dmDetails[dmID]
            dm[Name] = dmDetails[Name]
            output.append(dm)
    
    return {
        'dms': output
    }
    
def dm_create_v1(token, u_ids):
    '''
    Creates a DM with the creator and the users it is directed to
    The name of the DM is an alphabetically-sorted, comma-separated list of user handles

    Arguments:
        token  (str): JWT containing { u_id, session_id }
        u_ids (list): List of u_ids that the authoerised user is directing the DM to

    Exceptions:
        InputError
            - u_id inside the list of u_ids does not refer to a valid user

        AccessError
            - Raised when an invalid token is given

    Return Value:
        Returns a dictionary with key 'dm_id' and 'dm_name' when sucessful
    '''
    data = json.load(open('data.json', 'r'))
    creator_id, _ = decode(token)
    if len(data['dms']) == 0:
        dm_ID = 0
    else:
        dm_ID = data['dms'][-1][dmID] + 1

    dmUsers = [creator_id]
    for user_id in u_ids:
        dmUsers.append(user_id)

    handles = []
    for user in dmUsers:
        
        userInfo = get_user(user)
        handles.append(userInfo[handle])
    handles.sort()
    dm_name = ', '.join(handles)

    for user_id in u_ids:
        check_removed(user_id)

    data['dms'].append({
        dmID: dm_ID,
        Name: dm_name,
        creatorID: creator_id,
        'all_members': dmUsers,
    })

    with open('data.json', 'w') as FILE:
        json.dump(data, FILE)

    for user in u_ids:
        push_added_notifications(creator_id, user, -1, dm_ID)

    return {
        'dm_id': dm_ID,
        'dm_name': dm_name
    }


def dm_remove_v1(token, dm_id):
    '''
    Removes a DM created by user 

    Arguments:
        token (str): JWT containing { u_id, session_id }
        dm_id (int): dm_id of the DM that the authorised user is trying to access the DM's details

    Exceptions:
        Input Error
            - Raise when dm_id does not refer to a valid DM
        AccessError
            - Raised when the user is not original DM creator 

    Return Value:
        {}
    '''
    #ASSUMPTION: Rest of dms retain same dm_ids when a dm is removed
    auth_user_ID, _ = decode(token)
    input_error = True

    data = json.load(open('data.json', 'r'))
    for items in data['dms']:
        #Loop for input errors:
        if dm_id == items['dm_id']:
            input_error = False
            if auth_user_ID != items['creator_id']:
                raise AccessError

    if input_error:
        raise InputError

    #Now that errors are fixed, can remove the existing DM with dm_id
    #Loop through dm_list, once dm_id is found remove it
    for objects in data['dms']:
        if objects['dm_id'] == dm_id:
            data['dms'].remove(objects)

    with open('data.json', 'w') as FILE:
        json.dump(data, FILE)

    return {}

def dm_invite_v1(token, dm_id, u_id):
    '''
    Invites a user to join an existing dm
    Arguments:
        token (str): JWT containing { u_id, session_id }
        dm_id (int): dm_id of the DM that the authorised user is trying to access the DM's details
        u_id (int): user ID of the user that is being added to the DM

    Exceptions:
        Input Error
            - Raise when dm_id does not refer to a valid DM
            - Raise when u_id does not refer to existing user 
        AccessError
            - Raised when the authorised user is not a member of DM

    Return Value:
        {}
    '''
    data = json.load(open('data.json', 'r'))
    #ASSUME: Do not need to add new user into dm_name
    get_user(u_id)
    check_removed(u_id)
    auth_user_ID, _ = decode(token)
    input_error = True
    for items in data['dms']:
        #Loop for input errors:
        if dm_id == items['dm_id']:
            input_error = False
            if auth_user_ID not in items['all_members']:
                raise AccessError
            else:
                #If no errors found can add dm to list
                items['all_members'].append(u_id)
                with open('data.json', 'w') as FILE:
                    json.dump(data, FILE)
                push_added_notifications(auth_user_ID, u_id, -1, dm_id)

    if input_error:
        raise InputError

    return {}


def dm_leave_v1(token, dm_id):
    '''
    Current user to leave DM with dm_id 
    Arguments:
        token (str): JWT containing { u_id, session_id }
        dm_id (int): dm_id of the DM that the authorised user is trying to access the DM's details

    Exceptions:
        Input Error
            - Raise when dm_id does not refer to a valid DM
        AccessError
            - Raised when the authorised user is not a member of DM

    Return Value:
        {}
    '''

    auth_user_ID, _ = decode(token)
    input_error = True
    data = json.load(open('data.json', 'r'))
    for items in data['dms']:
        #Loop for input errors:
        if dm_id == items['dm_id']:
            input_error = False
            if auth_user_ID not in items['all_members']:
                raise AccessError
            else:
                #If error not found remove dm from list 
                items['all_members'].remove(auth_user_ID)

    if input_error:
        raise InputError

    with open('data.json', 'w') as FILE:
        json.dump(data, FILE)

    return {}

def dm_messages_v1(token, dm_id, start):
    '''
    Return up to 50 messages from a DM with dm_id between index "start" and "start + 50"
    The message with index 0 is the most recent message in the channel

    Arguments:
        token (str): JWT containing { u_id, session_id }
        dm_id (int): dm_id of the DM that the authorised user is trying to access the DM's messages

    Exceptions:
        InputError
            - Raised when the dm_id inputed is not valid
            = Raised when start is greater than the total number of messages in the DM

        AccessError
            - Raised when an invalid token is given
            - Raised when the authorised user is not a member of the DM corresponding to the dm_id

    Return Value:
        Returns a dictionary with key 'messages', 'start', and 'end'
        'messages' maps to a list of dictionary, where each dictionary contain types { message_id, u_id, message, time_created}
        'start' is the value of start passed into the function
        'end' is "start + 50" if there more messages that can be loaded, otherwise, -1 is returned in 'end'
    '''
    data = json.load(open('data.json', 'r'))

    auth_user_id, _ = decode(token)
    num_of_messages = message_count(-1, dm_id)

    dmMembers = get_dm(dm_id)[allMems]
    if auth_user_id not in dmMembers:
        raise AccessError
    
    # Input error 2:start is greater than the total number of messages in the channel
    if start > num_of_messages:
        raise InputError

    desired_end = start + 50
    if num_of_messages < desired_end:
        desired_end = -1

    messages = []
    for objects in data['messages_log']:
        if dm_id == objects['dm_id']:
            current_DM = objects.copy()
            del current_DM[cID]
            del current_DM['dm_id']
            messages.insert(0,current_DM)

    #Reverse list such that the we have the newest messages at the start and oldest at the end 
    reversed(messages)        

    #Take 50 messages from our start value
    #Chop off all the messages before our start value 
    for _ in range(start):
        messages.pop(0)
    
    while len(messages) > 50:
        messages.pop(-1)
    
    return {
        'messages': messages,
        'start': start,
        'end': desired_end,
    }
