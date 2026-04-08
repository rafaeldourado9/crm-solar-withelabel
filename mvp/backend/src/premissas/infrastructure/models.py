from sqlalchemy import Boolean, ForeignKey, JSON, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.base_model import BaseModel


class PremissaModel(BaseModel):
    __tablename__ = "premissas"

    tenant_id: Mapped[PG_UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("tenants.id"), index=True
    )
    ativa: Mapped[bool] = mapped_column(Boolean, default=True)

    # Margens e Custos
    margem_lucro_percentual: Mapped[Numeric] = mapped_column(Numeric(5, 2), default=18)
    comissao_percentual: Mapped[Numeric] = mapped_column(Numeric(5, 2), default=5)
    imposto_percentual: Mapped[Numeric] = mapped_column(Numeric(5, 2), default=6)
    margem_desconto_avista_percentual: Mapped[Numeric] = mapped_column(Numeric(5, 2), default=2)
    montagem_por_painel: Mapped[Numeric] = mapped_column(Numeric(10, 2), default=70)
    valor_projeto: Mapped[Numeric] = mapped_column(Numeric(10, 2), default=400)

    # Parametros Tecnicos
    hsp_padrao: Mapped[Numeric] = mapped_column(Numeric(5, 2), default=5.5)
    perda_padrao: Mapped[Numeric] = mapped_column(Numeric(5, 4), default=0.20)
    overload_inversor: Mapped[Numeric] = mapped_column(Numeric(5, 4), default=0.70)

    # Energia
    tarifa_energia_atual: Mapped[Numeric] = mapped_column(Numeric(10, 2), default=0.95)
    inflacao_energetica_anual: Mapped[Numeric] = mapped_column(Numeric(5, 4), default=0.08)
    perda_eficiencia_anual: Mapped[Numeric] = mapped_column(Numeric(5, 4), default=0.005)

    # JSON fields
    taxas_maquininha: Mapped[dict] = mapped_column(JSON)
    faixas_material_eletrico: Mapped[list] = mapped_column(JSON)

    # Deslocamento
    consumo_veiculo: Mapped[Numeric] = mapped_column(Numeric(5, 2), default=10)
    preco_combustivel: Mapped[Numeric] = mapped_column(Numeric(10, 2), default=6.75)
    margem_deslocamento: Mapped[Numeric] = mapped_column(Numeric(5, 4), default=0.20)
    cidades_sem_cobranca: Mapped[list] = mapped_column(JSON)
