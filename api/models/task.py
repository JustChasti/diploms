import json
import bcrypt
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
    password: str
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    parse_time: Optional[datetime] = None
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
            '_id': ObjectId(self.user_id),
            'password': bcrypt.hashpw(
                self.password.encode('utf-8'),
                encrytp_salt
            ).decode('utf-8')
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
        estimated_time, max_time = self.get_uncomplited_time()
        return {
            'message': f'Task {task_id} added, estimated waiting time: {estimated_time} seconds, maximum waiting time {max_time} seconds',
            'task_id': str(task_id),
            'estimated': estimated_time,
            'maximum': max_time
        }

    @default_decorator('add task error')
    def add_task(self):
        self.created_at = datetime.now()
        self.completed_at = datetime.now() + timedelta(days=7)
        if not self.chek_task_user():
            return {
                'message': 'No users with this id and password'
            }
        id = self.add_to_base()
        if id:
            return self.add_to_rabbitmq(id)
        else:
            return {
                'message': 'you cannot add more than 2 identical tasks in 12 hours if the previous task has not been completed'
            }

    @default_decorator('get tasks time error')
    def get_uncomplited_time(self):
        task_filtered = tasks.find({
            'created_at': {"$gt": datetime.now() - timedelta(hours=12)},
            'complete': False,
        })
        max_time = int(len(list(task_filtered))) * 15
        authors = task_filtered.distinct('user_id')
        unic_authors = set(authors)
        estimated_time = 15
        print(authors)
        for i in unic_authors:
            completed_tasks = tasks.find({
                'user_id': i
            })
            author_estimated = 0
            for task_time in  completed_tasks.distinct('parse_time'):
                if task_time:
                    author_estimated += task_time
            estimated_time += int(author_estimated/len(list(completed_tasks)))
        return [estimated_time, max_time]


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
            'created_at': str(task['created_at']),
            'parse_time': str(task['parse_time']),
            'element': task['element'],
            'element_type': task['element_type']

        }
        return retur_html_file(path=f"{page_dir}/{task_id}.html", headers=headers)

    else:
        return JSONResponse({
            'error': 'there is no any completed task, with this parameters'
        })
