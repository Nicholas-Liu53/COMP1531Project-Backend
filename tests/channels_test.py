# File to test functions in src/channels.py

import pytest
from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
import src.auth, src.channel

def test_channels_list():
    # Test 1: For an empty data file, test if running the function with any auth_user_id returns anything
    ## Should raise an AccessError
    # Test 2: Add users but don't join any channels. Test if running the function with their auth_user_id returns anything
    # Test 3: Add users to the channel and test if running the function returns the correct input
    # Test 4: Ensure that the function returns the correct data type
    
    pass

def test_channels_listall():
    # Test 1: If a user with an invalid auth_user_id is inputed, an AccessError is raised
    # Test 2: Ensure that the function returns the correct data type
    # Test 3: Ensure that both public and private channels are displayed
    # Test 4: Add users but don't join any channels. Test if running the function with their auth_user_id returns anything
    # Test 5: Add users to the channel and test if running the function returns the correct input
    pass

def test_channels_create():
    # # Test 1: Newly created public channel by user_id 1 appears in his channel list
    # firstChannel = channels_create_v1(1, 'Oogway', True)
    # assert {'channel_id': result, 'name': 'Oogway'} in channels_list_v1(1)['channels']

    # # Test 2: 

    # secondChannel = channels_create_v1(2, 'Yayot', False)
    # assert {''}
    pass 