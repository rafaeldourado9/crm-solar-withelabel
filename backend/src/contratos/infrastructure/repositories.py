from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.contratos.domain.entities import Contrato
from src.contratos.infrastructure.models import ContratoModel


class SQLAlchemyContratoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, contrato: Contrato) -> Contrato:
        model = ContratoModel(**contrato.model_dump())
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return Contrato.model_validate(model)

    async def get_by_id(self, id: UUID, tenant_id: UUID) -> Contrato | None:
        result = await self.session.execute(
            select(ContratoModel).where(
                ContratoModel.id == id, ContratoModel.tenant_id == tenant_id
            )
        )
        model = result.scalar_one_or_none()
        return Contrato.model_validate(model) if model else None

    async def get_by_proposta(self, proposta_id: UUID, tenant_id: UUID) -> Contrato | None:
        result = await self.session.execute(
            select(ContratoModel).where(
                ContratoModel.proposta_id == proposta_id,
                ContratoModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        return Contrato.model_validate(model) if model else None

    async def list_by_tenant(
        self,
        tenant_id: UUID,
        cliente_id: UUID | None = None,
        status: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Contrato]:
        query = select(ContratoModel).where(ContratoModel.tenant_id == tenant_id)
        if cliente_id:
            query = query.where(ContratoModel.cliente_id == cliente_id)
        if status:
            query = query.where(ContratoModel.status == status)
        query = query.offset(offset).limit(limit).order_by(ContratoModel.created_at.desc())
        result = await self.session.execute(query)
        return [Contrato.model_validate(m) for m in result.scalars().all()]

    async def count_by_tenant(
        self,
        tenant_id: UUID,
        cliente_id: UUID | None = None,
        status: str | None = None,
    ) -> int:
        query = select(func.count(ContratoModel.id)).where(ContratoModel.tenant_id == tenant_id)
        if cliente_id:
            query = query.where(ContratoModel.cliente_id == cliente_id)
        if status:
            query = query.where(ContratoModel.status == status)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def update(self, contrato: Contrato) -> Contrato:
        result = await self.session.execute(
            select(ContratoModel).where(ContratoModel.id == contrato.id)
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Contrato {contrato.id} não encontrado")
        for key, value in contrato.model_dump(exclude={"id", "created_at"}).items():
            setattr(model, key, value)
        await self.session.flush()
        await self.session.refresh(model)
        return Contrato.model_validate(model)

    async def next_numero(self, tenant_id: UUID) -> str:
        result = await self.session.execute(
            select(func.count(ContratoModel.id)).where(ContratoModel.tenant_id == tenant_id)
        )
        total = result.scalar_one()
        ano = datetime.utcnow().year
        return f"CONT-{ano}-{total + 1:04d}"
