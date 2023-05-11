from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates


main_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@main_router.get('/')
async def main(request: Request):
    return templates.TemplateResponse(
        "main.html",
        {"request": request}
    )