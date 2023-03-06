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

    @default_decorator('error in add user')
    def add_user(self):
        if self.find_user():
            users.insert_one({
                self.__dict__
            })
