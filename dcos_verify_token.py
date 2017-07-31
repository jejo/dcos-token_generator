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
    verify_token(args[1], args[2])
    

def verify_token(masterUrl, authToken):
    keys = requests.get('https://'+ masterUrl +'/acs/api/v1/auth/jwks',verify=False).json()['keys'][0]

    exponent_bytes = base64url_decode(keys['e'].encode('ascii'))
    exponent_int = bytes_to_number(exponent_bytes)

    modulus_bytes = base64url_decode(keys['n'].encode('ascii'))
    modulus_int = bytes_to_number(modulus_bytes)

    public_numbers = rsa.RSAPublicNumbers(n=modulus_int, e=exponent_int)
    public_key = public_numbers.public_key(backend=default_backend())

    payload = jwt.decode(authToken, public_key, algorithm='RS256')

    print payload
    print "expiration is: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(payload['exp']))

    
if __name__ == '__main__':
    main(sys.argv)        
