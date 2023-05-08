import uvicorn
from fastapi import FastAPI
from loguru import logger
from proxy_checker.check import check


logger.add("data.log", rotation="100 MB", enqueue=True)

app = FastAPI()


if __name__ == "__main__":
    pass
