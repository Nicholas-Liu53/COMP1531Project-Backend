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

#Ethan
'''
Within a channel you can send dm's to others
''''
@app.route('/dm/remove/v1', methods = ['DELETE'])
def dm_remove_v1(token, dm_id):
#Remove an existing DM, can only be done by original creator of dm
#ASSUMPTION: Rest of dms retain same dm_ids when a dm is removed

    #First omit errors
    #Raise input error if dm_id is not valid DM number
    #Assume dm's are contained in list dm_list
    if dm_id < 0 or dm_id > len(dm_list):
        raise Exception("InputError")
    #AccessError when the user is not original DM creator
    #Can do this by crosschecking the token from input and dm_creator
    if (token_num != original_creator) is True:
        raise Exception("AccessError")

    #Now that errors are fixed, can remove the existing DM with dm_id
    #Loop through dm_list, once dm_id is found remove it
    for i in range(len(DM_list)):
        if DM_list[i]['dm_id'] == dm_id:
            del DM_list[i]

    return {}


#Ethan
@app.route('/dm/invite/v1', methods = ['POST'])
def dm_invite_v1(token, dm_id, u_id):

#ASSUME: Do not need to add new user into dm_name

#Invites a user to an existing dm
#Dm's will be contained like channels in a list, with each dm being a dictionary

    #Raises Input Error when dm_id is not valid
    if dm_id < 0 or dm_id > len(dm_list):
        raise Exception("InputError")
    #Access error if auth user i.e token is not a member of dm
    error_present = True
    #Loop through dm list of token or auth user
    #If dm_id is found then change it to false
    result = dm_list_v1(token)
    for i in range(len(0,result)):
        if result[i] == dm_id:
            error_present = False

    if error_present = True:
        raise Exception("AccessError")


    #Now that errors are fixed, can invite user to DM


    return {}

#Ethan
@app.route('/dm/leave/v1', methods = ['POST'])
def dm_leave_v1(token, dm_id):
#Given a DM ID, user is removed as a member of this DM

    #Raises InputError when dm_id is not valid
    if dm_id < 0 or dm_id > len(dm_list):
        raise Exception("InputError")

    # Access error if user is not a member of token
    error_present = True
    # Loop through dm list of token or auth user
    # If dm_id is found then change it to false
    result = dm_list_v1(token)
    for i in range(len(0, result)):
        if result[i] == dm_id:
            error_present = False

    if error_present = True:
        raise Exception("AccessError")

    #Now can remove user from DM with dm_id

    return {}

def dm_messages_v1(token, dm_id, start):
    pass