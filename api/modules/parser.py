import codecs
from loguru import logger
from bson.objectid import ObjectId
from datetime import datetime

from db.db import tasks
from db.state_machine import StateMachine
from modules.extractor import extract
from modules.decorators import default_decorator
from config import page_dir


@default_decorator('error in getting html')
async def get_html(host, task):
    StateMachine.set_state(host['hostname'], False)
    started_at = datetime.now()
    try:
        data = extract(
            url=task['url'], hostname=host['hostname'],
            tag_type=task['type'], tag_name=task['element']
        )
    except Exception as e:
        data = f'<p>{e}<p>'
    with open(
        file=f'{page_dir}/{task["task_id"]}.html',
        mode="w",
        encoding="utf−8"
    ) as file:
        file.write(data)
    tasks.update_one(
        {'_id': ObjectId(task['task_id'])},
        {"$set": {
            'complete': True,
            'parse_time': int((datetime.now() - started_at).seconds),
            'completed_at': datetime.now()
            }
        }
    )
    StateMachine.set_state(host['hostname'], True)
