from error import InputError, AccessError
channels = [
    {
        'channel_id': 1,
        'channel_name': 'hi',
        'owner_members': [],
        'all_members': [{'user_id': 1,
        'first_name': 'a',
        'last_name': 'a',
        'email': None,
        'handle_str': None,
        'password': None}],
        'is_public': True
    }  ,  
    {
        'channel_id': 2,
        'channel_name': 'bi',
        'owner_members': [],
        'all_members': [],
        'is_public': True
    },
    {
        'channel_id': 3,
        'channel_name': 'li',
        'owner_members': [],
        'all_members': [],
        'is_public': True
    }
]
userdata = [
        {'user_id': 1,
        'first_name': 'a',
        'last_name': 'a',
        'email': None,
        'handle_str': None,
        'password': None},
            {'user_id': 2,
        'first_name': 'b',
        'last_name': 'b',
        'email': None,
        'handle_str': None,
        'password': None},
            {'user_id': 3,
        'first_name': 'c',
        'last_name': 'c',
        'email': None,
        'handle_str': None,
        'password': None},
]
def channel_invite_v1(auth_user_id, channel_id,u_id):
    '''<INSERT DOCSTRINGS> '''

    for check in channels:
        passed = False
        if check["channel_id"] == channel_id:
            passed = True
            break
    if passed == False:
        raise InputError

    for chans in channels:
        userAuth = False
        if chans["channel_id"] == channel_id:
            for users in chans["all_members"]:
                if users['user_id'] == auth_user_id:
                    userAuth = True
                    break
            if userAuth == False:
                raise AccessError
                    
    
    

    inviteUser = {}
    for user in userdata:
        if user["user_id"] == u_id: # finds desired u_id
            inviteUser = user.copy()
    if inviteUser == {}:
        raise InputError

    for chan in channels:
        if chan["channel_id"] == channel_id:
            # ensures no duplicates
            chan["all_members"].append(inviteUser) if inviteUser not in chan["all_members"] else None

    return channels

def channel_details_v1(auth_user_id, channel_id):
    # check for valid channel
    for check in channels:
        passed = False
        if check["channel_id"] == channel_id:
            passed = True
            break
    if passed == False:
        raise InputError

    # check if user is authorised for channel
    for chans in channels:
        userAuth = False
        if chans["channel_id"] == channel_id:
            for users in chans["all_members"]:
                if users['user_id'] == auth_user_id:
                    userAuth = True
                    break
            if userAuth == False:
                raise AccessError
    for details in channels:
        if details["channel_id"] == channel_id:
            filteredDetails = dict((item, details[item]) for item in ["channel_name"] if item in details)
            ownmem = []
            for user in details["owner_members"]:
                filteredOwner = {}
                filteredOwner.update(dict((key,value) for key, value in user.items() if key == "user_id"))
                filteredOwner.update(dict((key,value) for key, value in user.items() if key == "first_name"))
                filteredOwner.update(dict((key,value) for key, value in user.items() if key == "last_name"))
                ownmem.append(filteredOwner)
            dictAllOwn = {"owner_members": ownmem}
            filteredDetails.update(dictAllOwn)


            allmem = []
            for user in details["all_members"]:
                filteredUser = {}
                filteredUser.update(dict((key,value) for key, value in user.items() if key == "user_id"))
                filteredUser.update(dict((key,value) for key, value in user.items() if key == "first_name"))
                filteredUser.update(dict((key,value) for key, value in user.items() if key == "last_name"))
                allmem.append(filteredUser)
            dictAllMem = {"all_members" : allmem}
            filteredDetails.update(dictAllMem)

    return filteredDetails
channel_invite_v1(1,1,3)
channel_invite_v1(1,1,2)


print(channel_details_v1(1,1)["all_members"])


