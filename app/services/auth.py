import uuid
from datetime import datetime, UTC, timedelta

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

from app.config import settings
from app.db.session import async_session_maker
from app.repositories.users import UsersRepository
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.schemas.users import UserResponse


class AuthService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    def create_access_token(self, user_id: int, session_jti: str, expires_at: datetime) -> str:
        payload = {
            "sub": str(user_id),
            "jti": session_jti,
            "exp": expires_at,
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    def decode_access_token(self, access_token: str) -> dict:
        return jwt.decode(access_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

    async def register(self, payload: RegisterRequest) -> UserResponse:
        async with async_session_maker() as async_session:
            async with async_session.begin():
                if await self.users_repository.get_user_by_email(async_session, payload.email):
                    raise HTTPException(status_code=409, detail="User email already exists")

                hashed_password = self.hash_password(payload.password)

                new_user = await self.users_repository.create_user(async_session, payload.full_name, payload.email,
                                                                   hashed_password)

                return UserResponse.model_validate(new_user)

    async def login(self, payload: LoginRequest) -> TokenResponse:
        async with (async_session_maker() as async_session):
            async with async_session.begin():
                if (not (user := await self.users_repository.get_user_by_email(async_session, payload.email))
                        or not self.verify_password(payload.password, user.hashed_password)
                        or not user.is_active):
                    raise HTTPException(status_code=401, detail="Wrong password or user does not exist")

                jti = str(uuid.uuid4())
                expires_at = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

                await self.users_repository.create_session(async_session, user.id, jti, expires_at)

                token = self.create_access_token(user.id, jti, expires_at)

                return TokenResponse(access_token=token)
