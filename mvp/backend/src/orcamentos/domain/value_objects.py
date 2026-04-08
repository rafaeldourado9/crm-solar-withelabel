from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CustoBreakdown:
    valor_kit: Decimal
    montagem: Decimal
    projeto: Decimal
    estrutura: Decimal
    material_eletrico: Decimal
    itens_adicionais: Decimal
    deslocamento: Decimal

    def total(self) -> Decimal:
        return (
            self.valor_kit
            + self.montagem
            + self.projeto
            + self.estrutura
            + self.material_eletrico
            + self.itens_adicionais
            + self.deslocamento
        )


@dataclass(frozen=True)
class MargemConfig:
    lucro: Decimal
    comissao: Decimal
    imposto: Decimal
    desconto_avista: Decimal


@dataclass(frozen=True)
class FormaPagamento:
    tipo: str  # "avista", "2", "3", "6", "12"
    taxa: Decimal  # percentual da maquininha


@dataclass(frozen=True)
class Dimensionamento:
    consumo_mensal_kwh: Decimal
    potencia_necessaria_kw: Decimal
    quantidade_paineis: int
    potencia_sistema_kwp: Decimal
    geracao_mensal_kwh: Decimal


@dataclass(frozen=True)
class FaixaMaterialEletrico:
    potencia_min: Decimal
    potencia_max: Decimal
    valor: Decimal


@dataclass(frozen=True)
class EconomiaAnual:
    ano: int
    tarifa: Decimal
    geracao_kwh: Decimal
    economia: Decimal
    economia_acumulada: Decimal
