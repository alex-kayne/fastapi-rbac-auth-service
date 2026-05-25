from fastapi import APIRouter, Depends

from app.db.models import User, UserSession
from app.dependencies import get_current_user
from app.dependencies import get_user_service
from app.schemas.users import UpdateUserRequest
from app.schemas.users import UserResponse
from app.services.users import UsersService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def get_user(users_service: UsersService = Depends(get_user_service),
                           user: tuple[User, UserSession] = Depends(get_current_user)) -> UserResponse:
    return users_service.get_me(user[0])


@router.patch("/me")
async def update_user(payload: UpdateUserRequest,
                      users_service: UsersService = Depends(get_user_service),
                      user: tuple[User, UserSession] = Depends(get_current_user)) -> UserResponse:
    return await users_service.update_me(user[0], payload)


@router.delete("/me", status_code=204)
async def delete_user(users_service: UsersService = Depends(get_user_service),
                      user: tuple[User, UserSession] = Depends(get_current_user)) -> None:
    await users_service.delete_me(user[0])

    return None
