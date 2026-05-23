from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import User, UserSession


class UsersRepository:

    async def get_user_by_email(self, async_session: AsyncSession, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return await async_session.scalar(statement)

    async def get_user_by_id(self, async_session: AsyncSession, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        return await async_session.scalar(statement)

    async def create_user(self, async_session: AsyncSession, full_name: str, email: str, hashed_password: str) -> User:
        new_user = User(full_name=full_name, email=email, hashed_password=hashed_password)

        async_session.add(new_user)
        await async_session.flush()

        return new_user

    async def create_session(self, async_session: AsyncSession, user_id: int, token_jti: str,
                             expires_at: datetime) -> UserSession:
        new_session = UserSession(user_id=user_id, token_jti=token_jti, expires_at=expires_at)

        async_session.add(new_session)
        await async_session.flush()

        return new_session
