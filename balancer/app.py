from time import sleep
from threading import Thread
import json
from multiprocessing import Process
from bson.objectid import ObjectId

import uvicorn
from fastapi import FastAPI
from loguru import logger
from pika import BlockingConnection, ConnectionParameters

from views.browser import browser_router
from views.main import main_router
from config import my_host, rabbit_host, queue_tasks_name
from db.db import create_host_list, hosts
from modules.parser import get_html


logger.add("data.log", rotation="100 MB", enqueue=True)

app = FastAPI()
app.include_router(browser_router)
app.include_router(main_router)


def assign_task(ch, method, properties, body):
    task = json.loads(body.decode("utf-8"))
    while True:
        host = hosts.find_one({'locked': False})
        logger.info(f"{host['hostname']} / {task['task_id']}")
        if host:
            break
        else:
            sleep(1)

    host_thread = Process(target=get_html, args=(host, task))
    host_thread.start()


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
                on_message_callback=assign_task,
                auto_ack=True
            )
            logger.info('ran pika listener')
            channel.start_consuming()
        except Exception as e:
            logger.exception(e)
            sleep(5)


@app.on_event("startup")
async def main():
    create_host_list()
    rabbit = Thread(target=starter)
    rabbit.start()


if __name__ == "__main__":
    uvicorn.run(app, host=my_host, port=8000)
