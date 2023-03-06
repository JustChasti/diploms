from fastapi import APIRouter
from fastapi.responses import JSONResponse


browser_router = APIRouter()


@browser_router.post('/add-task', response_class=JSONResponse)
async def get_data(url: str):
    return {
        'info': "Can't find this city on openweathermap.org",
        'city': {'name': url}
    }
