import pytest
from src.message import message_send_v1, message_remove_v1, message_edit_v1, message_share_v1, message_senddm_v1
from src.error import InputError, AccessError
import src.channel, src.channels, src.auth
from src.other import get_user, get_channel, clear_v1, SECRET
from datetime import timezone, datetime
from src.notifications import notifications_get_v1
import jwt

AuID   = 'auth_user_id'
cID    = 'channel_id'
token  = 'token'
nMess  = 'notification_message'
notifs = 'notifications'

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

    channel1 = src.channels.channels_create_v1(user1[token], 'TrumpPence', True)

    #* Test 1: Test if added into channel notif comes up
    src.channel.channel_invite_v1(user1[token], channel1[cID], user2[AuID])
    assert {
        cID    : channel1[cID],
        'dm_id': -1,
        nMess  : f"{get_user(user1[AuID])['handle_string']} added you to {get_channel(channel1[cID])['name']}",
    } in notifications_get_v1(user2[token])[notifs]
    src.channel.channel_invite_v1(user1[token], channel1[cID], user3[AuID])
    assert {
        cID    : channel1[cID],
        'dm_id': -1,
        nMess  : f"{get_user(user1[AuID])['handle_string']} added you to {get_channel(channel1[cID])['name']}",
    } in notifications_get_v1(user3[token])[notifs]

    #* Test 2: Test if mentions comes up
    message_send_v1(user2[token], channel1[cID], f"Hello @{get_user(user1[AuID])['handle_string']} @{get_user(user3[AuID])['handle_string']}")
    assert {
        cID    : channel1[cID],
        'dm_id': -1,
        nMess  : f"{get_user(user2[AuID])['handle_string']} tagged you in {get_channel(channel1[cID])['name']}: Hello @{get_user(user1[AuID])['handle_string']} @{get_user(user3[AuID])['handle_string']}",
    } in notifications_get_v1(user1[token])[notifs]
    assert {
        cID    : channel1[cID],
        'dm_id': -1,
        nMess  : f"{get_user(user2[AuID])['handle_string']} tagged you in {get_channel(channel1[cID])['name']}: Hello @{get_user(user1[AuID])['handle_string']} @{get_user(user3[AuID])['handle_string']}",
    } in notifications_get_v1(user3[token])[notifs]

    #* Test 3: Only recent 20 notifs come up
    i = 0
    while i < 22:
        message_send_v1(user1[token], channel1[cID], f"Hi @{get_user(user2[AuID])['handle_string']} @{get_user(user3[AuID])['handle_string']}")
        i += 1
    assert {
        cID    : channel1[cID],
        'dm_id': -1,
        nMess  : f"{get_user(user1[AuID])['handle_string']} added you to {get_channel(channel1[cID])['name']}",
    } not in notifications_get_v1(user3[token])[notifs]
    assert {
        cID    : channel1[cID],
        'dm_id': -1,
        nMess  : f"{get_user(user2[AuID])['handle_string']} tagged you in {get_channel(channel1[cID])['name']}: Hello @{get_user(user1[AuID])['handle_string']} @{get_user(user3[AuID])['handle_string']}",
    } not in notifications_get_v1(user3[token])[notifs]

    i = 0
    while i < 21:
        if i == 0:
            message_send_v1(user3[token], channel1[cID], f"Baby shark @{get_user(user2[AuID])['handle_string']}")
        else:
            message_send_v1(user3[token], channel1[cID], f"Dooo dooo dooo dooo @{get_user(user2[AuID])['handle_string']}")
        i += 1
    assert {
        cID    : channel1[cID],
        'dm_id': -1,
        nMess  : f"{get_user(user3[AuID])['handle_string']} tagged you in {get_channel(channel1[cID])['name']}: Baby shark @{get_user(user2[AuID])['handle_string']}",
    } not in notifications_get_v1(user2[token])[notifs]

    #* Test 4: Only first 20 characters
    assert {
        cID    : channel1[cID],
        'dm_id': -1,
        nMess  : f"{get_user(user3[AuID])['handle_string']} tagged you in {get_channel(channel1[cID])['name']}: Dooo dooo dooo dooo ",
    } in notifications_get_v1(user2[token])[notifs]