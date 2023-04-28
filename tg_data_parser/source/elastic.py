from datetime import datetime
from time import sleep
from bson.objectid import ObjectId

from loguru import logger
from elasticsearch import Elasticsearch
from config import elastic_host, elastic_index


def add_article(channel_id: ObjectId, article_text: str) -> bool:
    # добавляет статью в базу
    es = Elasticsearch(elastic_host)
    data = {
        'channel_id': str(channel_id),
        'timestamp': datetime.now(),
        'text': article_text
    }
    while True:
        try:
            result = es.search(
                index=elastic_index, query={"match": {"text": article_text}}
            )
            break
        except Exception as e:
            logger.warning('Cant connect to elasic')
            sleep(5)
    if result:
        return False
    resp = es.index(index=elastic_index, document=data)
    print(resp.body)
    return True
    # terms = es.termvectors()
