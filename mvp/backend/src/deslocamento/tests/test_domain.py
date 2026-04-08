from decimal import Decimal

import pytest

from src.deslocamento.domain.services import DeslocamentoCalculator


class TestDeslocamentoCalculator:
    def test_cidade_isenta_custo_zero(self):
        """Itapora ou Dourados -> custo = 0"""
        resultado = DeslocamentoCalculator.calcular(
            cidade_cliente="Dourados",
            distancia_km=Decimal("100"),
            consumo_veiculo=Decimal("10"),
            preco_combustivel=Decimal("6.75"),
            margem_deslocamento=Decimal("0.20"),
            cidades_sem_cobranca=["Itapora", "Dourados"],
        )
        assert resultado.custo == Decimal("0")
        assert resultado.cidade_isenta is True

    def test_cidade_isenta_case_insensitive(self):
        resultado = DeslocamentoCalculator.calcular(
            cidade_cliente="dourados",
            distancia_km=Decimal("100"),
            consumo_veiculo=Decimal("10"),
            preco_combustivel=Decimal("6.75"),
            margem_deslocamento=Decimal("0.20"),
            cidades_sem_cobranca=["Itapora", "Dourados"],
        )
        assert resultado.custo == Decimal("0")
        assert resultado.cidade_isenta is True

    def test_cidade_isenta_itapora(self):
        resultado = DeslocamentoCalculator.calcular(
            cidade_cliente="Itapora",
            distancia_km=Decimal("50"),
            consumo_veiculo=Decimal("10"),
            preco_combustivel=Decimal("6.75"),
            margem_deslocamento=Decimal("0.20"),
            cidades_sem_cobranca=["Itapora", "Dourados"],
        )
        assert resultado.custo == Decimal("0")
        assert resultado.cidade_isenta is True

    def test_deslocamento_100km(self):
        """100km * 2 = 200km / 10 km/L = 20L * 6.75 = 135 * 1.20 = 162"""
        resultado = DeslocamentoCalculator.calcular(
            cidade_cliente="Ponta Pora",
            distancia_km=Decimal("100"),
            consumo_veiculo=Decimal("10"),
            preco_combustivel=Decimal("6.75"),
            margem_deslocamento=Decimal("0.20"),
            cidades_sem_cobranca=["Itapora", "Dourados"],
        )
        assert resultado.custo == Decimal("162.00")
        assert resultado.cidade_isenta is False
        assert resultado.distancia_km == Decimal("100")

    def test_deslocamento_50km(self):
        """50km * 2 = 100km / 10 = 10L * 6.75 = 67.50 * 1.20 = 81.00"""
        resultado = DeslocamentoCalculator.calcular(
            cidade_cliente="Maracaju",
            distancia_km=Decimal("50"),
            consumo_veiculo=Decimal("10"),
            preco_combustivel=Decimal("6.75"),
            margem_deslocamento=Decimal("0.20"),
            cidades_sem_cobranca=["Itapora", "Dourados"],
        )
        assert resultado.custo == Decimal("81.00")
        assert resultado.cidade_isenta is False

    def test_deslocamento_distancia_zero_cidade_nao_isenta(self):
        resultado = DeslocamentoCalculator.calcular(
            cidade_cliente="Cidade Qualquer",
            distancia_km=Decimal("0"),
            consumo_veiculo=Decimal("10"),
            preco_combustivel=Decimal("6.75"),
            margem_deslocamento=Decimal("0.20"),
            cidades_sem_cobranca=["Itapora", "Dourados"],
        )
        assert resultado.custo == Decimal("0.00")
        assert resultado.cidade_isenta is False
