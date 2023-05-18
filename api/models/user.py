import bcrypt
from pydantic import BaseModel, validator
import jwt
from datetime import datetime, timedelta
from db.db import users
from modules.decorators import default_decorator
from config import encrypt_salt, ACCESS_TOKEN_EXPIRE_DAYS, REFRESH_TOKEN_EXPIRE_DAYS


class Token():
    user_id: str
    days: int
    token_type: str


    def __init__(self, user_id, days, token_type):
        self.user_id = user_id
        self.days = days
        self.token_type = token_type

    @default_decorator('error in generating token')
    def generate_token(self):
        expire = datetime.now() + timedelta(days=self.days)
        to_encode = {
            'id': self.user_id,
            'type': self.token_type,
        }
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


class UserModel(BaseModel):
    username: str
    password: str

    @default_decorator('Error in find user')
    def find_user(self):
        user = users.find_one({
            'username': self.username
        })
        if user:
            return True
        else:
            return False

    @default_decorator('Error in find user')
    def get_id(self):
        self.password = bcrypt.hashpw(
            self.password.encode('utf-8'),
            encrypt_salt
        ).decode('utf-8')
        user = users.find_one({
            'username': self.username,
            'password': self.password
        })
        if user:
            return user['_id']
        else:
            return False

    @default_decorator('error in add user')
    def add_user(self):
        if self.find_user():
            return False
        else:
            self.password = bcrypt.hashpw(
                self.password.encode('utf-8'),
                encrypt_salt
            ).decode('utf-8')
            user = users.insert_one(
                self.__dict__
            )
            return user.inserted_id

    
    @default_decorator('token creation error')
    def create_r_token(self, type):
        user = self.get_id()
        if user:
            pass
        else:
            return {'refresh_token': 0}
