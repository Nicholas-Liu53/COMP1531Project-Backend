import src.data
from src.error import AccessError, InputError
import src.auth
import jwt

SECRET = 'MENG'

AuID      = 'auth_user_id'
uID       = 'u_id'
cID       = 'channel_id'
creatorID = 'creator_id'
allMems   = 'all_members'
Name      = 'name'
fName     = 'name_first'
lName     = 'name_last'
chans     = 'channels'
handle    = 'handle_string'
dmID      = 'dm_id'
seshID    = 'session_id'

def dm_details_v1(token, dm_id):
    auth_user_id, _ = decode(token)
    dm_name, dmMembers = get_members(-1, dm_id)
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
    auth_user_id, _ = decode(token)
    output = []
    for dmDetails in src.data.dms:
        for memberD in dmDetails['all_members']:
            if auth_user_id == memberD['u_id']:
                dm = {}
                dm[dmID] = dmDetails[dmID]
                dm[Name] = dmDetails[Name]
                output.append(dm)
    
    return {
        'dms': output
    }
    

def dm_create_v1(token, u_ids):
    creator_id, _ = decode(token)

    if len(src.data.dms) == 0:
        dm_ID = 0
    else:
        dm_ID = src.data.dms[-1][dmID] + 1

    dmUsers = u_ids.append(creator_id)
    handles = []
    for user in dmUsers:
        userInfo = get_user(user)
        handles.append(userInfo[handle])
    handles.sort()
    dm_name = ', '.join(handles)

    src.data.users.append({
        dmID: dm_ID,
        Name: dm_name,
        creatorID: creator_id,
        'all_members': dmUsers,
    })

    return {
        'dm_id': dmID,
        'dm_name': dm_name
    }

#Ethan
def dm_remove_v1(token, dm_id):
#Remove an existing DM, can only be done by original creator of dm
#ASSUMPTION: Rest of dms retain same dm_ids when a dm is removed

    auth_user_ID, _ = decode(token)
    #First omit errors
    #Raise input error if dm_id is not valid DM number
    #If dm_id not contained in list
    #AccessError when the user is not original DM creator
    input_error = True

    for items in src.data.dms:
        #Loop for input errors:
        if dm_id == items['dm_id']:
            input_error = False
            if auth_user_ID != items['creator_id']:
                raise AccessError

    if input_error:
        raise input_error

    #Now that errors are fixed, can remove the existing DM with dm_id
    #Loop through dm_list, once dm_id is found remove it
    for objects in src.data.dms:
        if objects['dm_id'] == dm_id:
            del objects

    return {}

#Ethan
def dm_invite_v1(token, dm_id, u_id):
#ASSUME: Do not need to add new user into dm_name
#Invites a user to an existing dm

    #Check u_id
    get_user(u_id)
    auth_user_ID, _ = decode(token)
    #Raises Input Error when dm_id is not valid
    #Access error if auth user i.e token is not a member of dm
    input_error = True
        for items in src.data.dms:
            #Loop for input errors:
            if dm_id == items['dm_id']:
                input_error = False
                if auth_user_ID not in items['all_members']:
                    raise AccessError
                else:
                    items['all_members'].append(u_id)

        if input_error:

            raise input_error

    return {}


def dm_leave_v1(token, dm_id):
#Given a DM ID, user is removed as a member of this DM
    auth_user_ID, _ = decode(token)
    #Raises InputError when dm_id is not valid
    # Access error if auth_user is not a member of dm with dm_id
    input_error = True
        for items in src.data.dms:
            #Loop for input errors:
            if dm_id == items['dm_id']:
                input_error = False
                if auth_user_ID not in items['all_members']:
                    raise AccessError
                else:
                    items['all_members'].remove(auth_user_ID)

        if input_error:
            raise input_error
    return {}

def dm_messages_v1(token, dm_id, start):
    pass

def decode(token):
    payload = jwt.decode(token, SECRET, algorithms='HS256')
    auth_user_id, session_id = payload.get('session_id'), payload.get('user_id')
    check_session(auth_user_id, session_id)
    return auth_user_id, session_id

def check_session(auth_user_id, session_id):
    for user in src.data.users:
        if auth_user_id == user[uID]:
            if session_id in user[session_id]:
                return
    raise AccessError

def get_members(channel_id, dm_id):
    if dm_id == -1:
        for chanDetails in src.data.channels:
            if channel_id == chanDetails[cID]:
                return chanDetails[Name], chanDetails[allMems]
        raise InputError
    else:
        for dmDetails in src.data.dms:
            if dm_id == dmDetails[dmID]:
                return dmDetails[Name], dmDetails[allMems]
        raise InputError

def get_user(user_id):
    for user in src.data.users:
        if user_id == user[uID]:
            return {
                uID: user[uID],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_string': user['handle_string'],
            }
    raise InputError