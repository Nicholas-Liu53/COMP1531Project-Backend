import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
import src.auth, src.other

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
    print(src.data.users)
    payload = request.get_json()
    return dumps(
        src.auth.auth_register_v2(payload['email'], payload['password'], payload['name_first'], payload['name_last'])
    )
    

@APP.route("/auth/login/v2", methods=['POST'])
def auth_login():
    print(src.data.users)
    payload = request.get_json()
    return dumps(
        src.auth.auth_login_v2(payload['email'], payload['password'])
    )

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
