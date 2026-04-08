from fastapi import APIRouter, Depends, status

from src.auth.application.dtos import (
    LoginRequest,
    LoginResponse,
    RefreshRequest,
    RefreshResponse,
    UserResponse,
)
from src.auth.application.use_cases import LoginUseCase, RefreshTokenUseCase
from src.auth.domain.entities import User
from src.auth.infrastructure.dependencies import (
    get_current_tenant,
    get_current_user,
    get_login_use_case,
    get_refresh_token_use_case,
)
from src.tenant.domain.entities import Tenant

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(
    dto: LoginRequest,
    tenant: Tenant = Depends(get_current_tenant),
    use_case: LoginUseCase = Depends(get_login_use_case),
) -> LoginResponse:
    """Login com email e senha"""
    return await use_case.execute(dto, tenant.id)


@router.post("/refresh", response_model=RefreshResponse)
async def refresh_token(
    dto: RefreshRequest,
    use_case: RefreshTokenUseCase = Depends(get_refresh_token_use_case),
) -> RefreshResponse:
    """Renovar access token usando refresh token"""
    return await use_case.execute(dto.refresh_token)


@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)) -> UserResponse:
    """Obter dados do usuário logado"""
    return UserResponse.model_validate(user)
