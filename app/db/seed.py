from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from app.db.session import async_session_maker
from app.db.models import Resource, Permission, Role, UserRole, RolePermission


async def insert_resources(async_session: AsyncSession):
    resources_data = [{"code": "documents", "name": "Documents"},
                      {"code": "reports", "name": "Reports"},
                      {"code": "orders", "name": "Orders"},
                      {"code": "access_rules", "name": "Access Rules"}, ]
    statement = insert(Resource)
    await async_session.execute(statement, resources_data)


async def insert_permissions(async_session: AsyncSession):
    permissions_data = [{"resource_id": 1, "resource": "documents", "action": "read", "code": "documents:read"},
                        {"resource_id": 2, "resource": "reports", "action": "read", "code": "reports:read"},
                        {"resource_id": 3, "resource": "orders", "action": "read", "code": "orders:read"},
                        {"resource_id": 4, "resource": "access_rules", "action": "manage",
                         "code": "access_rules:manage"}, ]

    statement = insert(Permission)
    await async_session.execute(statement, permissions_data)


async def insert_roles(async_session: AsyncSession):
    roles_data = [{"name": "admin", },
                  {"name": "user", }]
    statement = insert(Role)
    await async_session.execute(statement, roles_data)


async def insert_user_roles(async_session: AsyncSession):
    roles_data = [{"user_id": 1, "role_id": 1, }, ]
    statement = insert(UserRole)
    await async_session.execute(statement, roles_data)


async def insert_role_permission(async_session: AsyncSession):
    role_permissions_data = [{"role_id": 1, "permission_id": 4, },
                             {"role_id": 1, "permission_id": 5, },
                             {"role_id": 1, "permission_id": 6, },
                             {"role_id": 1, "permission_id": 7, },]
    statement = insert(RolePermission)
    await async_session.execute(statement, role_permissions_data)


async def main():
    async with async_session_maker() as async_session:
        async with async_session.begin():
            await insert_resources(async_session)
            await insert_permissions(async_session)
            await insert_roles(async_session)
            await insert_user_roles(async_session)
            await insert_role_permission(async_session)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
