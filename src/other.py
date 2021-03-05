import src.data

def clear_v1():

    src.data.users = [
        {
            'user_id': None,
            'first_name': None,
            'last_name': None,
            'email': None,
            'password': None,
            'handle_string': None,
        }
    ]

    src.data.channels = [
        {
            'channel_id': 1,
            'is_public': None,
            'channel_name': None,
            'owner_members': [],
            'all_members': [],
        }
    ]

def search_v1(auth_user_id, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }
