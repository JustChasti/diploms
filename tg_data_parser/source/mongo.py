from time import sleep
from pymongo import MongoClient
from loguru import logger
from config import base_host, base_port, client_name, channels


while True:
    try:
        client = MongoClient(
            base_host, base_port
        )[client_name]
        channels_list = client['channels']
        break
    except Exception as e:
        logger.exception(e)
        sleep(5)


def add_example_channels():
    for i in channels:
        channels_list.update_one(
            filter={
                'link': i
            },
            update={"$set": {
                'link': i
            }},
            upsert=True
        )


def add_article(channel_id, article_text) -> bool:
    pass
