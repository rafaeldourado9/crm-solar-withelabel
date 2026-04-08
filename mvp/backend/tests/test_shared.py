from decimal import Decimal

import pytest

from src.shared.exceptions import DomainError, NotFoundError, ValidationError
from src.shared.utils import format_brl, numero_por_extenso
from src.shared.value_objects import validate_cpf, validate_cnpj, validate_cpf_cnpj


class TestFormatBrl:
    def test_valor_simples(self):
        assert format_brl(Decimal("1234.56")) == "R$ 1.234,56"

    def test_valor_grande(self):
        assert format_brl(Decimal("25000.00")) == "R$ 25.000,00"

    def test_valor_zero(self):
        assert format_brl(Decimal("0.00")) == "R$ 0,00"

    def test_centavos(self):
        assert format_brl(Decimal("0.99")) == "R$ 0,99"


class TestNumeroPorExtenso:
    def test_zero(self):
        assert numero_por_extenso(Decimal("0")) == "zero reais"

    def test_um_real(self):
        assert numero_por_extenso(Decimal("1")) == "um real"

    def test_cem_reais(self):
        assert numero_por_extenso(Decimal("100")) == "cem reais"

    def test_mil_reais(self):
        assert numero_por_extenso(Decimal("1000")) == "mil reais"

    def test_vinte_cinco_mil(self):
        result = numero_por_extenso(Decimal("25000"))
        assert "vinte e cinco mil" in result
        assert "reais" in result

    def test_com_centavos(self):
        result = numero_por_extenso(Decimal("1.50"))
        assert "um real" in result
        assert "cinquenta centavos" in result

    def test_cento_e_cinquenta(self):
        result = numero_por_extenso(Decimal("150"))
        assert "cento e cinquenta reais" == result


class TestValidacoes:
    def test_cpf_valido(self):
        assert validate_cpf("051.536.511-42") == "05153651142"

    def test_cpf_invalido(self):
        with pytest.raises(ValidationError):
            validate_cpf("123")

    def test_cnpj_valido(self):
        assert validate_cnpj("38.068.450/0001-99") == "38068450000199"

    def test_cnpj_invalido(self):
        with pytest.raises(ValidationError):
            validate_cnpj("123")

    def test_cpf_cnpj_detecta_cpf(self):
        assert validate_cpf_cnpj("051.536.511-42") == "05153651142"

    def test_cpf_cnpj_detecta_cnpj(self):
        assert validate_cpf_cnpj("38.068.450/0001-99") == "38068450000199"

    def test_cpf_cnpj_invalido(self):
        with pytest.raises(ValidationError):
            validate_cpf_cnpj("123456")


class TestExceptions:
    def test_not_found_error(self):
        err = NotFoundError("Cliente", "abc-123")
        assert "Cliente" in err.message
        assert "abc-123" in err.message

    def test_domain_error(self):
        err = DomainError("algo deu errado")
        assert str(err) == "algo deu errado"
