from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.user import UserModel
from config import admin_password


main_router = APIRouter()


@main_router.post('/add-user', response_class=JSONResponse)
async def add_user(user: UserModel, a_password: str):
    if a_password == admin_password:  # переделать проверку пароля
        id = user.add_user()
        if id:
            return {
                'info': "This user has been added",
                'user_id': str(id)
            }
        else:
            return {
                'info': "Adding user error",
                'user_id': id
            }
    else:
        return {
                'info': "Adding user error, passwords didn't match",
                'user_id': False
            }


@main_router.get('/user_id/{username}/{password}', response_class=JSONResponse)
async def get_user(username: str, password: str):
    user = UserModel(email='', username=username, password=password)
    id = user.get_id()
    if id:
        return {'id': str(id)}
    else:
        return {'id': 0}
