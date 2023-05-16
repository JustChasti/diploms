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


@main_router.get('/api')
async def signup(request: Request):
    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')
    # здесь отправляем запрос на получение пользователя
    # если он пишет что токен истек обновляем acces_token
    if access_token and refresh_token:
        user_login = 'chastytim@mail.ru'
        user_id = 'abc1234dd'
        tasks = 3
        proxies = 5
        proxies_max = 20
        return templates.TemplateResponse(
            "api.html",
            {
                "request": request, 
                "home": "/", 
                "api": "/api",
                "pricing": "/pricing",
                "about": "/about",
                "login": "/login",
                "signup": "/signup",
                "user_login": user_login,
                "user_id": user_id,
                "tasks": tasks,
                "proxies": proxies,
                "proxies_max": proxies_max
            }
        )
    else:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request, 
                "error_name": "Ошибка авторизации", 
                "error_text": "Вы не авторизованы, войдите в систему",
            }
        )



@main_router.post('/login')
async def login_analys(request: Request):
    form = LoginForm(request)
    await form.load_data()
    if form.login == 'chastytim@mail.ru':  # тут идет запрос к api
        response = RedirectResponse('/api', 303)
        response.set_cookie(key="access_token", value="auth - jwt token")
        response.set_cookie(key="refresh_token", value="refr - jwt token")
        return response
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request, 
            "error_name": "Ошибка Авторизации", 
            "error_text": "Вы не авторизованы",
        }
    )


@main_router.post('/signup')
async def signup_analys(request: Request):
    form = LoginForm(request)
    await form.load_data()
    if form.login == 'chastytim@mail.ru':  # тут идет запрос к api
        response = RedirectResponse('/api', 303)
        response.set_cookie(key="auth_token", value="auth - jwt token")
        response.set_cookie(key="refr_token", value="refr - jwt token")
        return response
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request, 
            "error_name": "Ошибка 0", 
            "error_text": "Текст ошибки 0",
        }
    )

