from datetime import datetime, timedelta
import jwt
from modules.decorators import default_decorator
from config import encrypt_salt, ACCESS_TOKEN_EXPIRE_DAYS
from config import REFRESH_TOKEN_EXPIRE_DAYS, SECRET_KEY, ALGORITHM


@default_decorator('error in decoding token')
def decode_token(token):
        data = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return data


def check_valid_token(data, token_type):
     try:
        if data['type'] == token_type and datetime.fromtimestamp(data['exp']) > datetime.now():
            return True
        return False
     except Exception as e:
        return False 


@default_decorator('error in generating token')
def generate_ac_token(token):
    data = decode_token(token)
    if data:
        if check_valid_token(data, 'refresh'):
            expire = datetime.now() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
            to_encode = {
                'id': data['id'],
                'exp': expire,
                'type': 'access'
            }
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            return encoded_jwt
    return False


class Token():
    user_id: str

    def __init__(self, user_id):
        self.user_id = user_id
    
    @default_decorator('error in generating token')
    def generate_refr_token(self):
        expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode = {
            'id': str(self.user_id),
            'exp': expire,
            'type': 'refresh'
        }
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
