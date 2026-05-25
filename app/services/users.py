from app.repositories.users import UsersRepository
from app.schemas.users import UserResponse, UpdateUserRequest
from app.db.models import User
from app.db.session import async_session_maker


class UsersService:
    def __init__(self, users_repository: UsersRepository) -> None:
        self.users_repository = users_repository

    def get_me(self, user: User) -> UserResponse:
        return UserResponse.model_validate(user)

    async def update_me(self, user: User, payload: UpdateUserRequest) -> UserResponse:
        async with async_session_maker() as async_session:
            async with async_session.begin():
                user = await self.users_repository.get_user_by_id(async_session, user.id)
                if payload.full_name:
                    user.full_name = payload.full_name

                if payload.email:
                    user.email = payload.email

                await async_session.flush()

        return UserResponse.model_validate(user)

    async def delete_me(self, user: User) -> None:
        async with async_session_maker() as async_session:
            async with async_session.begin():
                user.is_active = False
                async_session.merge(user)
                await self.users_repository.deactivate_all_user_sessions(async_session, user.id)

        return None
