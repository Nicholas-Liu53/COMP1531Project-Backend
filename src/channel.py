import src.data
from src.error import AccessError, InputError

from src.error import AccessError, InputError
from src.channels import channels_listall_v1, channels_list_v1

def channel_invite_v1(auth_user_id, channel_id, u_id):
    #check if channel_id is valid
    for check in src.data.channels:
        passed = False
        if check['channel_id'] == channel_id:
            passed = True
            break
    if passed == False:
        raise InputError

    # check if user is authorised to invite

    for chans in src.data.channels:
        userAuth = False
        if chans["channel_id"] == channel_id:
            for users in chans["all_members"]:
                if users['user_id'] == auth_user_id:
                    userAuth = True
                    break
            if userAuth == False:
                raise AccessError
                    
    # should check for auth_user_id in channel info first for owners
    inviteUser = {}
    for user in src.data.users:
        if user["user_id"] == u_id: # finds desired u_id
            inviteUser = user.copy()
    if inviteUser == {}:
        raise InputError
    
    # now searches for channel_id
    for chan in src.data.channels:
        if chan["channel_id"] == channel_id:
            # no duplicates
            chan["all_members"].append(inviteUser) if inviteUser not in chan["all_members"] else None
    return {   
    }



def channel_details_v1(auth_user_id, channel_id):
    # check for valid channel
    for check in src.data.channels:
        passed = False
        if check["channel_id"] == channel_id:
            passed = True
            break
    if passed == False:
        raise InputError

    # check if user is authorised for channel
    for chans in src.data.channels:
        userAuth = False
        if chans["channel_id"] == channel_id:
            for users in chans["all_members"]:
                if users['user_id'] == auth_user_id:
                    userAuth = True
                    break
            if userAuth == False:
                raise AccessError
    for details in src.data.channels:
        if details["channel_id"] == channel_id:
            # filteres the information to be displayed
            filteredDetails = dict((item, details[item]) for item in ["channel_name"] if item in details)

            # takes only user_id, first and last name
            ownmem = []
            for user in details["owner_members"]:
                filteredOwner = {}
                filteredOwner.update(dict((key,value) for key, value in user.items() if key == "user_id"))
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
                filteredUser.update(dict((key,value) for key, value in user.items() if key == "user_id"))
                filteredUser.update(dict((key,value) for key, value in user.items() if key == "name_first"))
                filteredUser.update(dict((key,value) for key, value in user.items() if key == "name_last"))
                filteredUser.update(dict((key,value) for key, value in user.items() if key == "email"))
                filteredUser.update(dict((key,value) for key, value in user.items() if key == "handle_string"))
                allmem.append(filteredUser)
            dictAllMem = {"all_members" : allmem}
            filteredDetails.update(dictAllMem)

    return filteredDetails

def channel_messages_v1(auth_user_id, channel_id, start):
    #ASSUMPTION: MESSAGES IS A LIST containing all the messages in channel 
    
    #Handling of input and access errors 
    #Input error: Channel ID is not a valid channel 
    #This is the case
    if channel_id not in src.channels.channels_listall_v1(auth_user_id):
        return InputError
    
    #Input error: Start is greater than total number of messages in list 
    if start > len(messages):
        return InputError
    
    #Access error: When auth_user_id is not a member of channel with channel_id 
    if channel_id not in src.channls.channels_list_v1(auth_user_id):
        return AccessError

    #First, find how many messages there are in channel after start 
    #Create new list for this so that index 0 is oldest message and 50 will be start index 
    messagesList = []
    
    #For each message after start, insert it into list such that in messagesList index 0 is oldest message 
    #and index 50 will be the message at 'start'
    #want to count back from 50 to message with index 'start-49' or until 50 messages have been counted out
    counter = start + 50
    while (counter > -1 and counter > start): 
        currentMessage = messages[counter]
        insert.messagesList(currentMessage)
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

'''
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        
        'start': 0,
        'end': 50,
    }
'''
def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
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
        elif src.data.users[j]['user_id'] == auth_user_id:
            userFound = True
        j += 1

    j -= 1      # Undo extra increment

    # Time to add the user into the channel
    src.data.channels[i]['all_members'].append(src.data.users[j])

    # Done, return empty list 
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }
