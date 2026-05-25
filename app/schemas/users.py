from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    is_active: bool


class UpdateUserRequest(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
