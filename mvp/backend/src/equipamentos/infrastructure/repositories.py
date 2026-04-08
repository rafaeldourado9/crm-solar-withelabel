from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.equipamentos.domain.entities import Inversor, Painel
from src.equipamentos.infrastructure.models import InversorModel, PainelModel


class SQLAlchemyPainelRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, painel: Painel) -> Painel:
        model = PainelModel(**painel.model_dump())
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return Painel.model_validate(model)

    async def get_by_id(self, painel_id: UUID, tenant_id: UUID) -> Painel | None:
        result = await self.session.execute(
            select(PainelModel).where(
                PainelModel.id == painel_id, PainelModel.tenant_id == tenant_id
            )
        )
        model = result.scalar_one_or_none()
        return Painel.model_validate(model) if model else None

    async def list_ativos(self, tenant_id: UUID) -> list[Painel]:
        result = await self.session.execute(
            select(PainelModel).where(
                PainelModel.tenant_id == tenant_id, PainelModel.ativo == True
            )
        )
        models = result.scalars().all()
        return [Painel.model_validate(m) for m in models]

    async def update(self, painel: Painel) -> Painel:
        result = await self.session.execute(
            select(PainelModel).where(PainelModel.id == painel.id)
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Painel {painel.id} não encontrado")

        for key, value in painel.model_dump(exclude={"id", "created_at"}).items():
            setattr(model, key, value)

        await self.session.flush()
        await self.session.refresh(model)
        return Painel.model_validate(model)


class SQLAlchemyInversorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, inversor: Inversor) -> Inversor:
        model = InversorModel(**inversor.model_dump())
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return Inversor.model_validate(model)

    async def get_by_id(self, inversor_id: UUID, tenant_id: UUID) -> Inversor | None:
        result = await self.session.execute(
            select(InversorModel).where(
                InversorModel.id == inversor_id, InversorModel.tenant_id == tenant_id
            )
        )
        model = result.scalar_one_or_none()
        return Inversor.model_validate(model) if model else None

    async def list_ativos(self, tenant_id: UUID) -> list[Inversor]:
        result = await self.session.execute(
            select(InversorModel).where(
                InversorModel.tenant_id == tenant_id, InversorModel.ativo == True
            )
        )
        models = result.scalars().all()
        return [Inversor.model_validate(m) for m in models]

    async def update(self, inversor: Inversor) -> Inversor:
        result = await self.session.execute(
            select(InversorModel).where(InversorModel.id == inversor.id)
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Inversor {inversor.id} não encontrado")

        for key, value in inversor.model_dump(exclude={"id", "created_at"}).items():
            setattr(model, key, value)

        await self.session.flush()
        await self.session.refresh(model)
        return Inversor.model_validate(model)
