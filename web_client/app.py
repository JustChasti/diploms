import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from loguru import logger
from config import my_host
from views.main import main_router


logger.add("data.log", rotation="100 MB", enqueue=True)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(main_router)


# if __name__ == "__main__":
#     uvicorn.run(app, host=my_host, port=80)
