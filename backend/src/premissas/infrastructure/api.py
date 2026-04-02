from uuid import UUID

from fastapi import APIRouter, Depends

from src.auth.infrastructure.dependencies import get_current_tenant
from src.premissas.application.dtos import AtualizarPremissaRequest, PremissaResponse
from src.premissas.application.use_cases import (
    AtualizarPremissaUseCase,
    ObterPremissaAtivaUseCase,
)
from src.premissas.infrastructure.dependencies import (
    get_atualizar_premissa_use_case,
    get_obter_premissa_ativa_use_case,
)
from src.tenant.domain.entities import Tenant

router = APIRouter(prefix="/api/v1/premissas", tags=["premissas"])


@router.get("/ativa", response_model=PremissaResponse)
async def obter_premissa_ativa(
    tenant: Tenant = Depends(get_current_tenant),
    use_case: ObterPremissaAtivaUseCase = Depends(get_obter_premissa_ativa_use_case),
) -> PremissaResponse:
    """Obter premissas ativas do tenant (cria default se não existir)"""
    premissa = await use_case.execute(tenant.id)
    return PremissaResponse.model_validate(premissa)


@router.put("/{premissa_id}", response_model=PremissaResponse)
async def atualizar_premissa(
    premissa_id: UUID,
    dto: AtualizarPremissaRequest,
    use_case: AtualizarPremissaUseCase = Depends(get_atualizar_premissa_use_case),
) -> PremissaResponse:
    """Atualizar premissas (apenas admin)"""
    premissa = await use_case.execute(premissa_id, dto)
    return PremissaResponse.model_validate(premissa)
