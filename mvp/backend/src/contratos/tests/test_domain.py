"""Testes unitários do domínio de Contratos + TemplateEngine + numero_por_extenso."""
from decimal import Decimal
from uuid import uuid4

import pytest

from src.contratos.domain.entities import Contrato, StatusContrato
from src.documentos.domain.services import TemplateEngine, numero_por_extenso


def _contrato_factory(**kwargs) -> Contrato:
    defaults = dict(
        tenant_id=uuid4(),
        proposta_id=uuid4(),
        cliente_id=uuid4(),
        numero="CONT-2024-0001",
        cliente_nome="Maria Santos",
        cliente_cpf_cnpj="98765432100",
        empresa_razao_social="Solar Tech Ltda",
        empresa_cnpj="12345678000195",
        potencia_total_kwp=Decimal("6.600"),
        quantidade_paineis=15,
        valor_total=Decimal("32000.00"),
    )
    defaults.update(kwargs)
    return Contrato(**defaults)


# --- Testes entidade Contrato ---

def test_contrato_criado_como_rascunho():
    c = _contrato_factory()
    assert c.status == StatusContrato.RASCUNHO


def test_assinar_contrato_rascunho():
    c = _contrato_factory()
    c.assinar()
    assert c.status == StatusContrato.ASSINADO


def test_iniciar_execucao_apos_assinado():
    c = _contrato_factory()
    c.assinar()
    c.iniciar_execucao()
    assert c.status == StatusContrato.EM_EXECUCAO


def test_concluir_contrato_em_execucao():
    c = _contrato_factory()
    c.assinar()
    c.iniciar_execucao()
    c.concluir()
    assert c.status == StatusContrato.CONCLUIDO


def test_assinar_contrato_ja_assinado_falha():
    c = _contrato_factory()
    c.assinar()
    with pytest.raises(ValueError):
        c.assinar()


# --- Testes numero_por_extenso ---

def test_zero():
    assert numero_por_extenso(Decimal("0")) == "zero reais"


def test_valor_inteiro_simples():
    assert numero_por_extenso(Decimal("1")) == "um real"


def test_valor_com_centavos():
    result = numero_por_extenso(Decimal("1.50"))
    assert "real" in result
    assert "cinquenta" in result


def test_valor_mil():
    result = numero_por_extenso(Decimal("1000"))
    assert "mil" in result


def test_valor_tipico_solar():
    result = numero_por_extenso(Decimal("32000.00"))
    assert "trinta" in result
    assert "dois" in result
    assert "mil" in result
    assert "reais" in result


def test_valor_grande():
    result = numero_por_extenso(Decimal("1000000"))
    assert "milhão" in result


# --- Testes TemplateEngine ---

def test_substituir_variavel_simples():
    texto = "Olá {{NOME}}, seu valor é {{VALOR}}."
    result = TemplateEngine.substituir_texto(texto, {"NOME": "João", "VALOR": "R$ 100"})
    assert result == "Olá João, seu valor é R$ 100."


def test_variavel_nao_encontrada_mantida():
    texto = "{{VAR_INEXISTENTE}}"
    result = TemplateEngine.substituir_texto(texto, {})
    assert result == "{{VAR_INEXISTENTE}}"


def test_extrair_variaveis():
    texto = "{{CLIENTE_NOME}} comprou por {{VALOR_FINAL}}."
    vars_encontradas = TemplateEngine.extrair_variaveis(texto)
    assert vars_encontradas == {"CLIENTE_NOME", "VALOR_FINAL"}


def test_variaveis_faltando():
    texto = "{{A}} e {{B}} e {{C}}"
    faltando = TemplateEngine.variaveis_faltando(texto, {"A": "x", "B": "y"})
    assert faltando == ["C"]
