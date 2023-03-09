from time import sleep
from threading import Thread
import json

import uvicorn
from fastapi import FastAPI
from loguru import logger
from pika import BlockingConnection, ConnectionParameters

from views.browser import browser_router
from views.main import main_router
from config import my_host, rabbit_host, queue_tasks_name


logger.add("data.log", rotation="100 MB")

app = FastAPI()
app.include_router(browser_router)
app.include_router(main_router)


def parse_page(ch, method, properties, body):
    data = json.loads(body.decode("utf-8"))
    print(data)


def starter():
    while True:
        try:
            connection = BlockingConnection(
                ConnectionParameters(host=rabbit_host, heartbeat=0)
            )
            channel = connection.channel()
            channel.queue_declare(queue=queue_tasks_name)
            channel.basic_consume(
                queue=queue_tasks_name,
                on_message_callback=parse_page,
                auto_ack=True
            )
            logger.info('ran pika listener')
            channel.start_consuming()
        except Exception as e:
            logger.exception(e)
            sleep(5)


@app.on_event("startup")
async def main():
    rabbit = Thread(target=starter)
    rabbit.start()


if __name__ == "__main__":
    uvicorn.run(app, host=my_host, port=8000)
