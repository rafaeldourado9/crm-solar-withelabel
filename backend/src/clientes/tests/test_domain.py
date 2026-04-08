import pytest

from src.clientes.domain.entities import Cliente, StatusCliente, TRANSICOES_VALIDAS
from src.shared.exceptions import ValidationError


class TestStatusCliente:
    def test_status_inicial_orcamento(self):
        cliente = Cliente(
            tenant_id="00000000-0000-0000-0000-000000000001",
            nome="Teste",
            cpf_cnpj="05153651142",
        )
        assert cliente.status == StatusCliente.ORCAMENTO

    def test_transicao_orcamento_para_proposta(self):
        cliente = Cliente(
            tenant_id="00000000-0000-0000-0000-000000000001",
            nome="Teste",
            cpf_cnpj="05153651142",
        )
        cliente.transicionar(StatusCliente.PROPOSTA)
        assert cliente.status == StatusCliente.PROPOSTA

    def test_transicao_proposta_para_contrato(self):
        cliente = Cliente(
            tenant_id="00000000-0000-0000-0000-000000000001",
            nome="Teste",
            cpf_cnpj="05153651142",
            status=StatusCliente.PROPOSTA,
        )
        cliente.transicionar(StatusCliente.CONTRATO)
        assert cliente.status == StatusCliente.CONTRATO

    def test_transicao_invalida_orcamento_para_contrato(self):
        cliente = Cliente(
            tenant_id="00000000-0000-0000-0000-000000000001",
            nome="Teste",
            cpf_cnpj="05153651142",
        )
        with pytest.raises(ValidationError, match="Transicao invalida"):
            cliente.transicionar(StatusCliente.CONTRATO)

    def test_transicao_contrato_nao_pode_voltar(self):
        cliente = Cliente(
            tenant_id="00000000-0000-0000-0000-000000000001",
            nome="Teste",
            cpf_cnpj="05153651142",
            status=StatusCliente.CONTRATO,
        )
        with pytest.raises(ValidationError, match="Transicao invalida"):
            cliente.transicionar(StatusCliente.ORCAMENTO)

    def test_pode_transicionar_retorna_true(self):
        cliente = Cliente(
            tenant_id="00000000-0000-0000-0000-000000000001",
            nome="Teste",
            cpf_cnpj="05153651142",
        )
        assert cliente.pode_transicionar(StatusCliente.PROPOSTA) is True

    def test_pode_transicionar_retorna_false(self):
        cliente = Cliente(
            tenant_id="00000000-0000-0000-0000-000000000001",
            nome="Teste",
            cpf_cnpj="05153651142",
        )
        assert cliente.pode_transicionar(StatusCliente.CONTRATO) is False

    def test_proposta_pode_voltar_para_orcamento(self):
        cliente = Cliente(
            tenant_id="00000000-0000-0000-0000-000000000001",
            nome="Teste",
            cpf_cnpj="05153651142",
            status=StatusCliente.PROPOSTA,
        )
        cliente.transicionar(StatusCliente.ORCAMENTO)
        assert cliente.status == StatusCliente.ORCAMENTO
