from asyncio import sleep
from bson.objectid import ObjectId
from loguru import logger

from db.db import hosts, tasks
from db.state_machine import StateMachine


async def get_html(host, task):
    # Task scheme
    # task_id, url, type, element
    print(0, host['hostname'], task['url'])
    StateMachine.set_state(host['hostname'], False)
    await sleep(15)
    tasks.update_one(
        {'_id': ObjectId(task['task_id'])},
        {"$set": {'complete': True}}
    )
    StateMachine.set_state(host['hostname'], True)
    print(1, host['hostname'], task['url'])
