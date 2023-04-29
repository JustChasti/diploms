from threading import Thread
from time import sleep
import asyncio

import uvicorn
from fastapi import FastAPI
from loguru import logger
from telethon.sync import TelegramClient, events
from config import api_hash, api_id, phone

from config import my_host, get_info_delay
from crawler.data_crawler import crawl_channel
from views.articles import article_router
from views.channels import channels_router
from source.mongo import channels_list, add_example_channels, add_articles
import aiochan as ac


logger.add("data.log", rotation="100 MB", enqueue=True)
app = FastAPI()

app.include_router(article_router)
app.include_router(channels_router)


def daemon():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError as e:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    client = TelegramClient('session1', api_id, api_hash)
    print(0)
    try:
        client.connect()
        client.start(phone=phone)
    except Exception as e:
        logger.exception('Cant connect to tg')
    print(1)
    while True:
        add_example_channels()
        channels = channels_list.find({})
        for i in channels:
            data = crawl_channel(client, i['link'])
            print(i)
            ac.run(add_articles(channel_id=i['_id'], article_text=data))
            break
        sleep(get_info_delay * 60)


@app.on_event("startup")
async def main():
    daemon_thread = Thread(target=daemon)
    daemon_thread.start()


if __name__ == "__main__":
    uvicorn.run(app, host=my_host, port=8000)
