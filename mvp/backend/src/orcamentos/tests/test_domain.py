from decimal import Decimal

import pytest

from src.orcamentos.domain.exceptions import InversorExcedidoError
from src.orcamentos.domain.services import SolarCalculatorService
from src.orcamentos.domain.value_objects import (
    CustoBreakdown,
    FaixaMaterialEletrico,
    FormaPagamento,
    MargemConfig,
)


class TestDimensionar:
    def test_dimensionar_consumo_500kwh_painel_550w(self):
        """500 kWh/mes, painel 550W, HSP 5.5, perda 20%
        potencia_necessaria = 500 / (5.5 * 30 * 0.80) = 3.787 kW
        qtd_paineis = CEIL(3787 / 550) = 7
        potencia_kwp = 7 * 550 / 1000 = 3.850
        geracao = 3.85 * 5.5 * 30 * 0.80 = 508.20 kWh"""
        resultado = SolarCalculatorService.dimensionar(
            consumo_mensal_kwh=Decimal("500"),
            painel_potencia_w=550,
            hsp=Decimal("5.5"),
            perda=Decimal("0.20"),
        )
        assert resultado.quantidade_paineis == 7
        assert resultado.potencia_sistema_kwp == Decimal("3.850")
        assert resultado.geracao_mensal_kwh == Decimal("508.20")

    def test_dimensionar_consumo_1000kwh_painel_550w(self):
        """1000 kWh/mes -> 14 paineis, 7.700 kWp"""
        resultado = SolarCalculatorService.dimensionar(
            consumo_mensal_kwh=Decimal("1000"),
            painel_potencia_w=550,
            hsp=Decimal("5.5"),
            perda=Decimal("0.20"),
        )
        assert resultado.quantidade_paineis == 14
        assert resultado.potencia_sistema_kwp == Decimal("7.700")

    def test_dimensionar_consumo_baixo_retorna_minimo_1_painel(self):
        """Consumo muito baixo ainda retorna ao menos 1 painel"""
        resultado = SolarCalculatorService.dimensionar(
            consumo_mensal_kwh=Decimal("10"),
            painel_potencia_w=550,
            hsp=Decimal("5.5"),
            perda=Decimal("0.20"),
        )
        assert resultado.quantidade_paineis >= 1


class TestValidarInversor:
    def test_validar_inversor_dentro_do_limite(self):
        """7 paineis * 550W = 3850W <= 5000 * 1.70 = 8500W -> OK"""
        result = SolarCalculatorService.validar_inversor(
            quantidade_paineis=7,
            painel_potencia_w=550,
            inversor_potencia_nominal_w=5000,
            overload=Decimal("0.70"),
        )
        assert result is True

    def test_validar_inversor_excede_limite_levanta_erro(self):
        """20 paineis * 550W = 11000W > 5000 * 1.70 = 8500W -> ERRO"""
        with pytest.raises(InversorExcedidoError):
            SolarCalculatorService.validar_inversor(
                quantidade_paineis=20,
                painel_potencia_w=550,
                inversor_potencia_nominal_w=5000,
                overload=Decimal("0.70"),
            )


class TestMaterialEletrico:
    def _faixas(self) -> list[FaixaMaterialEletrico]:
        return [
            FaixaMaterialEletrico(Decimal("0"), Decimal("3"), Decimal("250")),
            FaixaMaterialEletrico(Decimal("3"), Decimal("5"), Decimal("350")),
            FaixaMaterialEletrico(Decimal("5"), Decimal("6"), Decimal("400")),
            FaixaMaterialEletrico(Decimal("6"), Decimal("8"), Decimal("500")),
            FaixaMaterialEletrico(Decimal("8"), Decimal("10"), Decimal("900")),
        ]

    def test_material_eletrico_inversor_4kwp_retorna_350(self):
        """4 kWp esta na faixa 3-5 -> R$ 350"""
        resultado = SolarCalculatorService.calcular_material_eletrico(
            Decimal("4"), self._faixas()
        )
        assert resultado == Decimal("350")

    def test_material_eletrico_inversor_7kwp_retorna_500(self):
        """7 kWp esta na faixa 6-8 -> R$ 500"""
        resultado = SolarCalculatorService.calcular_material_eletrico(
            Decimal("7"), self._faixas()
        )
        assert resultado == Decimal("500")

    def test_material_eletrico_inversor_2kwp_retorna_250(self):
        resultado = SolarCalculatorService.calcular_material_eletrico(
            Decimal("2"), self._faixas()
        )
        assert resultado == Decimal("250")

    def test_material_eletrico_inversor_9kwp_retorna_900(self):
        resultado = SolarCalculatorService.calcular_material_eletrico(
            Decimal("9"), self._faixas()
        )
        assert resultado == Decimal("900")

    def test_material_eletrico_fallback_ultima_faixa(self):
        """Potencia acima de todas as faixas -> retorna ultima"""
        resultado = SolarCalculatorService.calcular_material_eletrico(
            Decimal("15"), self._faixas()
        )
        assert resultado == Decimal("900")


class TestSubtotal:
    def test_calcular_subtotal_completo(self):
        """valor_kit=15000 + montagem(7*70=490) + projeto(400) + estrutura(800)
           + material_eletrico(350) + itens_adicionais(200) + deslocamento(150)
           = 17390"""
        custos = CustoBreakdown(
            valor_kit=Decimal("15000"),
            montagem=Decimal("490"),
            projeto=Decimal("400"),
            estrutura=Decimal("800"),
            material_eletrico=Decimal("350"),
            itens_adicionais=Decimal("200"),
            deslocamento=Decimal("150"),
        )
        assert SolarCalculatorService.calcular_subtotal(custos) == Decimal("17390")


