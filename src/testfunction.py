from error import AccessError, InputError

channels = [

    {
        'channel_id': 1,
        'is_public': True,
        'name': 'test',
        'owner_members': [],
        'all_members': [
            {
        'u_id': 1,
        'name_first': 'vi',
        'name_last': 'le',
        'email': 'levincent',
        'password': None,
        'handle_string': 'lmfo',
        'permission_id': None,
        'session_id': [],
        }
        ],
    }
]

def channel_details_v1(auth_user_id, channel_id):

    '''
    channel_details_v1 calls upon a new copy of the desired channel dictionary that only contains filtered keys and values that is public.
    Does not include private information such as password.
    
    Arguments:
        auth_user_id (int) - The id of the user that is calling the channel details. Must be present within that channel's "all_members"
        channel_id (int) - The id of the desired channel which we want details of.
    
    Exceptions:
        InputError - Occurs when the channel_id used as a parameter does not already exist in the channels list.
        AccessError - Occurs when the user calling the function is not authorised as a member of that channel, meaning the id is not present in "all_members" within channel dictioanry.
    
    Return Value:
        Returns filteredDetails on succesfully creating a copy of the channel we want, with only the filtered information. The return is a dictionary.
    '''

    # check for valid channel
    passed = False
    for check in channels:
        if check["channel_id"] == channel_id:
            passed = True
    if not passed:
        raise InputError

    # check if user is authorised for channel
    for chans in channels:
        userAuth = False
        if chans["channel_id"] == channel_id:
            for users in chans["all_members"]:
                if users['u_id'] == auth_user_id:
                    userAuth = True
                    break
            if not userAuth:
                raise AccessError
    for details in channels:
        if details["channel_id"] == channel_id:

            # filteres the information to be displayed
            filteredDetails = dict((item, details[item]) for item in ["name","is_public"] if item in details)

            # takes only user_id, first and last name
            ownmem = []
            for user in details["owner_members"]:
                filteredOwner = {}
                filteredOwner.update(dict((key,value) for key, value in user.items() if key == "name_first"))
                filteredOwner.update(dict((key,value) for key, value in user.items() if key == "name_last"))
                filteredOwner.update(dict((key,value) for key, value in user.items() if key == "email"))
                filteredOwner.update(dict((key,value) for key, value in user.items() if key == "handle_string"))
                ownmem.append(filteredOwner)
            dictAllOwn = {"owner_members": ownmem}
            filteredDetails.update(dictAllOwn)

            allmem = []
            for user in details["all_members"]:
                filteredUser = {}
                filteredUser.update(dict((key,value) for key, value in user.items() if key == "name_first"))
                filteredUser.update(dict((key,value) for key, value in user.items() if key == "name_last"))
                filteredUser.update(dict((key,value) for key, value in user.items() if key == "email"))
                filteredUser.update(dict((key,value) for key, value in user.items() if key == "handle_string"))
                allmem.append(filteredUser)
            dictAllMem = {"all_members" : allmem}
            filteredDetails.update(dictAllMem)

    return filteredDetails


print(channel_details_v1(1,1))