from typing import Annotated

from fastapi.security import OAuth2PasswordBearer

from models import UserPublic, UserCreate, UserUpdate
from services import user_service, auth_service
from fastapi import APIRouter, Depends, Request


user_router = APIRouter(prefix="/user")

oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@user_router.get("/me", response_model=UserPublic)
async def get_user(token: Annotated[str, Depends(oauth_scheme)]):
    current_user = auth_service.get_current_user(token)
    return current_user


@user_router.get("/", response_model=UserPublic | list[UserPublic])
async def get_user(request: Request):
    params = request.query_params
    return user_service.get(dict(params))

@user_router.post("/create", response_model=UserPublic)
async def create_user(user: UserCreate):
    return user_service.create(user)

@user_router.put("/{user_id}", response_model=UserPublic)
async def update_user(user_id: str, user: UserUpdate):
    return user_service.update(user_id, user)