from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from src.auth.domain.entities import User
from src.auth.infrastructure.dependencies import get_current_tenant, get_current_user
from src.clientes.application.dtos import (
    AtualizarClienteRequest,
    ClienteListResponse,
    ClienteResponse,
    CriarClienteRequest,
)
from src.clientes.application.use_cases import (
    AtualizarClienteUseCase,
    CriarClienteUseCase,
    DeletarClienteUseCase,
    ListarClientesUseCase,
    ObterClienteUseCase,
)
from src.clientes.infrastructure.dependencies import (
    get_atualizar_cliente_use_case,
    get_criar_cliente_use_case,
    get_deletar_cliente_use_case,
    get_listar_clientes_use_case,
    get_obter_cliente_use_case,
)
from src.shared.exceptions import ForbiddenError
from src.tenant.domain.entities import Tenant

router = APIRouter(prefix="/api/v1/clientes", tags=["clientes"])


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def criar_cliente(
    dto: CriarClienteRequest,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    use_case: CriarClienteUseCase = Depends(get_criar_cliente_use_case),
) -> ClienteResponse:
    cliente = await use_case.execute(dto, tenant.id, user.role, user.id)
    return ClienteResponse.model_validate(cliente)


@router.get("/", response_model=ClienteListResponse)
async def listar_clientes(
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    use_case: ListarClientesUseCase = Depends(get_listar_clientes_use_case),
    status_filter: str | None = Query(None, alias="status"),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
) -> ClienteListResponse:
    items, total = await use_case.execute(
        tenant.id, user.role, user.id, status=status_filter, offset=offset, limit=limit
    )
    return ClienteListResponse(
        items=[ClienteResponse.model_validate(c) for c in items],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.get("/{cliente_id}", response_model=ClienteResponse)
async def obter_cliente(
    cliente_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    use_case: ObterClienteUseCase = Depends(get_obter_cliente_use_case),
) -> ClienteResponse:
    cliente = await use_case.execute(cliente_id, tenant.id, user.role, user.id)
    return ClienteResponse.model_validate(cliente)


@router.put("/{cliente_id}", response_model=ClienteResponse)
async def atualizar_cliente(
    cliente_id: UUID,
    dto: AtualizarClienteRequest,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    use_case: AtualizarClienteUseCase = Depends(get_atualizar_cliente_use_case),
) -> ClienteResponse:
    cliente = await use_case.execute(cliente_id, dto, tenant.id, user.role, user.id)
    return ClienteResponse.model_validate(cliente)


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_cliente(
    cliente_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    use_case: DeletarClienteUseCase = Depends(get_deletar_cliente_use_case),
) -> None:
    if user.role != "admin":
        raise ForbiddenError("Apenas admin pode deletar clientes")
    await use_case.execute(cliente_id, tenant.id)
