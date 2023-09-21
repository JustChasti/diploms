from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.user import UserModel, get_user_data
from models.token import generate_ac_token
from config import admin_password


main_router = APIRouter()


@main_router.post('/add_user', response_class=JSONResponse)
async def add_user(user: UserModel):
    if True:  # a_password == admin_password:
        tokens = user.add_user()
        if tokens:
            return {
                'info': "This user has been added",
                'tokens': tokens
            }
        else:
            return {
                'info': "Adding user error",
                'tokens': tokens
            }
    else:
        return {
                'info': "Adding user error, passwords didn't match",
                'tokens': False
            }
    

@main_router.post('/login', response_class=JSONResponse)
async def login(user: UserModel):
    user_id = user.get_id()
    if user_id:
        return user.login_user(user_id)
    else:
        return {
            'info': "No user with that login and password"
        }
    

@main_router.get('/refresh', response_class=JSONResponse)
async def refresh(refresh_token: str):
    access_token = generate_ac_token(refresh_token)
    return {'access_token': access_token}


@main_router.get('/user_info/{access_token}', response_class=JSONResponse)
async def get_user(access_token: str):
    return get_user_data(access_token)
