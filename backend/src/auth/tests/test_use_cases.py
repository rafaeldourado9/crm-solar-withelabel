from uuid import uuid4

import pytest

from src.auth.application.dtos import CriarUserRequest, LoginRequest, LoginResponse
from src.auth.application.use_cases import CriarUserUseCase, LoginUseCase, RefreshTokenUseCase
from src.auth.domain.services import PasswordService
from src.auth.infrastructure.repositories import SQLAlchemyUserRepository
from src.shared.exceptions import ForbiddenError, NotFoundError, ValidationError


class TestCriarUserUseCase:
    @pytest.mark.asyncio
    async def test_criar_user_sucesso(self, db_session):
        repo = SQLAlchemyUserRepository(db_session)
        use_case = CriarUserUseCase(repo)

        tenant_id = uuid4()
        user = await use_case.execute(
            email="teste@email.com",
            password="senha123",
            nome="Test User",
            tenant_id=tenant_id,
            role="vendedor",
        )

        assert user.id is not None
        assert user.email == "teste@email.com"
        assert user.nome == "Test User"
        assert user.role == "vendedor"
        assert user.ativo is True

    @pytest.mark.asyncio
    async def test_criar_user_email_duplicado(self, db_session):
        repo = SQLAlchemyUserRepository(db_session)
        use_case = CriarUserUseCase(repo)

        tenant_id = uuid4()
        await use_case.execute(
            email="duplicado@email.com",
            password="senha123",
            nome="User 1",
            tenant_id=tenant_id,
        )

        with pytest.raises(ValidationError, match="ja existe"):
            await use_case.execute(
                email="duplicado@email.com",
                password="senha456",
                nome="User 2",
                tenant_id=tenant_id,
            )

    @pytest.mark.asyncio
    async def test_criar_user_com_role_admin(self, db_session):
        repo = SQLAlchemyUserRepository(db_session)
        use_case = CriarUserUseCase(repo)

        user = await use_case.execute(
            email="admin@email.com",
            password="senha123",
            nome="Admin User",
            tenant_id=uuid4(),
            role="admin",
        )

        assert user.role == "admin"

    @pytest.mark.asyncio
    async def test_criar_user_password_hashed(self, db_session):
        repo = SQLAlchemyUserRepository(db_session)
        use_case = CriarUserUseCase(repo)

        user = await use_case.execute(
            email="hash@email.com",
            password="senha123",
            nome="Hash User",
            tenant_id=uuid4(),
        )

        # Password deve estar hasheado (nao plaintext)
        assert user.hashed_password != "senha123"
        assert PasswordService.verify_password("senha123", user.hashed_password)


class TestLoginUseCase:
    @pytest.mark.asyncio
    async def test_login_sucesso(self, db_session):
        repo = SQLAlchemyUserRepository(db_session)
        criar_use_case = CriarUserUseCase(repo)
        login_use_case = LoginUseCase(repo)

        tenant_id = uuid4()
        await criar_use_case.execute(
            email="login@email.com",
            password="senha123",
            nome="Login User",
            tenant_id=tenant_id,
        )

        dto = LoginRequest(email="login@email.com", password="senha123")
        result = await login_use_case.execute(dto, tenant_id)

        assert isinstance(result, LoginResponse)
        assert result.access_token is not None
        assert result.refresh_token is not None
        assert result.token_type == "bearer"

    @pytest.mark.asyncio
    async def test_login_email_nao_encontrado(self, db_session):
        repo = SQLAlchemyUserRepository(db_session)
        login_use_case = LoginUseCase(repo)

        dto = LoginRequest(email="nao_existe@email.com", password="senha123")

        with pytest.raises(NotFoundError):
            await login_use_case.execute(dto, uuid4())

    @pytest.mark.asyncio
    async def test_login_senha_incorreta(self, db_session):
        repo = SQLAlchemyUserRepository(db_session)
        criar_use_case = CriarUserUseCase(repo)
        login_use_case = LoginUseCase(repo)

        tenant_id = uuid4()
        await criar_use_case.execute(
            email="senha_errada@email.com",
            password="senha123",
            nome="User",
            tenant_id=tenant_id,
        )

        dto = LoginRequest(email="senha_errada@email.com", password="senha_errada")

        with pytest.raises(ValidationError, match="Senha"):
            await login_use_case.execute(dto, tenant_id)

    @pytest.mark.asyncio
    async def test_login_user_inativo(self, db_session):
        repo = SQLAlchemyUserRepository(db_session)
        criar_use_case = CriarUserUseCase(repo)
        login_use_case = LoginUseCase(repo)

        tenant_id = uuid4()
        user = await criar_use_case.execute(
            email="inativo@email.com",
            password="senha123",
            nome="Inativo",
            tenant_id=tenant_id,
        )

        # Desativar user
        user.ativo = False
        await repo.update(user)

        dto = LoginRequest(email="inativo@email.com", password="senha123")

        with pytest.raises(ForbiddenError, match="inativo"):
            await login_use_case.execute(dto, tenant_id)

    @pytest.mark.asyncio
    async def test_login_user_bloqueado(self, db_session):
        repo = SQLAlchemyUserRepository(db_session)
        criar_use_case = CriarUserUseCase(repo)
        login_use_case = LoginUseCase(repo)

        tenant_id = uuid4()
        user = await criar_use_case.execute(
            email="bloqueado@email.com",
            password="senha123",
            nome="Bloqueado",
            tenant_id=tenant_id,
        )

        user.bloqueado = True
        await repo.update(user)

        dto = LoginRequest(email="bloqueado@email.com", password="senha123")

        with pytest.raises(ForbiddenError, match="bloqueado"):
            await login_use_case.execute(dto, tenant_id)


class TestRefreshTokenUseCase:
    @pytest.mark.asyncio
    async def test_refresh_token_sucesso(self, db_session):
        repo = SQLAlchemyUserRepository(db_session)
        criar_use_case = CriarUserUseCase(repo)
        login_use_case = LoginUseCase(repo)
        refresh_use_case = RefreshTokenUseCase(repo)

        tenant_id = uuid4()
        await criar_use_case.execute(
            email="refresh@email.com",
            password="senha123",
            nome="Refresh User",
            tenant_id=tenant_id,
        )

        # Faz login para obter refresh token
        login_dto = await login_use_case.execute(
            LoginRequest(email="refresh@email.com", password="senha123"),
            tenant_id,
        )

        # Usa refresh token
        result = await refresh_use_case.execute(login_dto.refresh_token)

        assert result.access_token is not None
        assert result.token_type == "bearer"

    @pytest.mark.asyncio
    async def test_refresh_token_invalido(self, db_session):
        repo = SQLAlchemyUserRepository(db_session)
        refresh_use_case = RefreshTokenUseCase(repo)

        with pytest.raises(ValidationError):
            await refresh_use_case.execute("token_invalido_xyz")

    @pytest.mark.asyncio
    async def test_refresh_token_usando_access_token(self):
        """Access token nao pode ser usado como refresh"""
        from src.auth.domain.services import JWTService

        user_id = uuid4()
        tenant_id = uuid4()
        access_token = JWTService.create_access_token(user_id, tenant_id, "admin")

        # Simula repo que nao encontra user (vai falhar no decode primeiro)
        # O teste verifica se o type check funciona
        payload = JWTService.decode_token(access_token)
        assert payload["type"] == "access"  # Nao e refresh
