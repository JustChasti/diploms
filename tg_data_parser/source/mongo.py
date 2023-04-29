from time import sleep
from pymongo import MongoClient
from loguru import logger
import aiochan as ac
from config import base_host, base_port, client_name, channels
from source.nlp import get_keywords


while True:
    try:
        client = MongoClient(
            base_host, base_port
        )[client_name]
        channels_list = client['channels']
        articles_list = client['articles']
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


def add_new_article(channel_id, text):
    result = articles_list.insert_one(document={
            'channel_id': channel_id,
            'text': text
        }
    )
    return result.inserted_id


async def add_articles(channel_id, articles):
    for i in articles:
        print(i)
        article = articles_list.find_one({'text': i})
        if not article:
            c = ac.Chan()
            ac.go(
                get_keywords(
                    channel=c,
                    text=i
                )
            )
            article = add_new_article(channel_id, i)
            key_words = await c.get()
            logger.info(key_words)
