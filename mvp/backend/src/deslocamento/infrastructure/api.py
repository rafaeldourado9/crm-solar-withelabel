from fastapi import APIRouter, Depends

from src.auth.infrastructure.dependencies import get_current_tenant
from src.deslocamento.application.dtos import CalcularDeslocamentoRequest, DeslocamentoResponse
from src.deslocamento.application.use_cases import CalcularDeslocamentoUseCase
from src.deslocamento.infrastructure.dependencies import get_calcular_deslocamento_use_case
from src.tenant.domain.entities import Tenant

router = APIRouter(prefix="/api/v1/deslocamento", tags=["deslocamento"])


@router.post("/calcular", response_model=DeslocamentoResponse)
async def calcular_deslocamento(
    dto: CalcularDeslocamentoRequest,
    tenant: Tenant = Depends(get_current_tenant),
    use_case: CalcularDeslocamentoUseCase = Depends(get_calcular_deslocamento_use_case),
) -> DeslocamentoResponse:
    """Calcular custo de deslocamento para instalacao"""
    return await use_case.execute(dto, tenant.id)
