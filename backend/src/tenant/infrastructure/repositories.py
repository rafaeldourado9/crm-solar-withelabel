from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tenant.domain.entities import Tenant
from src.tenant.infrastructure.models import TenantModel


class SQLAlchemyTenantRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, tenant: Tenant) -> Tenant:
        model = TenantModel(**tenant.model_dump())
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return Tenant.model_validate(model)

    async def get_by_id(self, tenant_id: UUID) -> Tenant | None:
        result = await self.session.execute(
            select(TenantModel).where(TenantModel.id == tenant_id)
        )
        model = result.scalar_one_or_none()
        return Tenant.model_validate(model) if model else None

    async def get_by_cnpj(self, cnpj: str) -> Tenant | None:
        result = await self.session.execute(
            select(TenantModel).where(TenantModel.cnpj == cnpj)
        )
        model = result.scalar_one_or_none()
        return Tenant.model_validate(model) if model else None

    async def update(self, tenant: Tenant) -> Tenant:
        result = await self.session.execute(
            select(TenantModel).where(TenantModel.id == tenant.id)
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Tenant {tenant.id} não encontrado")

        for key, value in tenant.model_dump(exclude={"id", "created_at"}).items():
            setattr(model, key, value)

        await self.session.flush()
        await self.session.refresh(model)
        return Tenant.model_validate(model)
