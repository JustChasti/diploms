from fastapi import APIRouter
from fastapi.responses import JSONResponse, FileResponse
from source.mongo import get_all_articles


article_router = APIRouter()


@article_router.get('/article/categories', response_class=JSONResponse)
async def get_categories():  # получение категорий
    return {'info': 'data'}


@article_router.get('/article/{category}', response_class=JSONResponse)
async def find_article_category(category):  # получение статей по категории
    return {'info': 'data'}


@article_router.get('/articles', response_class=FileResponse)
async def get_articles():  # получение всех статей из базы
    filename = get_all_articles()
    return FileResponse(path=filename, filename=filename)
