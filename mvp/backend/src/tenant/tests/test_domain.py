import pytest
from uuid import uuid4

from src.tenant.domain.entities import Tenant


def test_criar_tenant_com_dados_minimos():
    tenant = Tenant(
        nome_fantasia="Solar Tech",
        razao_social="Solar Tech LTDA",
        cnpj="12.345.678/0001-90",
        endereco="Rua A, 123",
        cidade="Dourados",
        estado="MS",
        cep="79800-000",
        representante_nome="João Silva",
        representante_cpf="123.456.789-00",
    )

    assert tenant.nome_fantasia == "Solar Tech"
    assert tenant.plano == "free"
    assert tenant.ativo is True
    assert tenant.cor_primaria == "#1E40AF"
    assert tenant.cor_secundaria == "#F59E0B"


def test_criar_tenant_com_dados_completos():
    tenant = Tenant(
        nome_fantasia="MAB Energia",
        razao_social="MAB Energia Solar LTDA",
        cnpj="12.345.678/0001-90",
        endereco="Av. Principal, 500",
        cidade="Dourados",
        estado="MS",
        cep="79800-000",
        representante_nome="Maria Santos",
        representante_cpf="987.654.321-00",
        representante_rg="12.345.678-9",
        banco_nome="Banco do Brasil",
        banco_agencia="1234-5",
        banco_conta="12345-6",
        banco_titular="MAB Energia Solar LTDA",
        logo_url="https://example.com/logo.png",
        cor_primaria="#FF0000",
        cor_secundaria="#00FF00",
        dominio_customizado="app.mabenergia.com.br",
        plano="pro",
    )

    assert tenant.banco_nome == "Banco do Brasil"
    assert tenant.logo_url == "https://example.com/logo.png"
    assert tenant.plano == "pro"
    assert tenant.dominio_customizado == "app.mabenergia.com.br"


def test_tenant_possui_id_e_timestamps():
    tenant = Tenant(
        nome_fantasia="Test",
        razao_social="Test LTDA",
        cnpj="12.345.678/0001-90",
        endereco="Rua A",
        cidade="Dourados",
        estado="MS",
        cep="79800-000",
        representante_nome="Test",
        representante_cpf="123.456.789-00",
    )

    assert tenant.id is not None
    assert tenant.created_at is not None
    assert tenant.updated_at is not None
