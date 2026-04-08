from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.vendedores.domain.entities import VendaVendedor
from src.vendedores.infrastructure.models import VendaVendedorModel


class SQLAlchemyVendaVendedorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, venda: VendaVendedor) -> VendaVendedor:
        model = VendaVendedorModel(**venda.model_dump())
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get_by_contrato(self, contrato_id: UUID, tenant_id: UUID) -> VendaVendedor | None:
        result = await self.session.execute(
            select(VendaVendedorModel).where(
                VendaVendedorModel.contrato_id == contrato_id,
                VendaVendedorModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list_by_vendedor(self, vendedor_id: UUID, tenant_id: UUID) -> list[VendaVendedor]:
        result = await self.session.execute(
            select(VendaVendedorModel)
            .where(
                VendaVendedorModel.vendedor_id == vendedor_id,
                VendaVendedorModel.tenant_id == tenant_id,
            )
            .order_by(VendaVendedorModel.created_at.desc())
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    async def marcar_pago(self, venda_id: UUID, tenant_id: UUID) -> VendaVendedor | None:
        result = await self.session.execute(
            select(VendaVendedorModel).where(
                VendaVendedorModel.id == venda_id,
                VendaVendedorModel.tenant_id == tenant_id,
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        model.pago = True
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)

    def _to_entity(self, model: VendaVendedorModel) -> VendaVendedor:
        return VendaVendedor(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            tenant_id=model.tenant_id,
            contrato_id=model.contrato_id,
            vendedor_id=model.vendedor_id,
            valor_venda=Decimal(str(model.valor_venda)),
            valor_comissao=Decimal(str(model.valor_comissao)),
            pago=model.pago,
        )
