from src.shared.exceptions import ConflictError, NotFoundError
from src.tenant.domain.entities import Tenant
from src.tenant.domain.repositories import TenantRepository
from src.tenant.application.dtos import (
    AtualizarBrandingRequest,
    AtualizarTenantRequest,
    CriarTenantRequest,
)
from uuid import UUID


class CriarTenantUseCase:
    def __init__(self, repo: TenantRepository):
        self.repo = repo

    async def execute(self, dto: CriarTenantRequest) -> Tenant:
        existing = await self.repo.get_by_cnpj(dto.cnpj)
        if existing:
            raise ConflictError(f"Tenant com CNPJ {dto.cnpj} ja existe")
        tenant = Tenant(**dto.model_dump())
        return await self.repo.create(tenant)


class ObterTenantUseCase:
    def __init__(self, repo: TenantRepository):
        self.repo = repo

    async def execute(self, tenant_id: UUID) -> Tenant:
        tenant = await self.repo.get_by_id(tenant_id)
        if not tenant:
            raise NotFoundError("Tenant", str(tenant_id))
        return tenant


class AtualizarTenantUseCase:
    def __init__(self, repo: TenantRepository):
        self.repo = repo

    async def execute(self, tenant_id: UUID, dto: AtualizarTenantRequest) -> Tenant:
        tenant = await self.repo.get_by_id(tenant_id)
        if not tenant:
            raise NotFoundError("Tenant", str(tenant_id))
        updates = dto.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(tenant, key, value)
        return await self.repo.update(tenant)


class AtualizarBrandingUseCase:
    def __init__(self, repo: TenantRepository):
        self.repo = repo

    async def execute(self, tenant_id: UUID, dto: AtualizarBrandingRequest) -> Tenant:
        tenant = await self.repo.get_by_id(tenant_id)
        if not tenant:
            raise NotFoundError("Tenant", str(tenant_id))
        updates = dto.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(tenant, key, value)
        return await self.repo.update(tenant)
