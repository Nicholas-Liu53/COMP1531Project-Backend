import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
import src.data
import src.auth, src.other, src.dm, src.notifications, src.channel, src.channels, src.message

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    src.other.clear_v1()
    return {}

@APP.route("/auth/register/v2", methods=['POST'])
def auth_register():
    payload = request.get_json()
    return src.auth.auth_register_v2(payload['email'], payload['password'], payload['name_first'], payload['name_last'])

@APP.route("/auth/login/v2", methods=['POST'])
def auth_login():
    payload = request.get_json()
    return src.auth.auth_login_v2(payload['email'], payload['password'])

@APP.route("/dm/details/v1", methods=['GET'])
def dm_details():
    token, dm_id = request.args.get('token'), request.args.get('dm_id')
    return src.dm.dm_details_v1(token, int(dm_id))

@APP.route("/dm/list/v1", methods=['GET'])
def dm_list():
    token = request.args.get('token')
    return src.dm.dm_list_v1(token)

@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    payload = request.get_json()
    return src.dm.dm_create_v1(payload.get('token'), payload.get('u_ids'))

@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove():
    pass

@APP.route("/dm/invite/v1", methods=['POST'])
def dm_invite():
    pass

@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave():
    pass

@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages():
    pass

@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    payload = request.get_json()
    return src.channel.channel_join_v1(payload['token'], payload['channel_id'])

@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    payload = request.get_json()
    return src.channel.channel_leave_v1(payload['token'], payload['channel_id'])

@APP.route("/channels/create/v2", methods=['POST'])
def channels_create():
    payload = request.get_json()
    return src.channels.channels_create_v1(payload['token'], payload['name'], payload['is_public'])

@APP.route("/channels/list/v2", methods=['GET'])
def channels_list():
    token = request.args.get('token')
    return src.channels.channels_list_v2(token)

@APP.route("/channels/listall/v2", methods=['GET'])
def channels_listall():
    token = request.args.get('token')
    return src.channels.channels_listall_v2(token)

@APP.route("/message/send/v2", methods=['POST'])
def message_send():
    payload = request.get_json()
    return src.message.message_send_v1(payload['token'], payload['channel_id'], payload['message'])

@APP.route("/message/edit/v2", methods=['PUT'])
def message_edit():
    payload = request.get_json()
    return src.message.message_edit_v1(payload['token'], payload['message_id'], payload['message'])

@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    payload = request.get_json()
    return src.message.message_remove_v1(payload['token'], payload['message_id'])

@APP.route("/notifications/get/v1", methods=['GET'])
def notifications_get():
    token = request.args.get('token')
    return src.notifications.notifications_get_v1(token)

@APP.route("/search/v2", methods=['GET'])
def search():
    token, query_str = request.args.get('token'), request.args.get('query_str')
    return src.other.search_v1(token, query_str)

@APP.route("/user/profile/v2", methods=['GET'])
def user_profile():
    payload = request.get_json()
    return src.user.user_profile_v2(payload['token'], payload['u_id'])

@APP.route("/user/profile/setname/v2", methods=['PUT'])
def user_setname():
    payload = request.get_json()
    return src.user.user_setname_v2(payload['token'], payload['name_first'], payload['name_last'])

@APP.route("/user/profile/setemail/v2", methods=['PUT'])
def user_setemail():
    payload = request.get_json()
    return src.user.user_setname_v2(payload['token'], payload['email'])

@APP.route("/user/profile/sethandle/v2", methods=['PUT'])
def user_sethandle():
    payload = request.get_json()
    return src.user.user_setname_v2(payload['token'], payload['handle_str'])

@APP.route("/users/all/v1", methods=['GET'])
def users_all():
    payload = request.get_json()
    return src.user.users_all(payload['token'])


if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
