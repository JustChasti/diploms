from pydantic import BaseModel, validator
from db.db import users


class UserModel(BaseModel):
    email: str
