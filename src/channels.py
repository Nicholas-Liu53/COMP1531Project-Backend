import src.data
from src.error import AccessError, InputError
from src.other import decode, get_channel, get_members, get_user
import jwt

AuID    = 'auth_user_id'
uID     = 'u_id'
cID     = 'channel_id'
allMems = 'all_members'
Name    = 'name'
fName   = 'name_first'
lName   = 'name_last'
chans   = 'channels'
token   = 'token'

def channels_list_v2(token):
    '''
    Provides a list of all channels (and their associated details) that the authorised user is part of

    Arguments:
        token (str): JWT containing { u_id, session_id }

    Exceptions:
        AccessError - Raised when the token passed in is not valid

    Return Value:
        Returns dictionary of a list of channels mapped to the key string 'channels'
        Each channel is represented by a dictionary containing types { channel_id, name }
    '''
    auth_user_id, _ = decode(token)
    output = []
    for chanD in src.data.channels:
        if auth_user_id in chanD['all_members']:
            channel = {}
            channel[cID] = chanD[cID]
            channel[Name] = chanD[Name]
            output.append(channel)

    return {
        'channels': output
    }

def channels_listall_v2(token):
    '''
    Provides a list of all channels (and their associated details)
    Channels are provided irrespective of whether the member is part of the channel
    Both public and private channels are provided

    Arguments:
        token (str): JWT containing { u_id, session_id }

    Exceptions:
        AccessError - Raised when the token passed in is not valid

    Return Value:
        Returns dictionary of a list of channels mapped to the key string 'channels'
        Each channel is represented by a dictionary containing types { channel_id, name }
    '''
    decode(token)
    output = []
    for d in src.data.channels:
        channel = {}
        channel[cID] = d[cID]
        channel[Name] = d[Name]
        output.append(channel)
    return {
        'channels': output
    }

def channels_create_v1(token, name, is_public):
    '''
    Creates a channel and adds the user into that channel as both an owner and member

    Arguments:
        token               - The token id of the user that wants to create a channel
        name         (str)  - The name of the channel that the user wants to create, comes as one string
        is_public    (bool) - The boolean value of whether this channel is to be public or private
                                True  --> Channel is to be public
                                False --> Channel is to be private

    Exceptions:
        InputError  - Occurs when the intended length of the channel name is too long (21 chars or greater)
        AccessError - Occurs when the auth_user_id inputted does not belong to any user in the database

    Return Value:
        Returns a dictionary with the key being 'channel_id' and the value of the newly created channel's id
    '''
    auth_user_id, _ = decode(token)
    # Ensure an InputError when the channel name is 
    # more than 20 characters long
    if len(name) > 20:
        raise InputError

    # Time to find the user details
    userFound = False
    j = 0
    while not userFound:
        if j >= len(src.data.users):
            # If user doesn't exist in database, AccessError
            raise AccessError
        elif src.data.users[j][uID] == auth_user_id:
            userFound = True
        j += 1

    j -= 1      # Undo extra increment

    # Identify the new channel ID
    # Which is an increment of the most recent channel id
    if not len(src.data.channels):
        newID = len(src.data.channels)
    else:
        newID = src.data.channels[-1][cID] + 1


    # Add this new channel into the channels data list
    # The only member is the auth user that created this channel
    src.data.channels.append(
        {
            'channel_id': newID,
            'is_public': is_public,
            'name': name,
            'owner_members': [src.data.users[j][uID]],
            'all_members': [src.data.users[j][uID]],
        }
    )

    # Return a dictionary containing the new channel ID 
    return {
        'channel_id': newID,
    }
