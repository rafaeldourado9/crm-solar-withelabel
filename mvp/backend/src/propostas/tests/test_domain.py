"""Testes unitários do domínio de Propostas."""
from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest

from src.propostas.domain.entities import Proposta, StatusProposta


def _proposta_factory(**kwargs) -> Proposta:
    defaults = dict(
        tenant_id=uuid4(),
        orcamento_id=uuid4(),
        cliente_id=uuid4(),
        numero="PROP-2024-0001",
        cliente_nome="João Silva",
        cliente_cpf_cnpj="12345678901",
        potencia_sistema_kwp=Decimal("5.280"),
        quantidade_paineis=12,
        painel_modelo="Risen 440W",
        inversor_modelo="Growatt 5kW",
        geracao_mensal_kwh=Decimal("580.00"),
        valor_final=Decimal("25000.00"),
        forma_pagamento="avista",
        data_validade=date.today() + timedelta(days=30),
    )
    defaults.update(kwargs)
    return Proposta(**defaults)


def test_proposta_criada_status_pendente():
    proposta = _proposta_factory()
    assert proposta.status == StatusProposta.PENDENTE


def test_aceitar_proposta_pendente():
    proposta = _proposta_factory()
    proposta.aceitar()
    assert proposta.status == StatusProposta.ACEITA


def test_recusar_proposta_pendente():
    proposta = _proposta_factory()
    proposta.recusar()
    assert proposta.status == StatusProposta.RECUSADA


def test_aceitar_proposta_ja_aceita_falha():
    proposta = _proposta_factory()
    proposta.aceitar()
    with pytest.raises(ValueError):
        proposta.aceitar()


def test_recusar_proposta_aceita_falha():
    proposta = _proposta_factory()
    proposta.aceitar()
    with pytest.raises(ValueError):
        proposta.recusar()
