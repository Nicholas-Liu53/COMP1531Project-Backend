import src.data
import src.error

def channels_list_v1(auth_user_id):
    return {
        'channels': [
            {
                'channel_id': 1,
                'name': 'My Channel',
            }
        ],
    }

def channels_listall_v1(auth_user_id):
    return {
        'channels': [
            {
                'channel_id': 1,
                'name': 'My Channel',
            }
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):
    # Ensure an InputError when the channel name is 
    # more than 20 characters long
    if len(name) > 20:
        raise InputError

    # Identify the new channel ID
    # Which is an increment of the most recent channel id
    newID = src.data.channels[len(src.data.channels) - 1]['channel_id'] + 1
    
    # Add this new channel into the channels data list
    # The only member is the auth user that created this channel
    src.data.channels.append(
        {
            'channel_id': newID,
            'is_public': is_public,
            'channel_name': name,
            'owner_member': [auth_user_id],
            'all_members': [auth_user_id],
        }
    )

    # Return a dictionary containing the new channel ID 
    return {
        'channel_id': newID,
    }