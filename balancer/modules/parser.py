from asyncio import sleep
from bson.objectid import ObjectId
from loguru import logger

from db.db import hosts, tasks


async def get_html(host, task):
    # Task scheme
    # task_id, url, type, element
    print(0, host['hostname'], task['url'])
    hosts.update_one({'_id': ObjectId(host['_id'])}, {"$set": {'locked': True}})
    await sleep(15)
    tasks.update_one({'_id': ObjectId(task['task_id'])}, {"$set": {'complete': True}})
    hosts.update_one({'_id': ObjectId(host['_id'])}, {"$set": {'locked': False}})
    print(1, host['hostname'], task['url'])
