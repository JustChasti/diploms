import json
from datetime import datetime, timedelta
import os
from pathlib import Path

from loguru import logger
from typing import Literal, Optional
from pydantic import BaseModel, validator
from bson.objectid import ObjectId
from pika import BlockingConnection, ConnectionParameters
from fastapi.responses import JSONResponse, FileResponse

from db.db import users, tasks
from modules.decorators import default_decorator
from config import rabbit_host, queue_tasks_name, page_dir


class TaskModel(BaseModel):
    user_id: str
    url: str
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    element_type: Literal['CLASS_NAME', 'CSS_SELECTOR', 'XPATH']
    element: str
    complete: bool = False

    @validator('created_at')
    def update_created(created_at):
        created_at = datetime.now()
        return created_at

    @validator('completed_at')
    def update_completed(completed_at):
        completed_at = datetime.now() + timedelta(days=7)
        return completed_at

    @default_decorator('find user error')
    def chek_task_user(self):
        user = users.find_one({
            '_id': ObjectId(self.user_id)
        })
        if user:
            return True
        else:
            return False

    @default_decorator('add to base error')
    def add_to_base(self):
        same_task = tasks.find_one({
            'url': self.url,
            'user_id': self.user_id,
            'complete': False,

        })
        # logger.info(self.created_at)
        if same_task:
            logger.info(same_task)
            if same_task['created_at'] + timedelta(hours=12) > datetime.now():
                return False

        task = tasks.insert_one(self.__dict__)
        return task.inserted_id

    @default_decorator('add to rabbit error')
    def add_to_rabbitmq(self, task_id):
        message = {
            'task_id': str(task_id),
            'url': self.url,
            'type': self.element_type,
            'element': self.element
        }
        connection = BlockingConnection(
                ConnectionParameters(rabbit_host)
            )
        channel = connection.channel()
        channel.queue_declare(queue=queue_tasks_name)
        channel.confirm_delivery()
        channel.basic_publish(
            exchange='',
            routing_key=queue_tasks_name,
            body=json.dumps(message)
        )
        connection.close()
        return {
            'message': f'Task {task_id} added, estimated waiting time: {0}, maximum waiting time {0}',
            'task_id': str(task_id),
            'estimated': 0,
            'maximum': 0
        }

    @default_decorator('add task error')
    def add_task(self):
        self.created_at = datetime.now()
        self.completed_at = datetime.now() + timedelta(days=7)
        if not self.chek_task_user():
            return {
                'message': 'No users with this id'
            }
        id = self.add_to_base()
        if id:
            return self.add_to_rabbitmq(id)
        else:
            return {
                'message': 'you cannot add more than 2 identical tasks in 12 hours if the previous task has not been completed'
            }


def retur_html_file(path, headers):
    # просто удалять файл после запроса нельзя, нужно создать клинер
    # fastapi пытается вернуть удаленный файл
    check = Path(path)
    if check.is_file():
        return FileResponse(path=path, headers=headers)
    return JSONResponse({
        'error': 'task not found error'
    })


@default_decorator('get task error')
def get_completed_task(user_id, task_id):
    task = tasks.find_one({
            '_id': ObjectId(task_id),
            'user_id': user_id,
            'complete': True,
    })
    if task:
        headers = {
            'task_id': str(task['_id']),
            'time': str(task['completed_at'] - task['created_at']),
            'element': task['element'],
            'element_type': task['element_type']

        }
        return retur_html_file(path=f"{page_dir}/{task_id}.html", headers=headers)

    else:
        return JSONResponse({
            'error': 'there is no any completed task, with this parameters'
        })
