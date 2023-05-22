from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from config import my_host
from forms.sign import LoginForm
from source.server_reqs import sign_in, sign_up, get_user_info


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


@main_router.get('/api')
async def signup(request: Request):
    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')
    data = get_user_info(access_token, refresh_token)
    if data:
        if len(data) == 2:
            access_token = data[1]
        data = data[0]    
        user_login = data['username']
        user_id = data['id']
        tasks = data['count_tasks']
        proxies = data['count_banned_proxies']
        proxies_max = data['count_max_proxies']
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
    data = sign_in(form.login, form.password)
    if data:
        response = RedirectResponse('/api', 303)
        response.set_cookie(key="access_token", value=data[0])
        response.set_cookie(key="refresh_token", value=data[1])
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
    data = sign_up(form.login, form.password)
    if data:
        response = RedirectResponse('/api', 303)
        response.set_cookie(key="access_token", value=data[0])
        response.set_cookie(key="refresh_token", value=data[1])
        return response
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request, 
            "error_name": "Ошибка Создания пользователя", 
            "error_text": "Скорее всего пользователь с таким именем уже существует",
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

