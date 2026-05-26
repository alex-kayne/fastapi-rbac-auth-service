from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Permission, UserRole, RolePermission, Role


class AccessRepository:

    async def get_user_permission_codes(self, async_session: AsyncSession, user_id: int) -> Sequence[str]:
        statement = select(Permission.code).join(RolePermission, RolePermission.permission_id == Permission.id).join(
            UserRole, UserRole.role_id == RolePermission.role_id).where(UserRole.user_id == user_id)
        return (await async_session.scalars(statement)).all()

    async def get_all_roles(self, async_session: AsyncSession) -> Sequence[Role]:
        statement = select(Role)
        return (await async_session.scalars(statement)).all()

    async def get_all_permissions(self, async_session: AsyncSession) -> Sequence[Permission]:
        statement = select(Permission)
        return (await async_session.scalars(statement)).all()

    async def get_role_by_id(self, async_session: AsyncSession, role_id: int) -> Role | None:
        statement = select(Role).where(Role.id == role_id)
        return await async_session.scalar(statement)

    async def get_permission_by_id(self, async_session: AsyncSession, permission_id: int) -> Permission | None:
        statement = select(Permission).where(Permission.id == permission_id)
        return await async_session.scalar(statement)

    async def get_user_role(self, async_session: AsyncSession, user_id: int, role_id: int) -> UserRole | None:
        statement = select(UserRole).where(UserRole.user_id == user_id, UserRole.role_id == role_id)
        return await async_session.scalar(statement)

    async def get_role_permission(self, async_session: AsyncSession, role_id: int,
                                  permission_id: int) -> RolePermission | None:
        statement = select(RolePermission).where(RolePermission.role_id == role_id,
                                                 RolePermission.permission_id == permission_id)
        return await async_session.scalar(statement)

    async def create_role(self, async_session: AsyncSession, name: str, description: str | None) -> Role:
        new_role = Role(name=name, description=description)
        async_session.add(new_role)
        await async_session.flush()
        return new_role

    async def assign_role_to_user(self, async_session: AsyncSession, user_id: int, role_id: int) -> UserRole | None:
        new_user_role = UserRole(user_id=user_id, role_id=role_id)
        async_session.add(new_user_role)
        await async_session.flush()
        return new_user_role

    async def remove_role_from_user(self, async_session: AsyncSession, user_role: UserRole) -> None:
        await async_session.delete(user_role)
        return None

    async def assign_permission_to_role(self, async_session: AsyncSession, role_id: int,
                                        permission_id: int) -> RolePermission:
        new_role_permission = RolePermission(permission_id=permission_id, role_id=role_id)
        async_session.add(new_role_permission)
        await async_session.flush()
        return new_role_permission

    async def remove_permission_from_role(self, async_session: AsyncSession, role_permission: RolePermission) -> None:
        await async_session.delete(role_permission)
        return None
