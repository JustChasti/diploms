from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from config import my_host
from forms.sign import LoginForm


main_router = APIRouter()
main_router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@main_router.get('/')
async def main(request: Request):
    return templates.TemplateResponse(
        "main.html",
        {
            "request": request, 
            "home": "/", 
            "api": "/api",
            "pricing": "/pricing",
            "about": "/about",
            "login": "/login",
            "signup": "/signup",
        }
    )


@main_router.get('/login')
async def login(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request, 
            "home": "/", 
            "api": "/api",
            "pricing": "/pricing",
            "about": "/about",
            "login": "/login",
            "signup": "/signup",
        }
    )


@main_router.get('/about')
async def login(request: Request):
    return templates.TemplateResponse(
        "about.html",
        {
            "request": request, 
            "home": "/", 
            "api": "/api",
            "pricing": "/pricing",
            "about": "/about",
            "login": "/login",
            "signup": "/signup",
        }
    )


@main_router.get('/signup')
async def signup(request: Request):
    return templates.TemplateResponse(
        "registration.html",
        {
            "request": request, 
            "home": "/", 
            "api": "/api",
            "pricing": "/pricing",
            "about": "/about",
            "login": "/login",
            "signup": "/signup",
        }
    )


@main_router.post('/login')
async def login_analys(request: Request):
    form = LoginForm(request)
    await form.load_data()
    if form.login == 'chastytim@mail.ru':
        return RedirectResponse('/api')
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request, 
            "error_name": "Ошибка 0", 
            "error_text": "Текст ошибки 0",
        }
    )


@main_router.post('/signup')
async def signup_analys(request: Request):
    form = LoginForm(request)
    await form.load_data()
    if form.login == 'chastytim@mail.ru':
        return RedirectResponse('/api')
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request, 
            "error_name": "Ошибка 0", 
            "error_text": "Текст ошибки 0",
        }
    )

