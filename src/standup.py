#File for implementation of standup functions 
from src.error import AccessError, InputError
from src.other import decode, get_channel, generate_new_message_id, get_user
from datetime import datetime
import json
import threading, time

AuID     = 'auth_user_id'
uID      = 'u_id'
cID      = 'channel_id'
chans    = 'channels'

def standup_start_v1(token, channel_id, length):
    auth_user_id, _ = decode(token)
    #* If Channel ID is not a valid channel, then an InputError is raised
    #* If authorised user is not in the channel, an AccessError is raised
    if auth_user_id not in get_channel(channel_id)['all_members']:
        raise AccessError
    elif standup_active_v1(token, channel_id)['is_active']:
        raise InputError

    with open('data.json', 'r') as FILE:
        data = json.load(FILE)

    now = datetime.now()
    time_finish = int(now.strftime("%s")) + length

    new_stand_up = {
        'channel_id': channel_id,
        'time_finish': time_finish,
        'messages': []
    }
    data['stand_ups'].append(new_stand_up)
    with open('data.json', 'w') as FILE:
        json.dump(data, FILE)
    
    threading.Timer(length, stand_up_push, args=(auth_user_id, channel_id)).start()
    return {
        'time_finish': time_finish
    }

def standup_active_v1(token, channel_id):
    _, _ = decode(token)
    #* If Channel ID is not a valid channel, then an InputError is raised
    get_channel(channel_id)
    with open('data.json', 'r') as FILE:
        data = json.load(FILE)
    
    for stand_up in data['stand_ups']:
        if channel_id == stand_up[cID]:
            return {
                'is_active': True,
                'time_finish': stand_up['time_finish']
            }
    return {
            'is_active': False,
            'time_finish': None
        }

#* Append string with "handle: message" to stand_up messages
def standup_send_v1(token, channel_id, message):
    auth_user_id, _ = decode(token)
    if auth_user_id not in get_channel(channel_id)['all_members']:
        raise AccessError
    elif not standup_active_v1(token, channel_id)['is_active']:
        raise InputError
    elif len(message) > 1000:
        raise InputError

    with open('data.json', 'r') as FILE:
        data = json.load(FILE)

    for stand_up in data['stand_ups']:
        if channel_id == stand_up[cID]:
            stand_up['messages'].append(f"{get_user(auth_user_id)['handle_str']}: {message}")

    with open('data.json', 'w') as FILE:
        json.dump(data, FILE)

    return {}

#* Function which is run at the end of the standup
#* Compiles messages into one big string
#* Removes the stand_up dictionary
def stand_up_push(auth_user_id, channel_id):
    with open('data.json', 'r') as FILE:
        data = json.load(FILE)

    for index, stand_up in enumerate(data['stand_ups']):
        if stand_up[cID] == channel_id:
            target = data['stand_ups'].pop(index)
            message = "\n".join(target['messages'])

    now = datetime.now()
    time_created = int(now.strftime("%s"))
    newID = generate_new_message_id()

    data['messages_log'].append(
        {
            'channel_id'    : channel_id,
            'dm_id'         : -1,
            'u_id'          : auth_user_id,
            'time_created'  : time_created,
            'message_id'    : newID,
            'message'       : message,
            'reacts': [],
            'is_pinned': False,
        }
    )

    with open('data.json', 'w') as FILE:
        json.dump(data, FILE)
