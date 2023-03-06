from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.user import UserModel


main_router = APIRouter()


@main_router.post('/add-user', response_class=JSONResponse)
async def add_user(user: UserModel):
    return {
        'info': "Can't find this city on openweathermap.org",
        'city': {'name': url}
    }