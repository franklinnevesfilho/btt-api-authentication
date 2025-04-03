from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from services import auth_service
from models import Token

auth_router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

@auth_router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    return auth_service.login(form_data.username, form_data.password)



