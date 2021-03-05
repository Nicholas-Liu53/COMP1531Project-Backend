# File containing all of the data variables

'''
Two variables:

users (list):
    each element of list is a user dictionary containing:
        user_id
        first_name
        last_name
        email
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
        'user_id': None,
        'first_name': None,
        'last_name': None,
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