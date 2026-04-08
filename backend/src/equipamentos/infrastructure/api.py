from fastapi import APIRouter, Depends, status

from src.auth.infrastructure.dependencies import get_current_tenant
from src.equipamentos.application.dtos import (
    CriarInversorRequest,
    CriarPainelRequest,
    InversorResponse,
    PainelResponse,
    ValidarDimensionamentoRequest,
    ValidarDimensionamentoResponse,
)
from src.equipamentos.application.use_cases import (
    CriarInversorUseCase,
    CriarPainelUseCase,
    ListarInversoresUseCase,
    ListarPaineisUseCase,
    ValidarDimensionamentoUseCase,
)
from src.equipamentos.infrastructure.dependencies import (
    get_criar_inversor_use_case,
    get_criar_painel_use_case,
    get_listar_inversores_use_case,
    get_listar_paineis_use_case,
    get_validar_dimensionamento_use_case,
)
from src.tenant.domain.entities import Tenant

router = APIRouter(prefix="/api/v1", tags=["equipamentos"])


@router.post("/paineis", response_model=PainelResponse, status_code=status.HTTP_201_CREATED)
async def criar_painel(
    dto: CriarPainelRequest,
    tenant: Tenant = Depends(get_current_tenant),
    use_case: CriarPainelUseCase = Depends(get_criar_painel_use_case),
) -> PainelResponse:
    """Criar painel (admin)"""
    painel = await use_case.execute(dto, tenant.id)
    return PainelResponse.model_validate(painel)


@router.get("/paineis", response_model=list[PainelResponse])
async def listar_paineis(
    tenant: Tenant = Depends(get_current_tenant),
    use_case: ListarPaineisUseCase = Depends(get_listar_paineis_use_case),
) -> list[PainelResponse]:
    """Listar painéis ativos"""
    paineis = await use_case.execute(tenant.id)
    return [PainelResponse.model_validate(p) for p in paineis]


@router.post(
    "/inversores", response_model=InversorResponse, status_code=status.HTTP_201_CREATED
)
async def criar_inversor(
    dto: CriarInversorRequest,
    tenant: Tenant = Depends(get_current_tenant),
    use_case: CriarInversorUseCase = Depends(get_criar_inversor_use_case),
) -> InversorResponse:
    """Criar inversor (admin)"""
    inversor = await use_case.execute(dto, tenant.id)
    return InversorResponse.model_validate(inversor)


@router.get("/inversores", response_model=list[InversorResponse])
async def listar_inversores(
    tenant: Tenant = Depends(get_current_tenant),
    use_case: ListarInversoresUseCase = Depends(get_listar_inversores_use_case),
) -> list[InversorResponse]:
    """Listar inversores ativos"""
    inversores = await use_case.execute(tenant.id)
    return [InversorResponse.model_validate(i) for i in inversores]


@router.post("/equipamentos/validar-dimensionamento", response_model=ValidarDimensionamentoResponse)
async def validar_dimensionamento(
    dto: ValidarDimensionamentoRequest,
    tenant: Tenant = Depends(get_current_tenant),
    use_case: ValidarDimensionamentoUseCase = Depends(get_validar_dimensionamento_use_case),
) -> ValidarDimensionamentoResponse:
    """Validar dimensionamento painel vs inversor"""
    resultado = await use_case.execute(dto, tenant.id)
    return ValidarDimensionamentoResponse(**resultado)
