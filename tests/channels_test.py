# File to test functions in src/channels.py

import pytest
from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
import src.auth, src.channel

def test_channels_list():
    pass

def test_channels_listall():
    pass

def test_channels_create():
    # # Test 1: Newly created public channel by user_id 1 appears in his channel list
    # firstChannel = channels_create_v1(1, 'Oogway', True)
    # assert {'channel_id': result, 'name': 'Oogway'} in channels_list_v1(1)['channels']

    # # Test 2: 

    # secondChannel = channels_create_v1(2, 'Yayot', False)
    # assert {''}
    pass 