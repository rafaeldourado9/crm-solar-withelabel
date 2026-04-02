from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.orcamentos.domain.entities import Orcamento
from src.orcamentos.infrastructure.models import OrcamentoModel


class SQLAlchemyOrcamentoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, orcamento: Orcamento) -> Orcamento:
        data = orcamento.model_dump()
        # Convert Decimals in itens_adicionais
        if data.get("itens_adicionais"):
            data["itens_adicionais"] = [
                {k: str(v) if isinstance(v, Decimal) else v for k, v in item.items()}
                for item in data["itens_adicionais"]
            ]
        model = OrcamentoModel(**data)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, orcamento_id: UUID, tenant_id: UUID) -> Orcamento | None:
        result = await self.session.execute(
            select(OrcamentoModel).where(
                OrcamentoModel.id == orcamento_id, OrcamentoModel.tenant_id == tenant_id
            )
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list_by_tenant(
        self,
        tenant_id: UUID,
        vendedor_id: UUID | None = None,
        cliente_id: UUID | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Orcamento]:
        query = select(OrcamentoModel).where(OrcamentoModel.tenant_id == tenant_id)
        if vendedor_id:
            query = query.where(OrcamentoModel.vendedor_id == vendedor_id)
        if cliente_id:
            query = query.where(OrcamentoModel.cliente_id == cliente_id)
        query = query.offset(offset).limit(limit).order_by(OrcamentoModel.created_at.desc())
        result = await self.session.execute(query)
        return [self._to_entity(m) for m in result.scalars().all()]

    async def count_by_tenant(
        self,
        tenant_id: UUID,
        vendedor_id: UUID | None = None,
        cliente_id: UUID | None = None,
    ) -> int:
        query = select(func.count(OrcamentoModel.id)).where(
            OrcamentoModel.tenant_id == tenant_id
        )
        if vendedor_id:
            query = query.where(OrcamentoModel.vendedor_id == vendedor_id)
        if cliente_id:
            query = query.where(OrcamentoModel.cliente_id == cliente_id)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def update(self, orcamento: Orcamento) -> Orcamento:
        result = await self.session.execute(
            select(OrcamentoModel).where(OrcamentoModel.id == orcamento.id)
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Orcamento {orcamento.id} nao encontrado")

        data = orcamento.model_dump(exclude={"id", "created_at"})
        if data.get("itens_adicionais"):
            data["itens_adicionais"] = [
                {k: str(v) if isinstance(v, Decimal) else v for k, v in item.items()}
                for item in data["itens_adicionais"]
            ]

        for key, value in data.items():
            setattr(model, key, value)

        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def delete(self, orcamento_id: UUID, tenant_id: UUID) -> bool:
        result = await self.session.execute(
            select(OrcamentoModel).where(
                OrcamentoModel.id == orcamento_id, OrcamentoModel.tenant_id == tenant_id
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            return False
        await self.session.delete(model)
        await self.session.flush()
        return True

    def _to_entity(self, model: OrcamentoModel) -> Orcamento:
        return Orcamento(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            tenant_id=model.tenant_id,
            cliente_id=model.cliente_id,
            vendedor_id=model.vendedor_id,
            status=model.status,
            consumo_mensal_kwh=Decimal(str(model.consumo_mensal_kwh)),
            painel_id=model.painel_id,
            painel_modelo=model.painel_modelo,
            painel_potencia_w=model.painel_potencia_w,
            inversor_id=model.inversor_id,
            inversor_modelo=model.inversor_modelo,
            inversor_potencia_nominal_w=model.inversor_potencia_nominal_w,
            quantidade_paineis=model.quantidade_paineis,
            potencia_sistema_kwp=Decimal(str(model.potencia_sistema_kwp)),
            geracao_mensal_kwh=Decimal(str(model.geracao_mensal_kwh)),
            valor_kit=Decimal(str(model.valor_kit)),
            valor_montagem=Decimal(str(model.valor_montagem)),
            valor_projeto=Decimal(str(model.valor_projeto)),
            valor_estrutura=Decimal(str(model.valor_estrutura)),
            tipo_estrutura=model.tipo_estrutura,
            valor_material_eletrico=Decimal(str(model.valor_material_eletrico)),
            custo_deslocamento=Decimal(str(model.custo_deslocamento)),
            itens_adicionais=model.itens_adicionais or [],
            valor_itens_adicionais=Decimal(str(model.valor_itens_adicionais)),
            subtotal=Decimal(str(model.subtotal)),
            margem_lucro=Decimal(str(model.margem_lucro)),
            comissao=Decimal(str(model.comissao)),
            imposto=Decimal(str(model.imposto)),
            margem_desconto_avista=Decimal(str(model.margem_desconto_avista)),
            valor_final=Decimal(str(model.valor_final)),
            forma_pagamento=model.forma_pagamento,
            taxa_juros=Decimal(str(model.taxa_juros)),
            valor_cobrado=Decimal(str(model.valor_cobrado)),
            numero_parcelas=model.numero_parcelas,
            valor_parcela=Decimal(str(model.valor_parcela)),
            economia_25_anos=model.economia_25_anos or [],
        )
