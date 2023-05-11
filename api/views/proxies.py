from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.user import UserModel
from config import admin_password
from db.db import get_available_proxy, ban_user_proxy
from modules.proxy_checker import add_new_proxy


proxy_router = APIRouter()


@proxy_router.post('/give_proxy', response_class=JSONResponse)
async def give_proxy(user: UserModel):
    user_id = user.get_id()
    if user_id:
        return get_available_proxy(user_id)
    else:
        return {'info': 'No user with that login and password'}


@proxy_router.post('/expire_proxy', response_class=JSONResponse)
async def expire_proxy(user: UserModel, address):
    user_id = user.get_id()
    if user_id:
        return ban_user_proxy(user_id, address)
    else:
        return {'info': 'No user with that login and password'}


@proxy_router.post('/add_proxy', response_class=JSONResponse)
async def add_proxy(admin_pass, address, port):
    if admin_pass == admin_password:
        return add_new_proxy(address, port)
    else:
        return {'info': 'password incorrect'}
