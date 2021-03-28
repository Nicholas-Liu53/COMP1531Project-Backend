import pytest
from src.message import message_send_v1, message_remove_v1, message_edit_v1
from src.error import InputError, AccessError
import src.channel, src.channels, src.auth

#* Test send functions together with message/send/v2
#? Test if message_id increases correctly

def test_senddm_errors():
    '''
    #* Test if a authorised user who is not part of the DM they are posting to raises an Access Error
    < Register 3 users >
    < Create dm with 2 users >
    < Try send a message with 3rd user >
    #* Test if passing an invalid dm_id raises an InputError
    < Register user >
    < Try send a message with user >
    #* Test if message is more than 1000 characters rauses an InputError
    < Register 2 users >
    < Create dm with both users >
    < Try send a long message >
    '''
    pass

def test_senddm_multiple():
    pass

def test_dm_unauthorised_user():
    #* All unauthorised user tests
    pass