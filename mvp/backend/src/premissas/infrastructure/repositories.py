from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.premissas.domain.entities import Premissa
from src.premissas.infrastructure.models import PremissaModel


class SQLAlchemyPremissaRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, premissa: Premissa) -> Premissa:
        data = premissa.model_dump()
        # Convert Decimal to float for JSON fields
        data["taxas_maquininha"] = {k: float(v) for k, v in data["taxas_maquininha"].items()}
        model = PremissaModel(**data)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, premissa_id: UUID) -> Premissa | None:
        result = await self.session.execute(
            select(PremissaModel).where(PremissaModel.id == premissa_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_ativa(self, tenant_id: UUID) -> Premissa | None:
        result = await self.session.execute(
            select(PremissaModel).where(
                PremissaModel.tenant_id == tenant_id, PremissaModel.ativa == True
            )
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def update(self, premissa: Premissa) -> Premissa:
        result = await self.session.execute(
            select(PremissaModel).where(PremissaModel.id == premissa.id)
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Premissa {premissa.id} não encontrada")

        data = premissa.model_dump(exclude={"id", "created_at"})
        data["taxas_maquininha"] = {k: float(v) for k, v in data["taxas_maquininha"].items()}

        for key, value in data.items():
            setattr(model, key, value)

        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)

    def _to_entity(self, model: PremissaModel) -> Premissa:
        data = {
            "id": model.id,
            "created_at": model.created_at,
            "updated_at": model.updated_at,
            "tenant_id": model.tenant_id,
            "ativa": model.ativa,
            "margem_lucro_percentual": Decimal(str(model.margem_lucro_percentual)),
            "comissao_percentual": Decimal(str(model.comissao_percentual)),
            "imposto_percentual": Decimal(str(model.imposto_percentual)),
            "margem_desconto_avista_percentual": Decimal(
                str(model.margem_desconto_avista_percentual)
            ),
            "montagem_por_painel": Decimal(str(model.montagem_por_painel)),
            "valor_projeto": Decimal(str(model.valor_projeto)),
            "hsp_padrao": Decimal(str(model.hsp_padrao)),
            "perda_padrao": Decimal(str(model.perda_padrao)),
            "overload_inversor": Decimal(str(model.overload_inversor)),
            "tarifa_energia_atual": Decimal(str(model.tarifa_energia_atual)),
            "inflacao_energetica_anual": Decimal(str(model.inflacao_energetica_anual)),
            "perda_eficiencia_anual": Decimal(str(model.perda_eficiencia_anual)),
            "taxas_maquininha": {k: Decimal(str(v)) for k, v in model.taxas_maquininha.items()},
            "faixas_material_eletrico": model.faixas_material_eletrico,
            "consumo_veiculo": Decimal(str(model.consumo_veiculo)),
            "preco_combustivel": Decimal(str(model.preco_combustivel)),
            "margem_deslocamento": Decimal(str(model.margem_deslocamento)),
            "cidades_sem_cobranca": model.cidades_sem_cobranca,
        }
        return Premissa(**data)
