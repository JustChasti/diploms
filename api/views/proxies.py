from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.user import UserModel
from config import admin_password


proxy_router = APIRouter()


@proxy_router.post('/give_proxy', response_class=JSONResponse)
async def give_proxy(user: UserModel):
    pass