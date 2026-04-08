import pytest
from uuid import uuid4

from src.shared.exceptions import ConflictError, NotFoundError
from src.tenant.application.dtos import (
    AtualizarBrandingRequest,
    AtualizarTenantRequest,
    CriarTenantRequest,
)
from src.tenant.application.use_cases import (
    AtualizarBrandingUseCase,
    AtualizarTenantUseCase,
    CriarTenantUseCase,
    ObterTenantUseCase,
)
from src.tenant.infrastructure.repositories import SQLAlchemyTenantRepository


@pytest.mark.asyncio
async def test_criar_tenant_sucesso(db_session):
    repo = SQLAlchemyTenantRepository(db_session)
    use_case = CriarTenantUseCase(repo)

    dto = CriarTenantRequest(
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

    tenant = await use_case.execute(dto)

    assert tenant.id is not None
    assert tenant.nome_fantasia == "Solar Tech"
    assert tenant.cnpj == "12.345.678/0001-90"
    assert tenant.plano == "free"


@pytest.mark.asyncio
async def test_criar_tenant_cnpj_duplicado_erro(db_session):
    repo = SQLAlchemyTenantRepository(db_session)
    use_case = CriarTenantUseCase(repo)

    dto = CriarTenantRequest(
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

    await use_case.execute(dto)

    with pytest.raises(ConflictError) as exc:
        await use_case.execute(dto)

    assert "ja existe" in str(exc.value.message)


@pytest.mark.asyncio
async def test_obter_tenant_sucesso(db_session):
    repo = SQLAlchemyTenantRepository(db_session)
    criar_use_case = CriarTenantUseCase(repo)
    obter_use_case = ObterTenantUseCase(repo)

    dto = CriarTenantRequest(
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

    tenant_criado = await criar_use_case.execute(dto)
    tenant_obtido = await obter_use_case.execute(tenant_criado.id)

    assert tenant_obtido.id == tenant_criado.id
    assert tenant_obtido.nome_fantasia == "Solar Tech"


@pytest.mark.asyncio
async def test_obter_tenant_nao_encontrado_erro(db_session):
    repo = SQLAlchemyTenantRepository(db_session)
    use_case = ObterTenantUseCase(repo)

    with pytest.raises(NotFoundError):
        await use_case.execute(uuid4())


@pytest.mark.asyncio
async def test_atualizar_tenant_sucesso(db_session):
    repo = SQLAlchemyTenantRepository(db_session)
    criar_use_case = CriarTenantUseCase(repo)
    atualizar_use_case = AtualizarTenantUseCase(repo)

    dto_criar = CriarTenantRequest(
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

    tenant = await criar_use_case.execute(dto_criar)

    dto_atualizar = AtualizarTenantRequest(
        nome_fantasia="Solar Tech Atualizada",
        cidade="Campo Grande",
    )

    tenant_atualizado = await atualizar_use_case.execute(tenant.id, dto_atualizar)

    assert tenant_atualizado.nome_fantasia == "Solar Tech Atualizada"
    assert tenant_atualizado.cidade == "Campo Grande"
    assert tenant_atualizado.cnpj == "12.345.678/0001-90"


@pytest.mark.asyncio
async def test_atualizar_branding_sucesso(db_session):
    repo = SQLAlchemyTenantRepository(db_session)
    criar_use_case = CriarTenantUseCase(repo)
    branding_use_case = AtualizarBrandingUseCase(repo)

    dto_criar = CriarTenantRequest(
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

    tenant = await criar_use_case.execute(dto_criar)

    dto_branding = AtualizarBrandingRequest(
        logo_url="https://example.com/logo.png",
        cor_primaria="#FF0000",
        cor_secundaria="#00FF00",
    )

    tenant_atualizado = await branding_use_case.execute(tenant.id, dto_branding)

    assert tenant_atualizado.logo_url == "https://example.com/logo.png"
    assert tenant_atualizado.cor_primaria == "#FF0000"
    assert tenant_atualizado.cor_secundaria == "#00FF00"
