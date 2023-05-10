import bcrypt
from pydantic import BaseModel, validator
from db.db import users
from modules.decorators import default_decorator


class UserModel(BaseModel):
    email: str
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
            encrytp_salt
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
                encrytp_salt
            ).decode('utf-8')
            user = users.insert_one(
                self.__dict__
            )
            return user.inserted_id
