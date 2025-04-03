from uuid import UUID

from fastapi import HTTPException

from models import TaskCreate, TaskUpdate, Task

from sqlmodel import select
from services import auth_service
from db_connection import get_session
from utils import reduce_list


def create(token: str, task: TaskCreate):
    session = get_session()

    user = auth_service.get_current_user(token=token)

    db_task = Task.model_validate(task)
    db_task.user_id = user.id

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task

def update(token: str, task_id: str, task: TaskUpdate):
    """
    Update a task in the database.
    :return:
    """
    session = get_session()

    user = auth_service.get_current_user(token=token)

    db_task = session.get(Task, task_id)

    if not db_task | db_task.user_id != user.id:
        return {"message": "Task not found"}

    task_data = task.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(task_data)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task

def get(
        token: str,
        params: dict
):
    """
    Get a task from the database.
    @params: task_id, user_id, task_name, task_description
    :return: UserPublic | {"message": "Task not found"}
    """

    session = get_session()
    user = _get_user(token)

    statement = select(Task).where(Task.user_id == user.id)

    if params:
        for param, value in params.items():
            if param == "id":
                try:
                    value = UUID(value)
                except ValueError:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid UUID format for {param}",
                    )

            statement = statement.where(getattr(Task, param) == value)

    result = session.exec(statement).all()

    return reduce_list(result)

def filter_by(
        token: str,
        params: dict,
):
    """
    Filter tasks in the database based on provided parameters.
    :return:
    - A list of task objects that match the filter criteria
    - An empty list if no tasks match the criteria
    """

    session = get_session()
    user = _get_user(token)

    statement = select(Task).where(Task.user_id == user.id)

    for param in params:
        statement = statement.where(getattr(Task, param) == params[param])

    result = session.exec(statement).all()

    return result

def get_all(token: str):
    """
    Get all tasks from the database.
    :return:
    - A list of all task objects in the database
    - An empty list if no tasks exist
    """
    session = get_session()
    user = _get_user(token)

    statement = select(Task).where(Task.user_id == user.id)

    result = session.exec(statement).all()
    session.close()

    return result

def delete(
        token: str,
        task_id: str
):
    """
    Delete a task from the database by task_id.
    :return:
    - None if the task was successfully deleted
    - A message indicating that the task was not found if it doesn't exist
    """
    session = get_session()
    user = _get_user(token)

    db_task = session.get(Task, task_id)

    if not db_task | db_task.user_id != user.id:
        return {"message": "Task not found"}

    session.delete(db_task)
    session.commit()
    session.close()

    return None

def _get_user(token: str):
    """
    Get the user associated with the provided token.
    :return:
    - The user object if found
    - None if the user is not found
    """
    user = auth_service.get_current_user(token=token)
    return user