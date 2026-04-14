import pytest
from httpx import AsyncClient
from uuid import uuid4

from src.tenant.application.use_cases import CriarTenantUseCase
from src.tenant.application.dtos import CriarTenantRequest
from src.tenant.infrastructure.repositories import SQLAlchemyTenantRepository
from src.auth.application.use_cases import CriarUserUseCase
from src.auth.infrastructure.repositories import SQLAlchemyUserRepository


def _cnpj_unico() -> str:
    """Gera um CNPJ unico para evitar conflito de unique constraint"""
    return f"12.345.678/0001-{uuid4().hex[:2].upper()}"


async def _criar_tenant_e_user(db_session, email: str = "test@email.com", password: str = "senha123"):
    """Helper para criar tenant e user para testes"""
    tenant_repo = SQLAlchemyTenantRepository(db_session)
    tenant_uc = CriarTenantUseCase(tenant_repo)
    
    tenant = await tenant_uc.execute(
        CriarTenantRequest(
            nome_fantasia="Test Tenant",
            razao_social="Test Tenant LTDA",
            cnpj=_cnpj_unico(),
            endereco="Rua Test, 123",
            cidade="Test City",
            estado="TS",
            cep="12345-000",
            representante_nome="Rep Name",
            representante_cpf="123.456.789-00",
        )
    )
    await db_session.commit()
    
    user_repo = SQLAlchemyUserRepository(db_session)
    user_uc = CriarUserUseCase(user_repo)
    
    user = await user_uc.execute(
        email=email,
        password=password,
        nome="Test User",
        tenant_id=tenant.id,
    )
    await db_session.commit()
    
    return tenant, user


class TestAuthAPI:
    @pytest.mark.asyncio
    async def test_login_sucesso(self, client: AsyncClient, db_session):
        tenant, _ = await _criar_tenant_e_user(db_session)

        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@email.com", "password": "senha123"},
            headers={"X-Tenant-ID": str(tenant.id)},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_senha_incorreta_retorna_422(self, client: AsyncClient, db_session):
        tenant, _ = await _criar_tenant_e_user(db_session)

        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@email.com", "password": "senha_errada"},
            headers={"X-Tenant-ID": str(tenant.id)},
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_refresh_token_sucesso(self, client: AsyncClient, db_session):
        from src.auth.application.use_cases import LoginUseCase
        from src.auth.application.dtos import LoginRequest
        from src.auth.infrastructure.repositories import SQLAlchemyUserRepository

        tenant, _ = await _criar_tenant_e_user(db_session)

        # Login para obter refresh token
        user_repo = SQLAlchemyUserRepository(db_session)
        login_use_case = LoginUseCase(user_repo)
        login_result = await login_use_case.execute(
            LoginRequest(email="test@email.com", password="senha123"),
            tenant.id,
        )

        # Refresh token
        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": login_result.refresh_token},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    @pytest.mark.asyncio
    async def test_get_me_com_token_valido(self, client: AsyncClient, db_session):
        from src.auth.application.use_cases import LoginUseCase
        from src.auth.application.dtos import LoginRequest
        from src.auth.infrastructure.repositories import SQLAlchemyUserRepository

        tenant, _ = await _criar_tenant_e_user(db_session)

        # Login
        user_repo = SQLAlchemyUserRepository(db_session)
        login_use_case = LoginUseCase(user_repo)
        login_result = await login_use_case.execute(
            LoginRequest(email="test@email.com", password="senha123"),
            tenant.id,
        )

        # GET /me
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {login_result.access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@email.com"
        assert data["nome"] == "Test User"
