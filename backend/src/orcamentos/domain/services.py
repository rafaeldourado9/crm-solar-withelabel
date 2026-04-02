from decimal import ROUND_CEILING, ROUND_HALF_UP, Decimal
from math import ceil

from src.orcamentos.domain.exceptions import InversorExcedidoError
from src.orcamentos.domain.value_objects import (
    CustoBreakdown,
    Dimensionamento,
    EconomiaAnual,
    FaixaMaterialEletrico,
    FormaPagamento,
    MargemConfig,
)


class SolarCalculatorService:
    """Logica pura de calculo solar - sem dependencias externas."""

    @staticmethod
    def dimensionar(
        consumo_mensal_kwh: Decimal,
        painel_potencia_w: int,
        hsp: Decimal,
        perda: Decimal,
    ) -> Dimensionamento:
        potencia_necessaria_kw = consumo_mensal_kwh / (hsp * 30 * (1 - perda))
        quantidade_paineis = max(1, ceil(float(potencia_necessaria_kw * 1000) / painel_potencia_w))
        potencia_sistema_kwp = Decimal(str(quantidade_paineis * painel_potencia_w)) / 1000
        geracao_mensal_kwh = potencia_sistema_kwp * hsp * 30 * (1 - perda)

        return Dimensionamento(
            consumo_mensal_kwh=consumo_mensal_kwh,
            potencia_necessaria_kw=potencia_necessaria_kw.quantize(Decimal("0.001"), ROUND_HALF_UP),
            quantidade_paineis=quantidade_paineis,
            potencia_sistema_kwp=potencia_sistema_kwp.quantize(Decimal("0.001"), ROUND_HALF_UP),
            geracao_mensal_kwh=geracao_mensal_kwh.quantize(Decimal("0.01"), ROUND_HALF_UP),
        )

    @staticmethod
    def validar_inversor(
        quantidade_paineis: int,
        painel_potencia_w: int,
        inversor_potencia_nominal_w: int,
        overload: Decimal,
    ) -> bool:
        potencia_paineis_total = quantidade_paineis * painel_potencia_w
        potencia_maxima_inversor = int(inversor_potencia_nominal_w * (1 + overload))

        if potencia_paineis_total > potencia_maxima_inversor:
            raise InversorExcedidoError(potencia_paineis_total, potencia_maxima_inversor)
        return True

    @staticmethod
    def calcular_material_eletrico(
        potencia_inversor_kwp: Decimal,
        faixas: list[FaixaMaterialEletrico],
    ) -> Decimal:
        for faixa in faixas:
            if faixa.potencia_min <= potencia_inversor_kwp < faixa.potencia_max:
                return faixa.valor
        return faixas[-1].valor

    @staticmethod
    def calcular_subtotal(custos: CustoBreakdown) -> Decimal:
        return custos.total()

    @staticmethod
    def aplicar_margens(subtotal: Decimal, margem: MargemConfig) -> Decimal:
        total_percentual = (margem.comissao + margem.imposto + margem.lucro) / 100
        valor_base = subtotal / (1 - total_percentual)
        valor_base_arredondado = Decimal(str(ceil(float(valor_base) / 100) * 100))

        margem_desconto = valor_base_arredondado * (margem.desconto_avista / 100)
        valor_com_margem = valor_base_arredondado + margem_desconto
        valor_final = Decimal(str(ceil(float(valor_com_margem) / 100) * 100))

        return valor_final

    @staticmethod
    def aplicar_juros(
        valor_final: Decimal, forma_pagamento: FormaPagamento
    ) -> tuple[Decimal, Decimal | None]:
        if forma_pagamento.tipo == "avista":
            return valor_final, None

        taxa = forma_pagamento.taxa
        valor_cobrado = valor_final * (1 + taxa / 100)
        parcelas = int(forma_pagamento.tipo)
        valor_parcela = (valor_cobrado / parcelas).quantize(Decimal("0.01"), ROUND_HALF_UP)

        return valor_cobrado.quantize(Decimal("0.01"), ROUND_HALF_UP), valor_parcela

    @staticmethod
    def calcular_economia_25_anos(
        geracao_mensal_kwh: Decimal,
        tarifa_atual: Decimal,
        inflacao_energetica: Decimal,
        perda_eficiencia: Decimal,
    ) -> list[EconomiaAnual]:
        resultados: list[EconomiaAnual] = []
        economia_acumulada = Decimal("0")

        for ano in range(1, 26):
            tarifa_ano = tarifa_atual * (1 + inflacao_energetica) ** ano
            geracao_ano = geracao_mensal_kwh * 12 * (1 - perda_eficiencia * ano / 100)
            economia_ano = (geracao_ano * tarifa_ano).quantize(Decimal("0.01"), ROUND_HALF_UP)
            economia_acumulada += economia_ano

            resultados.append(
                EconomiaAnual(
                    ano=ano,
                    tarifa=tarifa_ano.quantize(Decimal("0.01"), ROUND_HALF_UP),
                    geracao_kwh=geracao_ano.quantize(Decimal("0.01"), ROUND_HALF_UP),
                    economia=economia_ano,
                    economia_acumulada=economia_acumulada.quantize(Decimal("0.01"), ROUND_HALF_UP),
                )
            )

        return resultados
