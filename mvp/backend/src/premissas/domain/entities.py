from decimal import Decimal
from uuid import UUID

from pydantic import Field

from src.shared.base_entity import BaseEntity


class Premissa(BaseEntity):
    tenant_id: UUID
    ativa: bool = True

    # Margens e Custos
    margem_lucro_percentual: Decimal = Field(default=Decimal("18"))
    comissao_percentual: Decimal = Field(default=Decimal("5"))
    imposto_percentual: Decimal = Field(default=Decimal("6"))
    margem_desconto_avista_percentual: Decimal = Field(default=Decimal("2"))
    montagem_por_painel: Decimal = Field(default=Decimal("70"))
    valor_projeto: Decimal = Field(default=Decimal("400"))

    # Parametros Tecnicos
    hsp_padrao: Decimal = Field(default=Decimal("5.5"))
    perda_padrao: Decimal = Field(default=Decimal("0.20"))
    overload_inversor: Decimal = Field(default=Decimal("0.70"))

    # Energia
    tarifa_energia_atual: Decimal = Field(default=Decimal("0.95"))
    inflacao_energetica_anual: Decimal = Field(default=Decimal("0.08"))
    perda_eficiencia_anual: Decimal = Field(default=Decimal("0.005"))

    # Taxas Maquininha (JSON)
    taxas_maquininha: dict[str, Decimal] = Field(
        default_factory=lambda: {
            "2": Decimal("2.5"),
            "3": Decimal("3.5"),
            "6": Decimal("5.0"),
            "12": Decimal("8.0"),
        }
    )

    # Material Eletrico por Faixa (JSON)
    faixas_material_eletrico: list[dict] = Field(
        default_factory=lambda: [
            {"potencia_min": 0, "potencia_max": 3, "valor": 250},
            {"potencia_min": 3, "potencia_max": 5, "valor": 350},
            {"potencia_min": 5, "potencia_max": 6, "valor": 400},
            {"potencia_min": 6, "potencia_max": 8, "valor": 500},
            {"potencia_min": 8, "potencia_max": 10, "valor": 900},
        ]
    )

    # Deslocamento
    consumo_veiculo: Decimal = Field(default=Decimal("10"))
    preco_combustivel: Decimal = Field(default=Decimal("6.75"))
    margem_deslocamento: Decimal = Field(default=Decimal("0.20"))
    cidades_sem_cobranca: list[str] = Field(default_factory=lambda: ["Itapora", "Dourados"])

    def calcular_material_eletrico(self, potencia_inversor_kwp: Decimal) -> Decimal:
        """Calcula valor do material elétrico baseado na potência do INVERSOR"""
        for faixa in self.faixas_material_eletrico:
            if faixa["potencia_min"] <= potencia_inversor_kwp < faixa["potencia_max"]:
                return Decimal(str(faixa["valor"]))
        return Decimal(str(self.faixas_material_eletrico[-1]["valor"]))
