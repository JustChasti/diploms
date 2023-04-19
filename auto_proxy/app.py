import uvicorn
from fastapi import FastAPI
from loguru import logger


logger.add("data.log", rotation="100 MB", enqueue=True)

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(app, host=my_host, port=8000)