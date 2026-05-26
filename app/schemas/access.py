from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None


class PermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    action: str
    resource_id: int
    description: str | None = None


class CreateRoleRequest(BaseModel):
    name: str
    description: str | None = None
