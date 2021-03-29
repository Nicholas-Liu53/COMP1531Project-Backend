import src.data
from src.error import AccessError, InputError
from src.channels import channels_listall_v1, channels_list_v1
import jwt

SECRET = 'MENG'

AuID      = 'auth_user_id'
uID       = 'u_id'
cID       = 'channel_id'
creatorID = 'creator_id'
allMems   = 'all_members'
Name      = 'name'
fName     = 'name_first'
lName     = 'name_last'
chans     = 'channels'
handle    = 'handle_string'
dmID      = 'dm_id'
seshID    = 'session_id'

def channel_invite_v1(token, channel_id, u_id):
    
    '''
    channel_invite_v1 checks if a user is authorised to invite another user to a channel and then automatically adds the
    desired user to the specific channel dictionary within the list contained in "all_members".

    Arguments:
        token (int) - The integer id of a user within both the user list and channel "all_members" calling the function to invite another user
        channel_id (int) - The integer id of the channel that we want to invite a user to. Should be present in the channels list.
        u_id (int) - The integer id of a user that the authorised user wants to invite to that specific channel.

    Exceptions:
        InputError - Occurs when the channel_id used as a parameter does not already exist in the channels list.
        InputError - Occurs when the u_id or id of the user that we are trying to invite does not already exist within the users list.
        AccessError - Occurs when the user calling the function is not authorised as a member of that channel, meaning the id is not present in "all_members" within channel dictioanry.

    Return Value:
        Returns an empty list on passing all Exceptions, with changes being made directly to our data.py  
    '''

    auth_user_id, _ = decode(token)

    #check if channel_id is valid
    passed = False
    for check in src.data.channels:
        if check['channel_id'] == channel_id:
            passed = True
            break
    if passed == False:
        raise InputError
    

    # check if user is authorised to invite
    for chans in src.data.channels:
        if chans["channel_id"] == channel_id:
            userAuth = False
            for users in chans["all_members"]:
                if users == auth_user_id:
                    userAuth = True
                    break
            if userAuth == False:
                raise AccessError
                    
    # should check for auth_user_id in channel info first for owners

    get_user(u_id)

    # now searches for channel_id
    for chan in src.data.channels:
        if chan["channel_id"] == channel_id:
            # ensure no duplicates
            chan["all_members"].append(u_id) if u_id not in chan["all_members"] else None
    return {   
    }



def channel_details_v1(token, channel_id):

    '''
    channel_details_v1 calls upon a new copy of the desired channel dictionary that only contains filtered keys and values that is public.
    Does not include private information such as password.
    
    Arguments:
        token (int) - The id of the user that is calling the channel details. Must be present within that channel's "all_members"
        channel_id (int) - The id of the desired channel which we want details of.
    
    Exceptions:
        InputError - Occurs when the channel_id used as a parameter does not already exist in the channels list.
        AccessError - Occurs when the user calling the function is not authorised as a member of that channel, meaning the id is not present in "all_members" within channel dictioanry.
    
    Return Value:
        Returns filteredDetails on succesfully creating a copy of the channel we want, with only the filtered information. The return is a dictionary.
    '''

    auth_user_id, _ = decode(token)

    # check for valid channel
    passed = False
    for check in src.data.channels:
        if check["channel_id"] == channel_id:
            passed = True
            break
    if passed == False:
        raise InputError

    # check if user is authorised for channel
    for chans in src.data.channels:
        if chans["channel_id"] == channel_id:
            userAuth = False
            for users in chans["all_members"]:
                if users == auth_user_id:
                    userAuth = True
                    break
            if userAuth == False:
                raise AccessError
    for details in src.data.channels:
        if details["channel_id"] == channel_id:

            # filteres the information to be displayed
            filteredDetails = dict((item, details[item]) for item in ["name","is_public"] if item in details)

            # takes only user_id, first and last name
            ownmem = []
            for user in details["owner_members"]:
                ownmem.append(get_user(user))
            dictAllOwn = {"owner_members": ownmem}
            filteredDetails.update(dictAllOwn)

            allmem = []
            for user in details["all_members"]:
                allmem.append(get_user(user))
            dictAllMem = {"all_members" : allmem}
            filteredDetails.update(dictAllMem)

    return filteredDetails

