# File containing all of the data variables

'''
Two variables:

users (list):
    each element of list is a user dictionary containing:
        user_id
        first_name
        last_name
        email
        handle_str
        password
        permission of user
        session_id

channels (list):
    each element of list is a channel dictionary containing:
        channel_id
        is_public (bool)
        channel_name
        owner members (list of user_id's)
        all members (list of user_id's)


messages (list):
    each element of list is a message containing:
    message_id
    u_id
    message
    time_created
'''
users = [

    {
        'u_id': None,
        'name_first': None,
        'name_last': None,
        'email': None,
        'password': None,
        'handle_string': None,
        'permission_id': None,
        'session_id': [],
    }
]

channels = [

    {
        'channel_id': None,
        'is_public': None,
        'name': None,
        'owner_members': [],
        'all_members': [],
    }
]

dms = [
    {
        'dm_id': None,
        'name': None,
        'creator_id': None,
        'all_members': [],
    }
]

messages_log = [

    {
        # If message is in channel, dm_id is None (not -1), in other words, don't store a value
        'channel_id': None,
        'dm_id': None,
        'u_id': None,
        'time_created': None,
        'message_id': None,
        'message': None,     # For message/share/v1, the optional message will be stored in message string
    },
]