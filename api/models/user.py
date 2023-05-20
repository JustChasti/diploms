import bcrypt
from pydantic import BaseModel, validator
from bson import ObjectId
from db.db import users, proxies, tasks
from modules.decorators import default_decorator
from config import encrypt_salt
from models.token import Token, generate_ac_token, decode_token, check_valid_token


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
            refresh_token = Token(user.inserted_id).generate_refr_token()
            access_token = generate_ac_token(refresh_token)
            return {'access_token': access_token, 'refresh_token': refresh_token}
        
    @default_decorator('error in login')
    def login_user(self, user_id):
        refresh_token = Token(user_id).generate_refr_token()
        access_token = generate_ac_token(refresh_token)
        return {'access_token': access_token, 'refresh_token': refresh_token}
    

@default_decorator('Error in find user')
def get_user_data(access_token):
    data = decode_token(access_token)
    if check_valid_token(data, 'access'):
        user = users.find_one({
            '_id': ObjectId(data['id'])
        })
        if user:
            response = {
                'id': data['id'],
                'username': user['username']
            }
            response['count_max_proxies'] = proxies.count_documents({})
            count_banned_proxies = 0
            # for i in proxies.find({}):
            #     if ObjectId(data['id']) in i['ban_list']:
            #         count_banned_proxies += 1
            # response['count_banned_proxies'] = count_banned_proxies
            response['count_banned_proxies'] = proxies.count_documents({"ban_list": ObjectId(data['id'])})
            return response
        else:
            return {'info': 'token invalid'}
    else:
        return {'info': 'token invalid'}
