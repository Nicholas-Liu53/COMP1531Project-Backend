# File to test functions in src/channel.py

import pytest
from src.channel import channel_invite_v1, channel_details_v1, channel_messages_v1, channel_leave_v1, channel_join_v1, channel_addowner_v1, channel_removeowner_v1
from src.error import InputError, AccessError
import src.auth, src.channels
import src.data


def test_channel_invite():
    ''' uses auth_user_id, channel_id, u_id)'''
    #* Create user and channel for user to be invited
    #* Users
    userID1 = src.auth.auth_register_v1("testing1@gmail.com", "Monkey", "Vincent", "Le")
    userID2 = src.auth.auth_register_v1("testing2@gmail.com", "jonkey", "Darius", "Kuan")
    #* Channel create
    privateChannel = src.channels.channels_create_v1(userID1[auth_user_id], 'Coolkids', False)

    #* Test 1: Does userID2 get successfully invited to channel "Coolkids"
    channel_invite_v1(userID1[auth_user_id], privateChannel[channel_id], userID2[user_id])
    assert {'user_id': userID2[auth_user_id], 'name_first': 'Darius', 'name_last': 'Kuan'} in channel_details_v1(userID1[auth_user_id], privateChannel[channel_id])[all_members]

    #* Test 2: is InputError raised when channel_id does not refer to valid channel
    with pytest.raises(InputError) as e:
        channel_invite_v1(userID1[auth_user_id], "ThischannelIDdoesNotExist", userID2[user_id])
    
    #* Test 3: is InputError raised when u_id isnt a valid user
    with pytest.raises(InputError) as e:
        channel_invite_v1(userID1[auth_user_id], "ThischannelIDdoesNotExist", "DoesntExist")
    
    #* Test 4: is AccessError raised when auth_user_id is not already a member of the channel
    userID3 = src.auth.auth_register_v1("imposter@gmail.com", "g2g2g", "Among", "Us")
    with pytest.raises(AccessError) as e:
        channel_invite_v1(userID3[auth_user_id], privateChannel[channel_id], userID2[user_id])

    pass

def test_channel_details():
    '''auth_user_id, channel_id'''
    userID1 = src.auth.auth_register_v1("testing4@gmail.com", "Monkey1", "Vincentd", "Lee")
    userID2 = src.auth.auth_register_v1("testing3@gmail.com", "jonkey1", "Imposterd", "Kuand")
    realChannel = src.channels.channels_create_v1(userID1[auth_user_id], 'ChannelINFO', True)

    #* Test 1: Using the authorised user, does the channel details get presented for one user in channel
    assert channel_details_v1(userID1[auth_user_id], realChannel[channel_id]) == { channel_name : "ChannelINFO", owner_members: [ {
        'user_id' : userID1[user_id], 
        'first_name': "Vincent",
        'last_name': 'Le',
        'email': 'testing1@gmail.com'
    }] }
    
    #* Test 2: Is InputError raised when Channel ID is not a valid channel
    with pytest.raises(AccessError) as e:
        channel_details_v1(userID1[auth_user_id], 'InvalidID')

    #* Test 3: Is AccessError raised when the user is not membber of channel with the channel id
    with pytest.raises(AccessError) as e:
        channel_details_v1(userID2[auth_user_id], realChannel[channel_id])
    

    pass

def test_channel_messages():
    pass

def test_channel_leave():
    pass

def test_channel_join():
    pass

def test_channel_addowner():
    pass

def test_channel_removeowner():
    pass