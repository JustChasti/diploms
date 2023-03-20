from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.task import TaskModel


browser_router = APIRouter()


@browser_router.post('/add-task', response_class=JSONResponse)
async def add_new_task(task: TaskModel):
    return task.add_task()


@browser_router.get('/get-task/{user_id}/{task_id}')
async def get_task(user_id, task_id):
    pass