class TestAplicarMargens:
    def test_aplicar_margens_padrao(self):
        """Subtotal 17390, margens 18+5+6=29%
        valor_base = 17390 / (1-0.29) = 24492.96 -> arredonda 24500
        margem_desconto = 24500 * 0.02 = 490
        valor_com_margem = 24990 -> arredonda 25000
        VALOR_FINAL = 25000"""
        margem = MargemConfig(
            lucro=Decimal("18"),
            comissao=Decimal("5"),
            imposto=Decimal("6"),
            desconto_avista=Decimal("2"),
        )
        resultado = SolarCalculatorService.aplicar_margens(Decimal("17390"), margem)
        assert resultado == Decimal("25000")

    def test_markup_arredonda_para_centena_superior(self):
        """Qualquer valor quebrado arredonda para cima na centena"""
        margem = MargemConfig(
            lucro=Decimal("18"),
            comissao=Decimal("5"),
            imposto=Decimal("6"),
            desconto_avista=Decimal("2"),
        )
        resultado = SolarCalculatorService.aplicar_margens(Decimal("10000"), margem)
        # 10000 / 0.71 = 14084.51 -> 14100, +2% = 14382 -> 14400
        assert resultado % 100 == 0

    def test_aplicar_margens_subtotal_10000(self):
        margem = MargemConfig(
            lucro=Decimal("18"),
            comissao=Decimal("5"),
            imposto=Decimal("6"),
            desconto_avista=Decimal("2"),
        )
        resultado = SolarCalculatorService.aplicar_margens(Decimal("10000"), margem)
        assert resultado == Decimal("14400")


class TestJuros:
    def test_avista_sem_juros(self):
        """forma_pagamento='avista' -> valor_final inalterado"""
        forma = FormaPagamento(tipo="avista", taxa=Decimal("0"))
        valor_cobrado, parcela = SolarCalculatorService.aplicar_juros(Decimal("25000"), forma)
        assert valor_cobrado == Decimal("25000")
        assert parcela is None

    def test_parcelado_12x_aplica_8_porcento(self):
        """25000 * 1.08 = 27000, parcela = 27000/12 = 2250"""
        forma = FormaPagamento(tipo="12", taxa=Decimal("8"))
        valor_cobrado, parcela = SolarCalculatorService.aplicar_juros(Decimal("25000"), forma)
        assert valor_cobrado == Decimal("27000.00")
        assert parcela == Decimal("2250.00")

    def test_parcelado_6x_aplica_5_porcento(self):
        """25000 * 1.05 = 26250, parcela = 26250/6 = 4375"""
        forma = FormaPagamento(tipo="6", taxa=Decimal("5"))
        valor_cobrado, parcela = SolarCalculatorService.aplicar_juros(Decimal("25000"), forma)
        assert valor_cobrado == Decimal("26250.00")
        assert parcela == Decimal("4375.00")

    def test_parcelado_2x_aplica_2_5_porcento(self):
        forma = FormaPagamento(tipo="2", taxa=Decimal("2.5"))
        valor_cobrado, parcela = SolarCalculatorService.aplicar_juros(Decimal("25000"), forma)
        assert valor_cobrado == Decimal("25625.00")
        assert parcela == Decimal("12812.50")

    def test_parcelado_3x_aplica_3_5_porcento(self):
        forma = FormaPagamento(tipo="3", taxa=Decimal("3.5"))
        valor_cobrado, parcela = SolarCalculatorService.aplicar_juros(Decimal("25000"), forma)
        assert valor_cobrado == Decimal("25875.00")
        assert parcela == Decimal("8625.00")


class TestEconomia25Anos:
    def test_economia_ano_1(self):
        """geracao_mensal * 12 * (1 - 0.005*1/100) * tarifa * (1.08)^1"""
        resultados = SolarCalculatorService.calcular_economia_25_anos(
            geracao_mensal_kwh=Decimal("508.20"),
            tarifa_atual=Decimal("0.95"),
            inflacao_energetica=Decimal("0.08"),
            perda_eficiencia=Decimal("0.005"),
        )
        assert len(resultados) == 25
        assert resultados[0].ano == 1
        assert resultados[0].economia > Decimal("0")

    def test_economia_acumulada_25_anos_positiva(self):
        """Deve retornar valor > 0 e crescente"""
        resultados = SolarCalculatorService.calcular_economia_25_anos(
            geracao_mensal_kwh=Decimal("508.20"),
            tarifa_atual=Decimal("0.95"),
            inflacao_energetica=Decimal("0.08"),
            perda_eficiencia=Decimal("0.005"),
        )
        assert resultados[-1].economia_acumulada > Decimal("0")
        # Acumulada deve ser crescente
        for i in range(1, len(resultados)):
            assert resultados[i].economia_acumulada > resultados[i - 1].economia_acumulada

    def test_economia_25_anos_retorna_25_itens(self):
        resultados = SolarCalculatorService.calcular_economia_25_anos(
            geracao_mensal_kwh=Decimal("508.20"),
            tarifa_atual=Decimal("0.95"),
            inflacao_energetica=Decimal("0.08"),
            perda_eficiencia=Decimal("0.005"),
        )
        assert len(resultados) == 25
        assert resultados[0].ano == 1
        assert resultados[24].ano == 25
