# File to test functions in src/admin.py

import pytest
from src.admin import user_remove_v1, userpermission_change_v1, notifications_get_v1
from src.error import AccessError, InputError

AuID    = 'auth_user_id'
uID     = 'u_id'
cID     = 'channel_id'
chans   = 'channels'
allMems = 'all_members'
fName   = 'name_first'
lName   = 'name_last'

def test_user_remove():
    pass

def test_userpermissions_change():
    pass

def test_notifications_get():
    pass