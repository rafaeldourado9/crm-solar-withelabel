from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.tenant.application.use_cases import (
    AtualizarBrandingUseCase,
    AtualizarTenantUseCase,
    CriarTenantUseCase,
    ObterTenantUseCase,
)
from src.tenant.domain.repositories import TenantRepository
from src.tenant.infrastructure.repositories import SQLAlchemyTenantRepository


def get_tenant_repository(db: AsyncSession = Depends(get_db)) -> TenantRepository:
    return SQLAlchemyTenantRepository(db)


def get_criar_tenant_use_case(
    repo: TenantRepository = Depends(get_tenant_repository),
) -> CriarTenantUseCase:
    return CriarTenantUseCase(repo)


def get_obter_tenant_use_case(
    repo: TenantRepository = Depends(get_tenant_repository),
) -> ObterTenantUseCase:
    return ObterTenantUseCase(repo)


def get_atualizar_tenant_use_case(
    repo: TenantRepository = Depends(get_tenant_repository),
) -> AtualizarTenantUseCase:
    return AtualizarTenantUseCase(repo)


def get_atualizar_branding_use_case(
    repo: TenantRepository = Depends(get_tenant_repository),
) -> AtualizarBrandingUseCase:
    return AtualizarBrandingUseCase(repo)
