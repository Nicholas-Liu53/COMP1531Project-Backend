import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
import src.data
import src.auth, src.other, src.dm

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
    
@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages_v1():
    token, channel_id, start = request.args.get('token'), request.args.get('channel_id'), request.args.get('start')
    return src.dm.dm_messages_v1(token, int(channel_id), int(start))

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
   payload = request.get_json()
   return src.dm.dm_remove_v1(payload.get('token'), payload.get('dm_id'))

@APP.route("/dm/invite/v1", methods=['POST'])
def dm_invite():
    payload = request.get_json()
    return src.dm.dm_invite_v1(payload.get('token'), payload.get('dm_id'), payload.get('u_id'))

@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave():
    payload = request.get_json()
    return src.dm.dm_leave_v1(payload.get('token'), payload.get('dm_id'))
    
@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages():
    token, dm_id, start = request.args.get('token'), request.args.get('dm_id'), request.args.get('start')
    return src.dm.dm_messages_v1(token, int(dm_id), int(start))

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
