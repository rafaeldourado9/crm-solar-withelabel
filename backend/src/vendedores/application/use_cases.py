"""Use cases do módulo Vendedores (camada sobre User com role vendedor/indicacao)."""
from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.domain.entities import User
from src.auth.domain.services import PasswordService
from src.auth.infrastructure.models import UserModel
from src.auth.infrastructure.repositories import SQLAlchemyUserRepository
from src.clientes.infrastructure.models import ClienteModel
from src.contratos.infrastructure.models import ContratoModel
from src.premissas.infrastructure.repositories import SQLAlchemyPremissaRepository
from src.shared.exceptions import ConflictError, ForbiddenError, NotFoundError, ValidationError
from src.vendedores.application.dtos import (
    AtualizarVendedorRequest,
    CriarVendedorRequest,
    ResumoVendedorResponse,
    VendedorResponse,
)

_ROLES_VENDEDOR = ["vendedor", "indicacao"]


class ListarVendedoresUseCase:
    def __init__(self, session: AsyncSession):
        self.repo = SQLAlchemyUserRepository(session)

    async def execute(self, tenant_id: UUID) -> list[VendedorResponse]:
        users = await self.repo.list_by_tenant(tenant_id, roles=_ROLES_VENDEDOR)
        return [VendedorResponse.model_validate(u) for u in users]


class CriarVendedorUseCase:
    def __init__(self, session: AsyncSession):
        self.repo = SQLAlchemyUserRepository(session)

    async def execute(self, dto: CriarVendedorRequest, tenant_id: UUID) -> VendedorResponse:
        if dto.role not in _ROLES_VENDEDOR:
            raise ValidationError(f"Role inválido. Use: {', '.join(_ROLES_VENDEDOR)}")

        existente = await self.repo.get_by_email(dto.email, tenant_id)
        if existente:
            raise ConflictError("Email já cadastrado")

        if len(dto.password) < 6:
            raise ValidationError("Senha deve ter mínimo 6 caracteres")

        user = User(
            tenant_id=tenant_id,
            email=dto.email,
            hashed_password=PasswordService.hash_password(dto.password),
            nome=dto.nome,
            role=dto.role,
        )
        criado = await self.repo.create(user)
        return VendedorResponse.model_validate(criado)


class AtualizarVendedorUseCase:
    def __init__(self, session: AsyncSession):
        self.repo = SQLAlchemyUserRepository(session)

    async def execute(
        self, vendedor_id: UUID, tenant_id: UUID, dto: AtualizarVendedorRequest
    ) -> VendedorResponse:
        user = await self.repo.get_by_id(vendedor_id)
        if not user or user.tenant_id != tenant_id or user.role not in _ROLES_VENDEDOR:
            raise NotFoundError("Vendedor não encontrado")

        if dto.nome is not None:
            user.nome = dto.nome
        if dto.role is not None:
            if dto.role not in _ROLES_VENDEDOR:
                raise ValidationError(f"Role inválido. Use: {', '.join(_ROLES_VENDEDOR)}")
            user.role = dto.role

        atualizado = await self.repo.update(user)
        return VendedorResponse.model_validate(atualizado)


class BloquearVendedorUseCase:
    def __init__(self, session: AsyncSession):
        self.repo = SQLAlchemyUserRepository(session)

    async def execute(self, vendedor_id: UUID, tenant_id: UUID) -> VendedorResponse:
        user = await self.repo.get_by_id(vendedor_id)
        if not user or user.tenant_id != tenant_id or user.role not in _ROLES_VENDEDOR:
            raise NotFoundError("Vendedor não encontrado")
        user.bloqueado = not user.bloqueado
        atualizado = await self.repo.update(user)
        return VendedorResponse.model_validate(atualizado)


class ResetarSenhaUseCase:
    def __init__(self, session: AsyncSession):
        self.repo = SQLAlchemyUserRepository(session)

    async def execute(self, vendedor_id: UUID, tenant_id: UUID, nova_senha: str) -> None:
        user = await self.repo.get_by_id(vendedor_id)
        if not user or user.tenant_id != tenant_id or user.role not in _ROLES_VENDEDOR:
            raise NotFoundError("Vendedor não encontrado")
        if len(nova_senha) < 6:
            raise ValidationError("Senha deve ter mínimo 6 caracteres")
        await self.repo.reset_password(vendedor_id, nova_senha)


class DeletarVendedorUseCase:
    def __init__(self, session: AsyncSession):
        self.repo = SQLAlchemyUserRepository(session)

    async def execute(self, vendedor_id: UUID, tenant_id: UUID) -> None:
        user = await self.repo.get_by_id(vendedor_id)
        if not user or user.tenant_id != tenant_id or user.role not in _ROLES_VENDEDOR:
            raise NotFoundError("Vendedor não encontrado")
        await self.repo.delete(vendedor_id)


class ResumoVendedorUseCase:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = SQLAlchemyUserRepository(session)
        self.premissa_repo = SQLAlchemyPremissaRepository(session)

    async def execute(self, vendedor_id: UUID, tenant_id: UUID) -> ResumoVendedorResponse:
        user = await self.user_repo.get_by_id(vendedor_id)
        if not user or user.tenant_id != tenant_id or user.role not in _ROLES_VENDEDOR:
            raise NotFoundError("Vendedor não encontrado")

        # Total de clientes
        r_clientes = await self.session.execute(
            select(func.count(ClienteModel.id)).where(
                ClienteModel.tenant_id == tenant_id,
                ClienteModel.vendedor_id == vendedor_id,
            )
        )
        total_clientes = r_clientes.scalar_one()

        # Total e valor de contratos
        r_contratos = await self.session.execute(
            select(
                func.count(ContratoModel.id),
                func.coalesce(func.sum(ContratoModel.valor_total), 0),
            ).where(
                ContratoModel.tenant_id == tenant_id,
                ContratoModel.vendedor_id == vendedor_id,
            )
        )
        total_contratos, valor_total = r_contratos.one()
        valor_total = Decimal(str(valor_total))

        # Comissão estimada via premissas
        premissa = await self.premissa_repo.get_ativa(tenant_id)
        comissao_pct = Decimal(str(premissa.comissao_percentual)) if premissa else Decimal("5")
        comissao_estimada = (valor_total * comissao_pct / 100).quantize(Decimal("0.01"))

        return ResumoVendedorResponse(
            vendedor_id=vendedor_id,
            nome=user.nome,
            total_clientes=total_clientes,
            total_contratos=total_contratos,
            valor_total_vendas=valor_total,
            comissao_estimada=comissao_estimada,
        )