def channel_messages_v1(auth_user_id, channel_id, start):

    '''
    channel_messages_v1 returns up to 50 messages within a specified channel.
    
    Arguments:
        token (int) - The id of the user that is calling the channel details. Must be present within that channel's "all_members".
        channel_id (int) - The id of the desired channel which we want details of.
        start(int) - The index of the message that they wish to start returning from.
    
    Exceptions:
        InputError - Occurs when channel_id is not valid or start is greater than total number of messages in channel.
        AccessError - Occurs when authorised user is not a member of channel with channel_id.
    
    Return Value:
        Returns up to 50 messages alongside a start and and end value.
    '''
    
    #Handling of input and access errors 
    #Input error: Channel ID is not a valid channel 
    #This is the case
    channelFound = False 
    for channel in src.channels.channels_listall_v1(auth_user_id)["channels"]:
        if channel_id == channel["channel_id"]:
            channelFound = True
    
    if not channelFound:
        raise InputError


    #Input error: Start is greater than total number of messages in list 
    if start > len(src.data.messages_log):
        raise InputError
    
    #Access error: When auth_user_id is not a member of channel with channel_id 
    userFound = False 
    for channel in src.channels.channels_list_v1(auth_user_id)["channels"]:
        if channel_id == channel["channel_id"]:
            userFound = True
    
    if not userFound:
        raise AccessError

    
    #First, find how many messages there are in channel after start 
    #Create new list for this so that index 0 is oldest message and 50 will be start index 
    messagesList = []
    
    #For each message after start, insert it into list such that in messagesList index 0 is oldest message 
    #and index 50 will be the message at 'start'
    #want to count back from 50 to message with index 'start-49' or until 50 messages have been counted out
    counter = start + 50

    if len(src.data.messages_log) < counter: 
        counter = len(src.data.messages_log) - 1 
    
    while (counter > -1 and counter > start): 
        currentMessage = src.data.messages_log[counter]
        messagesList.insert(currentMessage)
        counter -= 1    
    
    #Now our correct messages are in list messagesList from oldest to newest order     
    #Case 1: Less than 50 messages 
    #Returns -1 as end
    
    #In terms of returning messages, return it as a list
    if len(messagesList) < 50:
            return {
        'messages': messagesList,
        #start should be returned as start
        'start': start,
        'end': -1,
    }
    
    else: 
        #Case 2: More than 50 messages     
        #Returns end which is 'start + 50'
        endValue = start + 50

        return {
        'messages': messagesList,
        'start' : start,
        'end': endValue,
    }

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    '''
    Takes in a user's id and a channel's id and adds that user to that given channel.
        --> Specifically adds it to the 'all_members' list in the channel dictionary 
    If the channel is private then the user isn't added. (See more in Exceptions)

    Arguments:
        token (int) - The id of the user that wants to join the channel
        channel_id   (int) - The id of the channel that the user wants to join

    Exceptions:
        InputError - Occurs when the channel_id inputted does not belong to any channel that exists in the database
        AccessError - Occurs when 
                            1) the channel that the user is trying to join is private
                            2) The auth_user_id inputted does not belong to any user

    Return Value:
        Returns an empty list regardless of conditions :)
    '''

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
        elif src.data.users[j]['u_id'] == auth_user_id:
            userFound = True
        j += 1

    j -= 1      # Undo extra increment

    # Time to add the user into the channel
    src.data.channels[i]['all_members'].append(src.data.users[j])

    # Done, return empty list 
    return {
    }

def channel_addowner_v1(token, channel_id, u_id):
    #if not a user in the channel, add it to all membs too
    # for access error, check permission id first and if permission id isnt of the Dreams owner, check owner list of channels
    # ALLWAYS CHECK FOR PERMISSION ID FIRST FOR DREAM OWNERS
    # Make user with user id u_id an owner of this channel
    # When user with user id u_id is already an owner of the channel INPUT ERROR
      
    auth_user_id, _ = decode(token)
    
    passed = False
    for check in src.data.channels:
        if check['channel_id'] == channel_id:
            passed = True
    if not passed:
        raise InputError
        
    for chans in src.data.channels:
        if chans["channel_id"] == channel_id:
            alreadyOwner = False
            for users in chans["owner_members"]:
                if users == u_id:
                    alreadyOwner = True
            if alreadyOwner == True:
                raise InputError

    # Access error
    dreamsOwner = False
    for users in src.data.users:
        if users['u_id'] == auth_user_id:
            if users['permission_id'] == 1:
                dreamsOwner = True
    for chans in src.data.channels:
        if chans["channel_id"] == channel_id:
            userAuth = False
            for users in chans["owner_members"]:
                if users['u_id'] == auth_user_id:
                    userAuth = True
                    break
    
    if dreamsOwner == False and userAuth == False:
        raise AccessError
    
    # now searches for channel_id
    for chan in src.data.channels:
        if chan["channel_id"] == channel_id:
            # ensure no duplicates
            chan["all_members"].append(u_id) if u_id not in chan["all_members"] else None
            chan["owner_members"].append(u_id) if u_id not in chan["owner_members"] else None

    return {
    }

def channel_removeowner_v1(token, channel_id, u_id):
    # does not remove from all membs
    auth_user_id, _ = decode(token)
    
    passed = False
    for check in src.data.channels:
        if check['channel_id'] == channel_id:
            passed = True
            break
    if not passed:
        raise InputError
    for chans in src.data.channels:
        if chans["channel_id"] == channel_id:
            userisOwner = False
            for users in chans["owner_members"]:
                if users == u_id:
                    userisOwner = True
                    break
            if not userisOwner:
                raise InputError

    # Access error
    dreamsOwner = False
    for users in src.data.users:
        if users['u_id'] == auth_user_id:
            if users['permission_id'] == 1:
                dreamsOwner = True
    
    for chans in src.data.channels:
        if chans["channel_id"] == channel_id:
            userAuth = False
            for users in chans["owner_members"]:
                if users['u_id'] == auth_user_id:
                    userAuth = True

    if dreamsOwner == False and userAuth == False:
        raise AccessError

    for chan in src.data.channels:
        if chan["channel_id"] == channel_id:
            for users in chan["owner_members"]:
                if users == u_id:
                    chan["owner_members"].remove(users)


    return {
    }

def check_session(auth_user_id, session_id):
    for user in src.data.users:
        if auth_user_id == user['u_id']:
            if session_id in user['session_id']:
                return
    raise AccessError


def decode(token):
    payload = jwt.decode(token, SECRET , algorithms = 'HS256')
    auth_user_id, session_id = payload.get('session_id'), payload.get('user_id')
    check_session(auth_user_id, session_id)
    return auth_user_id, session_id


def get_user(user_id):
    for user in src.data.users:
        if user_id == user['user_id']:
            return {
                'user_id': user['user_id'],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_string': user['handle_string'],
            }
    raise InputError
