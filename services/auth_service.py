from datetime import datetime, timedelta, timezone
from typing import Annotated

from db_connection import get_session
from utils import password_util, jwt_util
from models import Token, TokenData, User, UserPublic
from . import user_service

from jwt import InvalidTokenError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


def login(email: str, password: str) -> Token:
    session = get_session()
    user = _authenticate_user(email, password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = _create_access_token(
        data={"sub": user.email}
    )

    session.close()

    return Token(access_token=access_token, token_type="bearer")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserPublic | None:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt_util.decode(token)
        email = payload.get("sub")

        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception

    user = user_service.get({
        "email": token_data.email
    })

    if not user:
        raise credentials_exception

    return UserPublic.model_validate(user)


def _authenticate_user(email: str, password: str) -> User | None:
    user = user_service.get({
        "email": email
    })

    if not user:
        return None

    if not password_util.verify(password, user.hashed_password):
        return None

    return user


def _create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt_util.encode(to_encode)
    return encoded_jwt
