import src.data
from src.error import AccessError, InputError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    # Find the channel in the database
    channelFound = False
    i = 0

    # Loop throug channel data base until channel is found
    while not channelFound:
        if i >= len(src.data.channels):
            # If channel doesn't exist in database, inputError
            raise InputError
        elif src.data.channels[i]['channel_id'] == channel_id:
            # If channel is found
            channelFound = True
        i += 1

    i -= 1      # Undo extra increment

    if src.data.channels[i]['is_public'] == False:
        # If channel is private, AccessError
        raise AccessError

    # Time to find the user details
    userFound = False
    j = 0
    while not userFound:
        if j >= len(src.data.users):
            # If user doesn't exist in database, AccessError
            raise AccessError
        elif src.data.users[j]['user_id']:
            userFound = True
        j += 1

    j -= 1      # Undo extra increment

    # Time to add the user into the channel
    src.data.channels[i]['all_members'].append(src.data.users[j])

    # Done, return empty list 
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }