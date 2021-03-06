import src.data
from src.error import AccessError, InputError

AuID    = 'auth_user_id'
uID     = 'user_id'
cID     = 'channel_id'
allMems = 'all_members'
cName   = 'channel_name'
fName   = 'name_first'
lName   = 'name_last'
chans   = 'channels'

def channels_list_v1(auth_user_id):
    # First, check if auth_user-id is a valid user_id
    check_auth_user_id(auth_user_id)

    output = []
    # Find channels that user is part of and add them to the output list
    for chanD in src.data.channels:
        for memberD in chanD['all_members']:
            if auth_user_id is memberD['user_id']:
                channel = {}
                channel[cID] = chanD[cID]
                channel[cName] = chanD[cName]
                if channel[cID] != None and channel[cName] != None:
                    output.append(channel)

    return {
        'channels': output
    }

def channels_listall_v1(auth_user_id):
    # First, check if auth_user_id is a valid user_id
    check_auth_user_id(auth_user_id)

    # If auth_user_id is valid, then it should print all channels in data
    output = []
    for d in src.data.channels:
        channel = {}
        channel[cID] = d[cID]
        channel[cName] = d[cName]
        if channel[cID] != None and channel[cName] != None:
            output.append(channel)
    return {
        'channels': output
    }

def channels_create_v1(auth_user_id, name, is_public):
    return {
        'channel_id': 1,
    }


# Function that checks if auth_user_id is valid
def check_auth_user_id(auth_user_id):
    for d in src.data.users:
        try:
            if auth_user_id == d[uID]:
                return
        except Exception:
            pass
    raise AccessError
