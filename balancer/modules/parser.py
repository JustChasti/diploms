import codecs
from bson.objectid import ObjectId

from db.db import tasks
from db.state_machine import StateMachine
from modules.extractor import extract
from modules.decorators import default_decorator
from config import page_dir


@default_decorator('error in getting html')
async def get_html(host, task):
    # Task scheme
    # task_id, url, type, element
    StateMachine.set_state(host['hostname'], False)
    try:
        data = extract(
            url=task['url'], hostname=host['hostname'],
            tag_type=task['type'], tag_name=task['element']
        )
    except Exception as e:
        data = f'<p>{e}<p>'
    file = codecs.open(f'{page_dir}/{task["task_id"]}.html', "w", "utf−8")
    file.write(data)
    file.close()
    tasks.update_one(
        {'_id': ObjectId(task['task_id'])},
        {"$set": {'complete': True}}
    )
    StateMachine.set_state(host['hostname'], True)
