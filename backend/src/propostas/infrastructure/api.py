from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from src.auth.domain.entities import User
from src.auth.infrastructure.dependencies import get_current_tenant, get_current_user
from src.propostas.application.dtos import (
    CriarPropostaRequest,
    PropostaListResponse,
    PropostaResponse,
)
from src.propostas.application.use_cases import (
    AceitarPropostaUseCase,
    CriarPropostaUseCase,
    ListarPropostasUseCase,
    ObterPropostaUseCase,
    RecusarPropostaUseCase,
)
from src.propostas.infrastructure.dependencies import (
    get_aceitar_proposta_use_case,
    get_criar_proposta_use_case,
    get_listar_propostas_use_case,
    get_obter_proposta_use_case,
    get_recusar_proposta_use_case,
)
from src.tenant.domain.entities import Tenant

router = APIRouter(prefix="/api/v1/propostas", tags=["propostas"])


@router.post("", response_model=PropostaResponse, status_code=status.HTTP_201_CREATED)
async def criar_proposta(
    dto: CriarPropostaRequest,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    use_case: CriarPropostaUseCase = Depends(get_criar_proposta_use_case),
) -> PropostaResponse:
    return await use_case.execute(dto, tenant.id, user)


@router.get("", response_model=PropostaListResponse)
async def listar_propostas(
    cliente_id: UUID | None = None,
    status_filtro: str | None = None,
    offset: int = 0,
    limit: int = 20,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    use_case: ListarPropostasUseCase = Depends(get_listar_propostas_use_case),
) -> PropostaListResponse:
    return await use_case.execute(tenant.id, user, cliente_id, status_filtro, offset, limit)


@router.get("/{proposta_id}", response_model=PropostaResponse)
async def obter_proposta(
    proposta_id: UUID,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    use_case: ObterPropostaUseCase = Depends(get_obter_proposta_use_case),
) -> PropostaResponse:
    return await use_case.execute(proposta_id, tenant.id)


@router.post("/{proposta_id}/aceitar", response_model=PropostaResponse)
async def aceitar_proposta(
    proposta_id: UUID,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    use_case: AceitarPropostaUseCase = Depends(get_aceitar_proposta_use_case),
) -> PropostaResponse:
    return await use_case.execute(proposta_id, tenant.id)


@router.post("/{proposta_id}/recusar", response_model=PropostaResponse)
async def recusar_proposta(
    proposta_id: UUID,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    use_case: RecusarPropostaUseCase = Depends(get_recusar_proposta_use_case),
) -> PropostaResponse:
    return await use_case.execute(proposta_id, tenant.id)
