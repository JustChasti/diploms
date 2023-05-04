from fastapi import APIRouter
from fastapi.responses import JSONResponse


channels_router = APIRouter()


@channels_router.post('/channel/add', response_class=JSONResponse)
async def add_channel():  # добавление нового канала
    return {'info': 'data'}


@channels_router.delete('/channel/delete/{name}', response_class=JSONResponse)
async def remove_channel(name):  # удаление канала
    return {'info': 'data'}
