from fastapi import APIRouter, Depends

from app.db.models import User, UserSession
from app.dependencies import get_auth_service, get_current_user
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.schemas.users import UserResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201)
async def register_user(payload: RegisterRequest,
                        auth_service: AuthService = Depends(get_auth_service)) -> UserResponse:
    return await auth_service.register(payload)


@router.post("/login")
async def login_user(payload: LoginRequest,
                     auth_service: AuthService = Depends(get_auth_service)) -> TokenResponse:
    return await auth_service.login(payload)


@router.post("/logout")
async def logout_user(auth_service: AuthService = Depends(get_auth_service),
                      user: tuple[User, UserSession] = Depends(get_current_user)) -> None:
    await auth_service.logout(user[1])
    return None
