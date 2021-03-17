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
        'user_id': None,
        'name_first': None,
        'name_last': None,
        'email': None,
        'password': None,
        'handle_string': None,
    }
]

channels = [
    {
        'channel_id': None,
        'is_public': None,
        'channel_name': None,
        'owner_members': [],
        'all_members': [],
    }
]

messages_log = [
    {
        'channel_id': None,
        'handle_string': None,
        'time_created': None,
        'message_id': None,
        'message_string': None,
    },
]
