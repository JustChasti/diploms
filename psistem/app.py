import requests
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from loguru import logger
from modules.main import db
from views.auth import auth_router


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
logger.add("test.log", rotation="100 MB")
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
