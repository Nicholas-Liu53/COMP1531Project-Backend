import src.data

from src.error import AccessError, InputError
from src.channels import channels_listall_v1, channels_list_v1

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

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
        
        #Change start 
        'start': 0,
        'end': 50,
    }
'''
def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }
