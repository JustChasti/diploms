import requests
import uvicorn
from fastapi import FastAPI
from loguru import logger


app = FastAPI()
logger.add("test.log", rotation="100 MB")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
