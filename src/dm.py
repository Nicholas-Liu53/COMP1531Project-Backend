import src.data
from src.error import AccessError, InputError

AuID    = 'auth_user_id'
uID     = 'u_id'
cID     = 'channel_id'
allMems = 'all_members'
cName   = 'name'
fName   = 'name_first'
lName   = 'name_last'
chans   = 'channels'

def dm_details_v1(token, dm_id):
    pass

def dm_list_v1(token):
    pass

def dm_create_v1(token, u_ids):
    pass

def dm_remove_v1(token, dm_id):
    pass

def dm_invite_v1(token, dm_id, u_id):
    pass

def dm_leave_v1(token, dm_id):
    pass

def dm_messages_v1(token, dm_id, start):
    pass