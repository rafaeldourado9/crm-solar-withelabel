from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.propostas.domain.entities import Proposta
from src.propostas.infrastructure.models import PropostaModel


class SQLAlchemyPropostaRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, proposta: Proposta) -> Proposta:
        data = proposta.model_dump()
        model = PropostaModel(**data)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return Proposta.model_validate(model)

    async def get_by_id(self, id: UUID, tenant_id: UUID) -> Proposta | None:
        result = await self.session.execute(
            select(PropostaModel).where(
                PropostaModel.id == id, PropostaModel.tenant_id == tenant_id
            )
        )
        model = result.scalar_one_or_none()
        return Proposta.model_validate(model) if model else None

    async def list_by_tenant(
        self,
        tenant_id: UUID,
        cliente_id: UUID | None = None,
        status: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Proposta]:
        query = select(PropostaModel).where(PropostaModel.tenant_id == tenant_id)
        if cliente_id:
            query = query.where(PropostaModel.cliente_id == cliente_id)
        if status:
            query = query.where(PropostaModel.status == status)
        query = query.offset(offset).limit(limit).order_by(PropostaModel.created_at.desc())
        result = await self.session.execute(query)
        return [Proposta.model_validate(m) for m in result.scalars().all()]

    async def count_by_tenant(
        self,
        tenant_id: UUID,
        cliente_id: UUID | None = None,
        status: str | None = None,
    ) -> int:
        query = select(func.count(PropostaModel.id)).where(PropostaModel.tenant_id == tenant_id)
        if cliente_id:
            query = query.where(PropostaModel.cliente_id == cliente_id)
        if status:
            query = query.where(PropostaModel.status == status)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def update(self, proposta: Proposta) -> Proposta:
        result = await self.session.execute(
            select(PropostaModel).where(PropostaModel.id == proposta.id)
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Proposta {proposta.id} não encontrada")
        for key, value in proposta.model_dump(exclude={"id", "created_at"}).items():
            setattr(model, key, value)
        await self.session.flush()
        await self.session.refresh(model)
        return Proposta.model_validate(model)

    async def next_numero(self, tenant_id: UUID) -> str:
        result = await self.session.execute(
            select(func.count(PropostaModel.id)).where(PropostaModel.tenant_id == tenant_id)
        )
        total = result.scalar_one()
        ano = datetime.now(timezone.utc).year
        return f"PROP-{ano}-{total + 1:04d}"
