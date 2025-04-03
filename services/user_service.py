from uuid import UUID

from utils import password_util, reduce_list
from models import UserCreate, UserUpdate, User, UserPublic
from fastapi import HTTPException
from db_connection import get_session
from sqlmodel import select



def create(user: UserCreate):
    session = get_session()
    hashed_password = password_util.hash(user.password)
    
    db_user = User.model_validate(user, update={"hashed_password":hashed_password})

    # check if email already exists
    statement = select(User).where(User.email == db_user.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    session.close()

    return db_user

def update(user_id: str, user: UserUpdate):
    session = get_session()
    db_user = session.get(User, user_id)

    if not db_user:
        return {"Error":"User not found"}
    
    user_data = user.model_dump(exclude_unset=True)
    extra_data = {}

    if "password" in user_data:
        password = user_data["password"]

        hashed_password = password_util.hash(password)

        extra_data["hashed_password"] = hashed_password
    
    db_user.sqlmodel_update(user_data, update=extra_data)

    session.add(db_user)
    session.commit()

    session.refresh(db_user)
    session.close()

    return db_user

from uuid import UUID

def get(params: dict) -> list[User] | User:
    session = get_session()
    statement = select(User)

    if params:
        for param, value in params.items():
            if param == "id":
                try:
                    value = UUID(value)  # Try to convert to UUID
                except ValueError:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid UUID format for {param}",
                    )
            statement = statement.where(getattr(User, param) == value)

    users = session.exec(statement).all()

    return reduce_list(users)


def delete(user_id: str) -> None:
    session = get_session()
    db_user = session.get(User, user_id)

    session.delete(db_user)
    session.commit()
    session.close()

    return None