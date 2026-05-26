from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import User, UserSession, Permission, UserRole, Role, RolePermission


class AccessRepository:

    async def get_user_permission_codes(self, async_session: AsyncSession, user_id: int) -> list[str]:
        statement = select(Permission.code).join(RolePermission, RolePermission.permission_id == Permission.id).join(
            UserRole, UserRole.role_id == RolePermission.role_id).where(UserRole.user_id == user_id)
        return (await async_session.scalars(statement)).all()
