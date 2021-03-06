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
    # Ensure an InputError when the channel name is 
    # more than 20 characters long
    if len(name) > 20:
        raise InputError

    # Time to find the user details
    userFound = False
    j = 0
    while not userFound:
        if j >= len(src.data.users):
            # If user doesn't exist in database, inputError
            raise AccessError
        elif src.data.users[j][uID] == auth_user_id:
            userFound = True
        j += 1

    j -= 1      # Undo extra increment

    # Identify the new channel ID
    # Which is an increment of the most recent channel id
    newID = len(src.data.channels)


    # Add this new channel into the channels data list
    # The only member is the auth user that created this channel
    src.data.channels.append(
        {
            'channel_id': newID,
            'is_public': is_public,
            'channel_name': name,
            'owner_member': [src.data.users[j]],
            'all_members': [src.data.users[j]],
        }
    )

    # Return a dictionary containing the new channel ID 
    return {
        'channel_id': newID,
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
