from fastapi import APIRouter, Depends

from app.dependencies import get_access_service, require_permission
from app.schemas.access import RoleResponse, PermissionResponse, CreateRoleRequest
from app.services.access import AccessService

router = APIRouter(prefix="/access", tags=["access"])


@router.get("/roles")
async def get_roles(access_service: AccessService = Depends(get_access_service),
                    _=Depends(require_permission("access_rules:manage"))) -> list[RoleResponse]:
    return await access_service.get_roles()


@router.get("/permissions")
async def get_permissions(access_service: AccessService = Depends(get_access_service),
                          _=Depends(require_permission("access_rules:manage"))) -> list[PermissionResponse]:
    return await access_service.get_permissions()


@router.post("/role", status_code=201)
async def create_role(payload: CreateRoleRequest,
                      access_service: AccessService = Depends(get_access_service),
                      _=Depends(require_permission("access_rules:manage"))) -> RoleResponse:
    return await access_service.create_role(payload)


@router.post("/users/{user_id}/roles/{role_id}", status_code=204)
async def assign_role_to_user(user_id: int, role_id: int,
                              access_service: AccessService = Depends(get_access_service),
                              _=Depends(require_permission("access_rules:manage"))) -> None:
    return await access_service.assign_role_to_user(user_id, role_id)


@router.delete("/users/{user_id}/roles/{role_id}", status_code=204)
async def remove_role_from_user(user_id: int, role_id: int,
                                access_service: AccessService = Depends(get_access_service),
                                _=Depends(require_permission("access_rules:manage"))) -> None:
    return await access_service.remove_role_from_user(user_id, role_id)


@router.post("/roles/{role_id}/permissions/{permission_id}", status_code=204)
async def assign_permission_to_role(role_id: int, permission_id: int,
                                    access_service: AccessService = Depends(get_access_service),
                                    _=Depends(require_permission("access_rules:manage"))) -> None:
    return await access_service.assign_permission_to_role(role_id, permission_id)


@router.delete("/roles/{role_id}/permissions/{permission_id}", status_code=204)
async def remove_permission_from_role(role_id: int, permission_id: int,
                                      access_service: AccessService = Depends(get_access_service),
                                      _=Depends(require_permission("access_rules:manage"))) -> None:
    return await access_service.remove_permission_from_role(role_id, permission_id)
