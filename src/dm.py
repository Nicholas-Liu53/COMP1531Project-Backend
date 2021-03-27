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

    #First omit errors
    #Raise input error if dm_id is not valid DM number
    if dm_id < 0 or dm_id > len(src.data.dms):
        raise Exception("InputError")

    #AccessError when the user is not original DM creator
    auth_user_ID = decode(token)
    if (auth_user_ID != src.data.dms['creator_id']) is True:
        raise Exception("AccessError")

    #Now that errors are fixed, can remove the existing DM with dm_id
    #Loop through dm_list, once dm_id is found remove it
    for i in range(0, len(src.data.dms)):
        if DM_list[i]['dm_id'] == dm_id:
            del DM_list[i]

    return {}

#Ethan
def dm_invite_v1(token, dm_id, u_id):
#ASSUME: Do not need to add new user into dm_name

#Invites a user to an existing dm
#Dm's will be contained like channels in a list, with each dm being a dictionary

    #Raises Input Error when dm_id is not valid
    if dm_id < 0 or dm_id > len(dm_list):
        raise Exception("InputError")
    #Access error if auth user i.e token is not a member of dm
    error_present = True
    #Loop through dm list of token or auth user
    #If dm_id is found then change it to false
    result = dm_list_v1(token)
    for i in range(len(0,result)):
        if result[i] == dm_id:
            error_present = False

    if error_present = True:
        raise Exception("AccessError")

    #Now that errors are fixed, can invite user to DM
    #Append their Uid to list of allMems list in dm_id dictionary
    for items in range(0,len(src.data.dms)):
        #How to differentiate between the dm_id within the dictionary and the one we want?
        if src.data.dms[items]['dm_id'] = 'dm_id':
            src.data.dms[items]['all_members'].append(u_id)
    return {}

#Ethan
@app.route('/dm/leave/v1', methods = ['POST'])
def dm_leave_v1(token, dm_id):
#Given a DM ID, user is removed as a member of this DM

    #Raises InputError when dm_id is not valid
    if dm_id < 0 or dm_id > len(dm_list):
        raise Exception("InputError")

    # Access error if user is not a member of token
    error_present = True
    # Loop through dm list of token or auth user
    # If dm_id is found then change it to false
    result = dm_list_v1(token)
    for i in range(len(0, result)):
        if result[i] == dm_id:
            error_present = False

    if error_present = True:
        raise Exception("AccessError")

    #Now can remove user from DM with dm_id

    #Is auth user id same as user Id, if not how to CHANGE IT

    current_user = decode(token)
    #remove their Uid from list of allMems list in dm_id dictionary
    for items in range(0,len(src.data.dms)):
        #How to differentiate between the dm_id within the dictionary and the one we want?
        if src.data.dms[items]['dm_id'] = 'dm_id':
                for members in src.data.dms[items][['all_members']]:
                    #Is this too much nesting?
                    if src.data.dms[items]['all_members'][members] = current_user:
                        del src.data.dms[items]['all_members'][members]
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
    raise AccessError