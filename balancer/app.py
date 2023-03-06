import uvicorn
from fastapi import FastAPI
from loguru import logger

from views.browser import browser_router
from config import my_host


logger.add("data.log", rotation="100 MB")

app = FastAPI()
app.include_router(browser_router)


@app.on_event("startup")
async def main():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host=my_host, port=8000)
