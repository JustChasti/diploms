from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.task import TaskModel


browser_router = APIRouter()


@browser_router.post('/add-task', response_class=JSONResponse)
async def get_data(task: TaskModel):
    return task.add_task()
