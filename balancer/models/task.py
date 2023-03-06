from typing import Literal
from pydantic import BaseModel, validator
from db.db import users


class TaskModel(BaseModel):
    user_id: str
    url: str
    element_type: Literal('CLASS_NAME', 'CSS_SELECTOR', 'XPATH')
    element: str
    complete: False
