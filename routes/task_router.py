from typing import Annotated

from models import TaskUpdate, TaskPublic, TaskCreate
from services import task_service

from fastapi import Depends, APIRouter, Request
from fastapi.security import OAuth2PasswordBearer

task_router = APIRouter(prefix="/task")

oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@task_router.get("/all", response_model=list[TaskPublic])
async def get_all_tasks(token: Annotated[str, Depends(oauth_scheme)]):
    return task_service.get_all(token=token)

@task_router.get("/", response_model=TaskPublic | list[TaskPublic])
async def get_task(token: Annotated[str, Depends(oauth_scheme)], request: Request):
    params = request.query_params
    return task_service.get(token, dict(params))
    
@task_router.delete("/delete/{task_id}")
async def delete_task(
    task_id: str,
    token: Annotated[str, Depends(oauth_scheme)]):
    return task_service.delete(token, task_id)

@task_router.put("/{task_id}", response_model=TaskPublic)
async def update_task(
    task_id: str,
    task: TaskUpdate,
    token: Annotated[str, Depends(oauth_scheme)],
    ):
    return task_service.update(token, task_id, task)


@task_router.post("/", response_model=TaskPublic)
async def create_task(
    task: TaskCreate,
    token: Annotated[str, Depends(oauth_scheme)],
):
    return task_service.create(task=task, token=token)
