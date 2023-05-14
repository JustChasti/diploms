from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from config import my_host


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