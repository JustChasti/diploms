from time import sleep
from zipfile import ZipFile
from bson.json_util import dumps
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
        category_list = client['category']
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


def get_all_articles():
    with ZipFile('dump.zip', 'w') as myzip:
        articles = articles_list.find({})
        with open(f'articles.json', 'w', encoding="utf-8") as file:
            file.write('[')
            for document in articles:
                file.write(dumps(document, ensure_ascii=False))
                file.write(',')
            file.write(']')
        myzip.write(f"articles.json")

    return 'dump.zip'


async def add_articles(channel_id, articles):
    # keyword example: [('полезная табличка', 0.33), ('chatgpt', 0.21), ()]
    for i in articles:
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
            categories = category_list.find({})
            key_words = await c.get()
            articles_list.update_one(
                filter={
                    '_id': article
                },
                update={"$set": {
                    'keywords': key_words
                }},
                upsert=True
            )
            existing = False
            for category in category_list:
                result = 0
