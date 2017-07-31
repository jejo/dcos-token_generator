import json
from datetime import datetime, timedelta
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from jwt.utils import base64url_decode, bytes_to_number

import jwt
import sys
import requests
import time


AUTH_TOKEN = None
TOKEN_REFRESH = 60
TOKEN_REFRESH_TIME = None


def main(args):
    generate_auth_token(args[1])

def generate_auth_token(config):
    with open(config, 'r') as fh:
        conf = json.load(fh)

    jwt_payload = {'uid': conf['uid'], 'exp': (datetime.utcnow() + timedelta(seconds=300))}
    login_token = jwt.encode(jwt_payload, conf['private_key'], algorithm='RS256').decode()

    login_payload = json.dumps({'uid': conf['uid'], 'token': login_token})
    #print "LOGIN_PAYLOAD: " +  login_payload

    global AUTH_TOKEN
    AUTH_TOKEN = requests.post(conf['login_endpoint'],
                              headers={'content-type': 'application/json'},
                               data=login_payload,verify=False).json()['token']

    print "AUTH_TOKEN: " + AUTH_TOKEN

if __name__ == '__main__':
    main(sys.argv)        
