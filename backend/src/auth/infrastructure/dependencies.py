from uuid import UUID

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.application.use_cases import CriarUserUseCase, LoginUseCase, RefreshTokenUseCase
from src.auth.domain.entities import User
from src.auth.domain.repositories import UserRepository
from src.auth.domain.services import JWTService
from src.auth.infrastructure.repositories import SQLAlchemyUserRepository
from src.database import get_db
from src.shared.exceptions import ForbiddenError
from src.tenant.domain.entities import Tenant
from src.tenant.domain.repositories import TenantRepository
from src.tenant.infrastructure.repositories import SQLAlchemyTenantRepository


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return SQLAlchemyUserRepository(db)


def get_login_use_case(
    repo: UserRepository = Depends(get_user_repository),
) -> LoginUseCase:
    return LoginUseCase(repo)


def get_refresh_token_use_case(
    repo: UserRepository = Depends(get_user_repository),
) -> RefreshTokenUseCase:
    return RefreshTokenUseCase(repo)


def get_criar_user_use_case(
    repo: UserRepository = Depends(get_user_repository),
) -> CriarUserUseCase:
    return CriarUserUseCase(repo)


async def get_current_user(
    authorization: str = Header(...),
    user_repo: UserRepository = Depends(get_user_repository),
) -> User:
    if not authorization.startswith("Bearer "):
        raise ForbiddenError("Token invalido")

    token = authorization.replace("Bearer ", "")
    try:
        payload = JWTService.decode_token(token)
    except ValueError:
        raise ForbiddenError("Token invalido ou expirado")

    if payload.get("type") != "access":
        raise ForbiddenError("Token invalido")

    user_id = UUID(payload["sub"])
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise ForbiddenError("Usuario nao encontrado")

    if not user.ativo or user.bloqueado:
        raise ForbiddenError("Usuario inativo ou bloqueado")

    return user


async def get_current_tenant(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Tenant:
    tenant_repo: TenantRepository = SQLAlchemyTenantRepository(db)
    tenant = await tenant_repo.get_by_id(user.tenant_id)
    if not tenant:
        raise ForbiddenError("Tenant nao encontrado")
    if not tenant.ativo:
        raise ForbiddenError("Tenant inativo")
    return tenant
