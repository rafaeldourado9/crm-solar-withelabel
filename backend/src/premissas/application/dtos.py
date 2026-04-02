from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class AtualizarPremissaRequest(BaseModel):
    margem_lucro_percentual: Decimal | None = None
    comissao_percentual: Decimal | None = None
    imposto_percentual: Decimal | None = None
    margem_desconto_avista_percentual: Decimal | None = None
    montagem_por_painel: Decimal | None = None
    valor_projeto: Decimal | None = None
    hsp_padrao: Decimal | None = None
    perda_padrao: Decimal | None = None
    overload_inversor: Decimal | None = None
    tarifa_energia_atual: Decimal | None = None
    inflacao_energetica_anual: Decimal | None = None
    perda_eficiencia_anual: Decimal | None = None
    taxas_maquininha: dict[str, Decimal] | None = None
    faixas_material_eletrico: list[dict] | None = None
    consumo_veiculo: Decimal | None = None
    preco_combustivel: Decimal | None = None
    margem_deslocamento: Decimal | None = None
    cidades_sem_cobranca: list[str] | None = None


class PremissaResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    ativa: bool
    margem_lucro_percentual: Decimal
    comissao_percentual: Decimal
    imposto_percentual: Decimal
    margem_desconto_avista_percentual: Decimal
    montagem_por_painel: Decimal
    valor_projeto: Decimal
    hsp_padrao: Decimal
    perda_padrao: Decimal
    overload_inversor: Decimal
    tarifa_energia_atual: Decimal
    inflacao_energetica_anual: Decimal
    perda_eficiencia_anual: Decimal
    taxas_maquininha: dict[str, Decimal]
    faixas_material_eletrico: list[dict]
    consumo_veiculo: Decimal
    preco_combustivel: Decimal
    margem_deslocamento: Decimal
    cidades_sem_cobranca: list[str]

    model_config = {"from_attributes": True}
