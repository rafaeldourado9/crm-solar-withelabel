from uuid import UUID

from src.auth.application.dtos import LoginRequest, LoginResponse, RefreshResponse
from src.auth.domain.entities import User
from src.auth.domain.repositories import UserRepository
from src.auth.domain.services import JWTService, PasswordService
from src.shared.exceptions import ForbiddenError, NotFoundError, ValidationError


class LoginUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, dto: LoginRequest, tenant_id: UUID) -> LoginResponse:
        user = await self.user_repo.get_by_email(dto.email, tenant_id)
        if not user:
            raise NotFoundError("Usuario", dto.email)

        if not PasswordService.verify_password(dto.password, user.hashed_password):
            raise ValidationError("Senha incorreta")

        if not user.ativo or user.bloqueado:
            raise ForbiddenError("Usuario inativo ou bloqueado")

        access_token = JWTService.create_access_token(user.id, user.tenant_id, user.role)
        refresh_token = JWTService.create_refresh_token(user.id, user.tenant_id)

        return LoginResponse(access_token=access_token, refresh_token=refresh_token)


class RefreshTokenUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, refresh_token: str) -> RefreshResponse:
        try:
            payload = JWTService.decode_token(refresh_token)
        except ValueError as e:
            raise ValidationError(str(e))

        if payload.get("type") != "refresh":
            raise ValidationError("Token invalido")

        user_id = UUID(payload["sub"])
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("Usuario")

        if not user.ativo or user.bloqueado:
            raise ForbiddenError("Usuario inativo ou bloqueado")

        access_token = JWTService.create_access_token(user.id, user.tenant_id, user.role)
        return RefreshResponse(access_token=access_token)


class CriarUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, email: str, password: str, nome: str, tenant_id: UUID, role: str = "vendedor") -> User:
        existing = await self.user_repo.get_by_email(email, tenant_id)
        if existing:
            raise ValidationError(f"Usuario com email {email} ja existe")

        hashed_password = PasswordService.hash_password(password)
        user = User(
            tenant_id=tenant_id,
            email=email,
            hashed_password=hashed_password,
            nome=nome,
            role=role,
        )
        return await self.user_repo.create(user)
