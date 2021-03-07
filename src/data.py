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
'''

users = [
    {
        '''
        'user_id': ____,
        'name_first': ____,
        'name_last': ____,
        'email': ____,
        'password': ____,
        'handle_string': ____,
        '''
    }
]

channels = [
    {
        '''
        'channel_id': ____,
        'is_public': ____,
        'channel_name': ____,
        'owner_members': [],
        'all_members': [],
        'messages_log': [
            {
                'time_created': _____,
                'user_id': _____,
                'message_id': ______,
                'message_string': _______,
            },
        ]
        '''
    }
]
