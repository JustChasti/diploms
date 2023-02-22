from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates


auth_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@auth_router.get('/auth/registration')
async def registrate_user(request: Request):
    return templates.TemplateResponse(
        "registration.html",
        {"request": request}
    )


@auth_router.post('/auth/registration')
async def registrate_user(request: Request):
    return templates.TemplateResponse(
        "registration.html",
        {"request": request}
    )
