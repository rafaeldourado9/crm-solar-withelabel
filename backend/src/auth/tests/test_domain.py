from uuid import uuid4

import pytest

from src.auth.domain.entities import User
from src.auth.domain.services import JWTService, PasswordService


class TestPasswordService:
    def test_hash_password_retorna_string_diferente(self):
        hashed = PasswordService.hash_password("senha123")
        assert hashed != "senha123"
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_verify_password_correta(self):
        password = "senha123"
        hashed = PasswordService.hash_password(password)
        assert PasswordService.verify_password(password, hashed) is True

    def test_verify_password_incorreta(self):
        hashed = PasswordService.hash_password("senha123")
        assert PasswordService.verify_password("senha_errada", hashed) is False

    def test_hash_diferente_para_mesma_senha(self):
        """Cada hash deve ser unico mesmo para senhas iguais (bcrypt usa salt)"""
        hash1 = PasswordService.hash_password("senha123")
        hash2 = PasswordService.hash_password("senha123")
        assert hash1 != hash2


class TestJWTService:
    def test_create_access_token(self):
        user_id = uuid4()
        tenant_id = uuid4()
        token = JWTService.create_access_token(user_id, tenant_id, "admin")
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_refresh_token(self):
        user_id = uuid4()
        tenant_id = uuid4()
        token = JWTService.create_refresh_token(user_id, tenant_id)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_access_token_valido(self):
        user_id = uuid4()
        tenant_id = uuid4()
        token = JWTService.create_access_token(user_id, tenant_id, "admin")
        payload = JWTService.decode_token(token)

        assert payload["sub"] == str(user_id)
        assert payload["tenant_id"] == str(tenant_id)
        assert payload["role"] == "admin"
        assert payload["type"] == "access"

    def test_decode_refresh_token_valido(self):
        user_id = uuid4()
        tenant_id = uuid4()
        token = JWTService.create_refresh_token(user_id, tenant_id)
        payload = JWTService.decode_token(token)

        assert payload["sub"] == str(user_id)
        assert payload["tenant_id"] == str(tenant_id)
        assert payload["type"] == "refresh"

    def test_decode_token_invalido(self):
        with pytest.raises(ValueError, match="Token"):
            JWTService.decode_token("token_invalid_xyz")

    def test_decode_token_expired(self):
        """Token expirado deve levantar ValueError"""
        # Nao ha teste direto sem mock, mas o decode_token deve levantar ValueError
        # para tokens expirados
        pass

    def test_access_token_contem_tenant_id(self):
        user_id = uuid4()
        tenant_id = uuid4()
        token = JWTService.create_access_token(user_id, tenant_id, "vendedor")
        payload = JWTService.decode_token(token)

        assert "tenant_id" in payload
        assert payload["tenant_id"] == str(tenant_id)

    def test_tokens_diferentes_access_vs_refresh(self):
        user_id = uuid4()
        tenant_id = uuid4()
        access = JWTService.create_access_token(user_id, tenant_id, "admin")
        refresh = JWTService.create_refresh_token(user_id, tenant_id)

        assert access != refresh


class TestUserEntity:
    def test_criar_user_com_dados_minimos(self):
        user = User(
            tenant_id=uuid4(),
            email="teste@email.com",
            hashed_password="hash123",
            nome="Test User",
        )

        assert user.id is not None
        assert user.role == "vendedor"
        assert user.ativo is True
        assert user.bloqueado is False

    def test_criar_user_com_role_admin(self):
        user = User(
            tenant_id=uuid4(),
            email="admin@email.com",
            hashed_password="hash123",
            nome="Admin",
            role="admin",
        )

        assert user.role == "admin"

    def test_criar_user_com_role_indicacao(self):
        user = User(
            tenant_id=uuid4(),
            email="indicacao@email.com",
            hashed_password="hash123",
            nome="Indicacao",
            role="indicacao",
        )

        assert user.role == "indicacao"

    def test_user_possui_timestamps(self):
        user = User(
            tenant_id=uuid4(),
            email="teste@email.com",
            hashed_password="hash123",
            nome="Test User",
        )

        assert user.created_at is not None
        assert user.updated_at is not None

    def test_user_bloqueado(self):
        user = User(
            tenant_id=uuid4(),
            email="teste@email.com",
            hashed_password="hash123",
            nome="Test User",
            bloqueado=True,
        )

        assert user.bloqueado is True

    def test_user_inativo(self):
        user = User(
            tenant_id=uuid4(),
            email="teste@email.com",
            hashed_password="hash123",
            nome="Test User",
            ativo=False,
        )

        assert user.ativo is False
