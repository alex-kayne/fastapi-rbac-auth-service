from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_auth_service
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
