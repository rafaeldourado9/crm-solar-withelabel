from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.clientes.domain.entities import Cliente
from src.clientes.infrastructure.models import ClienteModel


class SQLAlchemyClienteRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, cliente: Cliente) -> Cliente:
        model = ClienteModel(**cliente.model_dump())
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return Cliente.model_validate(model)

    async def get_by_id(self, cliente_id: UUID, tenant_id: UUID) -> Cliente | None:
        result = await self.session.execute(
            select(ClienteModel).where(
                ClienteModel.id == cliente_id, ClienteModel.tenant_id == tenant_id
            )
        )
        model = result.scalar_one_or_none()
        return Cliente.model_validate(model) if model else None

    async def list_by_tenant(
        self,
        tenant_id: UUID,
        vendedor_id: UUID | None = None,
        status: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Cliente]:
        query = select(ClienteModel).where(ClienteModel.tenant_id == tenant_id)
        if vendedor_id:
            query = query.where(ClienteModel.vendedor_id == vendedor_id)
        if status:
            query = query.where(ClienteModel.status == status)
        query = query.offset(offset).limit(limit).order_by(ClienteModel.created_at.desc())
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [Cliente.model_validate(m) for m in models]

    async def count_by_tenant(
        self,
        tenant_id: UUID,
        vendedor_id: UUID | None = None,
        status: str | None = None,
    ) -> int:
        query = select(func.count(ClienteModel.id)).where(
            ClienteModel.tenant_id == tenant_id
        )
        if vendedor_id:
            query = query.where(ClienteModel.vendedor_id == vendedor_id)
        if status:
            query = query.where(ClienteModel.status == status)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def update(self, cliente: Cliente) -> Cliente:
        result = await self.session.execute(
            select(ClienteModel).where(ClienteModel.id == cliente.id)
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Cliente {cliente.id} nao encontrado")

        for key, value in cliente.model_dump(exclude={"id", "created_at"}).items():
            setattr(model, key, value)

        await self.session.flush()
        await self.session.refresh(model)
        return Cliente.model_validate(model)

    async def delete(self, cliente_id: UUID, tenant_id: UUID) -> bool:
        result = await self.session.execute(
            select(ClienteModel).where(
                ClienteModel.id == cliente_id, ClienteModel.tenant_id == tenant_id
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            return False
        await self.session.delete(model)
        await self.session.flush()
        return True
