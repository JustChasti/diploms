from time import sleep
from bson.objectid import ObjectId
from time import sleep
from loguru import logger

from db.db import hosts, tasks


def get_html(host, task):
    # Task scheme
    # task_id, url, type, element
    hosts.update_one({'_id': ObjectId(host['_id'])}, {"$set": {'locked': True}})
    sleep(15)
    tasks.update_one({'_id': ObjectId(task['task_id'])}, {"$set": {'complete': True}})
    hosts.update_one({'_id': ObjectId(host['_id'])}, {"$set": {'locked': False}})
