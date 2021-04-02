import pytest
from src.message import message_send_v1, message_remove_v1, message_edit_v1, message_share_v1, message_senddm_v1
from src.error import InputError, AccessError
import src.channel, src.channels, src.auth
from src.other import decode, get_user, get_channel, get_dm, clear_v1, SECRET
from datetime import timezone, datetime
from src.notifications import notifications_get_v1
import jwt
from src.dm import dm_create_v1, dm_invite_v1

cID    = 'channel_id'
token  = 'token'
nMess  = 'notification_message'
notifs = 'notifications'
AuID = 'auth_user_id'

@pytest.fixture
def user1():
    src.other.clear_v1()    
    return src.auth.auth_register_v2("first@gmail.com", "password", "User", "1")

@pytest.fixture
def user2():
    return src.auth.auth_register_v2("second@gmail.com", "password", "User", "2")

@pytest.fixture
def user3():
    return src.auth.auth_register_v2("third@gmail.com", "password", "User", "3")

def test_notifications_get_in_channels(user1, user2, user3):
    # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #   Note: This test has white-box testing involved  #
    # # # # # # # # # # # # # # # # # # # # # # # # # # #
    user1ID, _ = decode(user1[token])
    user2ID, _ = decode(user2[token])
    user3ID, _ = decode(user3[token])

    channel1 = src.channels.channels_create_v1(user1[token], 'TrumpPence', True)

    #* Test 1: Test if added into channel notif comes up
    src.channel.channel_invite_v1(user1[token], channel1[cID], user2ID)
    assert {
        cID    : channel1[cID],
        'dm_id': -1,
        nMess  : f"{get_user(user1ID)['handle_string']} added you to {get_channel(channel1[cID])['name']}",
    } in notifications_get_v1(user2[token])[notifs]
    src.channel.channel_invite_v1(user1[token], channel1[cID], user3ID)
    assert {
        cID    : channel1[cID],
        'dm_id': -1,
        nMess  : f"{get_user(user1ID)['handle_string']} added you to {get_channel(channel1[cID])['name']}",
    } in notifications_get_v1(user3[token])[notifs]

    #* Test 2: Test if mentions comes up
    message_send_v1(user2[token], channel1[cID], f"Hello @{get_user(user1ID)['handle_string']} @{get_user(user3ID)['handle_string']}")
    assert {
        cID    : channel1[cID],
        'dm_id': -1,
        nMess  : f"{get_user(user2ID)['handle_string']} tagged you in {get_channel(channel1[cID])['name']}: Hello @{get_user(user1ID)['handle_string']} @{get_user(user3ID)['handle_string']}",
    } in notifications_get_v1(user1[token])[notifs]
    assert {
        cID    : channel1[cID],
        'dm_id': -1,
        nMess  : f"{get_user(user2ID)['handle_string']} tagged you in {get_channel(channel1[cID])['name']}: Hello @{get_user(user1ID)['handle_string']} @{get_user(user3ID)['handle_string']}",
    } in notifications_get_v1(user3[token])[notifs]

    #* Test 3: Only recent 20 notifs come up
    i = 0
    while i < 22:
        message_send_v1(user1[token], channel1[cID], f"Hi @{get_user(user2ID)['handle_string']} @{get_user(user3ID)['handle_string']}")
        i += 1
    assert {
        cID    : channel1[cID],
        'dm_id': -1,
        nMess  : f"{get_user(user1ID)['handle_string']} added you to {get_channel(channel1[cID])['name']}",
    } not in notifications_get_v1(user3[token])[notifs]
    assert {
        cID    : channel1[cID],
        'dm_id': -1,
        nMess  : f"{get_user(user2ID)['handle_string']} tagged you in {get_channel(channel1[cID])['name']}: Hello @{get_user(user1ID)['handle_string']} @{get_user(user3ID)['handle_string']}",
    } not in notifications_get_v1(user3[token])[notifs]

    i = 0
    while i < 21:
        if i == 0:
            message_send_v1(user3[token], channel1[cID], f"Baby shark @{get_user(user2ID)['handle_string']}")
        else:
            message_send_v1(user3[token], channel1[cID], f"Dooo dooo dooo dooo @{get_user(user2ID)['handle_string']}")
        i += 1
    assert {
        cID    : channel1[cID],
        'dm_id': -1,
        nMess  : f"{get_user(user3ID)['handle_string']} tagged you in {get_channel(channel1[cID])['name']}: Baby shark @{get_user(user2ID)['handle_string']}",
    } not in notifications_get_v1(user2[token])[notifs]

    #* Test 4: Only first 20 characters
    assert {
        cID    : channel1[cID],
        'dm_id': -1,
        nMess  : f"{get_user(user3ID)['handle_string']} tagged you in {get_channel(channel1[cID])['name']}: Dooo dooo dooo dooo ",
    } in notifications_get_v1(user2[token])[notifs]

def test_notifications_dms_added(user1, user2, user3):
    #Test that a notif is sent to user when they are added to dm with channel id = -1
    #Ordered from most to least recent

    dm_0 = dm_create_v1(user1[token], [user2[AuID]])
    dm_1 = dm_create_v1(user1[token], [user3[AuID]])


    #Test 1: for initial creation of DM
    assert {
        cID : -1,
        'dm_id': 0,
        nMess : f"{get_user(user1[AuID])['handle_string']} tagged you in {get_dm(dm_0['dm_id'])['name']}",
    } in notifications_get_v1(user2[token])[notifs]

    #Test 2: For DM_invite inviting another person
    dm_invite_v1(user1[token], dm_0['dm_id'], user3['u_id'])

    assert {
        cID : -1,
        'dm_id': 0,
        nMess : f"{get_user(user1[AuID])['handle_string']} tagged you in {get_dm(dm_0['dm_id'])['name']}",
    } in notifications_get_v1(user3[token])[notifs]

    #Test 3: being added to multiple dms
    assert {
        cID : -1,
        'dm_id': 1,
        nMess : f"{get_user(user1[AuID])['handle_string']} tagged you in {get_dm(dm_1['dm_id'])['name']}",
    } in notifications_get_v1(user3[token])[notifs]

    #Test 4: Make sure ordered from most to least recent

#* DM tagged tests
    #* When tagged, correct amount of tags come up
    '''
    < Register 2 users >
    < Create DM >
    < Tag once >
    < Assert tagged once >
    '''
    #* Only first 20 characters of the message come up
    '''
    < Register 2 users >
    < Create DM >
    < Tag with long ass message >
    < Assert message is 20 characters >
    '''
    #* Test that users that are not in the DM cannot be tagged
    '''
    < Register 3 users >
    < Create DM with first 2 >
    < Try tag the third >
    < Assert that he was no tagged >
    '''
    #* When tagged >20 times, only 20 tags come up (and oldest ones dont show up)
    '''
    < Register 2 users >
    < Create DM >
    < Tag 21 >
    < Assert that 20 notifs are displayed >
    '''