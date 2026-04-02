from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.auth.domain.entities import User
from src.auth.infrastructure.dependencies import get_current_tenant, get_current_user
from src.database import get_db
from src.shared.exceptions import ForbiddenError
from src.tenant.domain.entities import Tenant
from src.vendedores.application.dtos import (
    AtualizarVendedorRequest,
    CriarVendedorRequest,
    ResetarSenhaRequest,
    ResumoVendedorResponse,
    VendedorResponse,
)
from src.vendedores.application.use_cases import (
    AtualizarVendedorUseCase,
    BloquearVendedorUseCase,
    CriarVendedorUseCase,
    DeletarVendedorUseCase,
    ListarVendedoresUseCase,
    ResetarSenhaUseCase,
    ResumoVendedorUseCase,
)
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/v1/vendedores", tags=["vendedores"])


def _require_admin(user: User) -> None:
    if user.role not in ("admin", "staff"):
        raise ForbiddenError("Apenas administradores podem gerenciar vendedores")


@router.get("", response_model=list[VendedorResponse])
async def listar_vendedores(
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[VendedorResponse]:
    return await ListarVendedoresUseCase(db).execute(tenant.id)


@router.post("", response_model=VendedorResponse, status_code=status.HTTP_201_CREATED)
async def criar_vendedor(
    dto: CriarVendedorRequest,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> VendedorResponse:
    _require_admin(user)
    return await CriarVendedorUseCase(db).execute(dto, tenant.id)


@router.put("/{vendedor_id}", response_model=VendedorResponse)
async def atualizar_vendedor(
    vendedor_id: UUID,
    dto: AtualizarVendedorRequest,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> VendedorResponse:
    _require_admin(user)
    return await AtualizarVendedorUseCase(db).execute(vendedor_id, tenant.id, dto)


@router.post("/{vendedor_id}/bloquear", response_model=VendedorResponse)
async def bloquear_vendedor(
    vendedor_id: UUID,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> VendedorResponse:
    _require_admin(user)
    return await BloquearVendedorUseCase(db).execute(vendedor_id, tenant.id)


@router.post("/{vendedor_id}/resetar-senha", status_code=status.HTTP_204_NO_CONTENT)
async def resetar_senha(
    vendedor_id: UUID,
    dto: ResetarSenhaRequest,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    _require_admin(user)
    await ResetarSenhaUseCase(db).execute(vendedor_id, tenant.id, dto.nova_senha)


@router.get("/{vendedor_id}/resumo", response_model=ResumoVendedorResponse)
async def resumo_vendedor(
    vendedor_id: UUID,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ResumoVendedorResponse:
    return await ResumoVendedorUseCase(db).execute(vendedor_id, tenant.id)


@router.delete("/{vendedor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_vendedor(
    vendedor_id: UUID,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    _require_admin(user)
    await DeletarVendedorUseCase(db).execute(vendedor_id, tenant.id)
