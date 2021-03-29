import src.data
from src.error import AccessError, InputError
from src.other import decode, get_channel, get_members, get_user
from datetime import timezone, datetime

def message_send_v1(token, channel_id, message):
    
    # Decode the token
    auth_user_id, _ = decode(token)

    # If the message is too long, raise InputError
    if len(message) > 1000:
        raise InputError

    # Check if user is in channel
    if auth_user_id not in get_channel(channel_id)['all_members']:
        raise AccessError

    now = datetime.now()
    time_created = int(now.strftime("%s"))

    # User is in the channel (which exists) & message is appropriate length
    #* Time to send a message
    data.messages_log.append(
        {
            'channel_id'    : channel_id,
            'dm_id'         : -1,
            'handle_string' : get_user(auth_user_id)['handle_string'],
            'time_created'  : time_created,
            'message_id'    : len(data.messages_log),
            'message_string': message,
        }
    )

    return {
        'message_id': 1,
    }

def message_remove_v1(auth_user_id, message_id):
    return {
    }

def message_edit_v1(auth_user_id, message_id, message):
    return {
    }