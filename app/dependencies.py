from datetime import datetime, UTC

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.db import User
from app.db.models import UserSession
from app.db.session import async_session_maker
from app.repositories.users import UsersRepository
from app.services.auth import AuthService
from app.services.users import UsersService


def get_user_repository() -> UsersRepository:
    return UsersRepository()


def get_auth_service() -> AuthService:
    return AuthService(get_user_repository())


async def get_current_user(cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> tuple[User, UserSession]:
    auth_service = get_auth_service()

    token = cred.credentials

    try:
        token_data = auth_service.decode_access_token(token)
    except jwt.PyJWTError:
        raise HTTPException(401)

    user_id = int(token_data["sub"])
    jti = token_data["jti"]

    async with async_session_maker() as async_session:
        async with async_session.begin():
            if (not (user := await auth_service.users_repository.get_user_by_id(async_session, user_id))
                    or not user.is_active):
                raise HTTPException(401)

            if (not (user_session := await auth_service.users_repository.get_session_by_jti(async_session, jti))
                    or not user_session.is_active
                    or user_session.expires_at < datetime.now(UTC)):
                raise HTTPException(401)

    return user, user_session


def get_user_service() -> UsersService:
    return UsersService(get_user_repository())
