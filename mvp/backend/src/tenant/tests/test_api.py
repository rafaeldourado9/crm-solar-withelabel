import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_criar_tenant_via_api(client: AsyncClient):
    payload = {
        "nome_fantasia": "Solar Tech",
        "razao_social": "Solar Tech LTDA",
        "cnpj": "12.345.678/0001-90",
        "endereco": "Rua A, 123",
        "cidade": "Dourados",
        "estado": "MS",
        "cep": "79800-000",
        "representante_nome": "João Silva",
        "representante_cpf": "123.456.789-00",
    }

    response = await client.post("/api/v1/tenants/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["nome_fantasia"] == "Solar Tech"
    assert data["cnpj"] == "12.345.678/0001-90"
    assert data["plano"] == "free"
    assert "id" in data


@pytest.mark.asyncio
async def test_criar_tenant_cnpj_duplicado_retorna_409(client: AsyncClient):
    payload = {
        "nome_fantasia": "Solar Tech",
        "razao_social": "Solar Tech LTDA",
        "cnpj": "12.345.678/0001-90",
        "endereco": "Rua A, 123",
        "cidade": "Dourados",
        "estado": "MS",
        "cep": "79800-000",
        "representante_nome": "João Silva",
        "representante_cpf": "123.456.789-00",
    }

    await client.post("/api/v1/tenants/", json=payload)
    response = await client.post("/api/v1/tenants/", json=payload)

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_obter_tenant_via_api(client: AsyncClient):
    payload = {
        "nome_fantasia": "Solar Tech",
        "razao_social": "Solar Tech LTDA",
        "cnpj": "12.345.678/0001-91",
        "endereco": "Rua A, 123",
        "cidade": "Dourados",
        "estado": "MS",
        "cep": "79800-000",
        "representante_nome": "João Silva",
        "representante_cpf": "123.456.789-00",
    }

    create_response = await client.post("/api/v1/tenants/", json=payload)
    tenant_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/tenants/{tenant_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == tenant_id
    assert data["nome_fantasia"] == "Solar Tech"


@pytest.mark.asyncio
async def test_obter_tenant_inexistente_retorna_404(client: AsyncClient):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.get(f"/api/v1/tenants/{fake_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_atualizar_tenant_via_api(client: AsyncClient):
    payload = {
        "nome_fantasia": "Solar Tech",
        "razao_social": "Solar Tech LTDA",
        "cnpj": "12.345.678/0001-92",
        "endereco": "Rua A, 123",
        "cidade": "Dourados",
        "estado": "MS",
        "cep": "79800-000",
        "representante_nome": "João Silva",
        "representante_cpf": "123.456.789-00",
    }

    create_response = await client.post("/api/v1/tenants/", json=payload)
    tenant_id = create_response.json()["id"]

    update_payload = {
        "nome_fantasia": "Solar Tech Atualizada",
        "cidade": "Campo Grande",
    }

    response = await client.put(f"/api/v1/tenants/{tenant_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["nome_fantasia"] == "Solar Tech Atualizada"
    assert data["cidade"] == "Campo Grande"


@pytest.mark.asyncio
async def test_atualizar_branding_via_api(client: AsyncClient):
    payload = {
        "nome_fantasia": "Solar Tech",
        "razao_social": "Solar Tech LTDA",
        "cnpj": "12.345.678/0001-93",
        "endereco": "Rua A, 123",
        "cidade": "Dourados",
        "estado": "MS",
        "cep": "79800-000",
        "representante_nome": "João Silva",
        "representante_cpf": "123.456.789-00",
    }

    create_response = await client.post("/api/v1/tenants/", json=payload)
    tenant_id = create_response.json()["id"]

    branding_payload = {
        "logo_url": "https://example.com/logo.png",
        "cor_primaria": "#FF0000",
        "cor_secundaria": "#00FF00",
    }

    response = await client.put(
        f"/api/v1/tenants/{tenant_id}/branding", json=branding_payload
    )

    assert response.status_code == 200
    data = response.json()
    assert data["logo_url"] == "https://example.com/logo.png"
    assert data["cor_primaria"] == "#FF0000"
    assert data["cor_secundaria"] == "#00FF00"
