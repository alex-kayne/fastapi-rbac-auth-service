from fastapi import HTTPException

from app.db.session import async_session_maker
from app.repositories.access import AccessRepository
from app.repositories.users import UsersRepository
from app.schemas.access import RoleResponse, PermissionResponse, CreateRoleRequest


class AccessService:
    def __init__(self, access_repository: AccessRepository,
                 user_repository: UsersRepository) -> None:
        self.access_repository = access_repository
        self.user_repository = user_repository

    async def get_roles(self) -> list[RoleResponse]:
        async with async_session_maker() as async_session:
            async with async_session.begin():
                roles = await self.access_repository.get_all_roles(async_session)

        return [RoleResponse.model_validate(role) for role in roles]

    async def get_permissions(self) -> list[PermissionResponse]:
        async with async_session_maker() as async_session:
            async with async_session.begin():
                permissions = await self.access_repository.get_all_permissions(async_session)

        return [PermissionResponse.model_validate(permission) for permission in permissions]

    async def create_role(self, payload: CreateRoleRequest) -> RoleResponse:
        async with async_session_maker() as async_session:
            async with async_session.begin():
                new_role = await self.access_repository.create_role(async_session, payload.name, payload.description)

        return RoleResponse.model_validate(new_role)

    async def assign_role_to_user(self, user_id: int, role_id: int) -> None:
        async with async_session_maker() as async_session:
            async with async_session.begin():
                if await self.access_repository.get_role_by_id(async_session, role_id) is None:
                    raise HTTPException(status_code=404)

                if await self.user_repository.get_user_by_id(async_session, user_id) is None:
                    raise HTTPException(status_code=404)

                if await self.access_repository.get_user_role(async_session, user_id, role_id):
                    raise HTTPException(status_code=409)

                await self.access_repository.assign_role_to_user(async_session, user_id, role_id)

        return None

    async def remove_role_from_user(self, user_id: int, role_id: int) -> None:
        async with async_session_maker() as async_session:
            async with async_session.begin():
                if user_role := await self.access_repository.get_user_role(async_session, user_id, role_id):
                    await self.access_repository.remove_role_from_user(user_role)
                else:
                    raise HTTPException(status_code=404)

        return None

    async def assign_permission_to_role(self, role_id: int, permission_id: int) -> None:
        async with async_session_maker() as async_session:
            async with async_session.begin():
                if await self.access_repository.get_role_by_id(async_session, role_id) is None:
                    raise HTTPException(status_code=404)

                if await self.access_repository.get_permission_by_id(async_session, permission_id) is None:
                    raise HTTPException(status_code=404)

                if await self.access_repository.get_role_permission(async_session, role_id, permission_id):
                    raise HTTPException(status_code=409)

                await self.access_repository.assign_permission_to_role(async_session, role_id, permission_id)

        return None

    async def remove_permission_from_role(self, role_id: int, permission_id: int) -> None:
        async with async_session_maker() as async_session:
            async with async_session.begin():
                if role_permission := await self.access_repository.get_role_permission(async_session, role_id,
                                                                                       permission_id):
                    await self.access_repository.remove_permission_from_role(async_session, role_permission)
                else:
                    raise HTTPException(status_code=404)

        return None
