from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from src.auth.domain.entities import User
from src.auth.infrastructure.dependencies import get_current_tenant, get_current_user
from src.orcamentos.application.dtos import (
    AtualizarOrcamentoRequest,
    CalcularMaterialEletricoRequest,
    CalcularMaterialEletricoResponse,
    CriarOrcamentoRequest,
    OrcamentoListResponse,
    OrcamentoResponse,
)
from src.orcamentos.application.use_cases import (
    AtualizarOrcamentoUseCase,
    CriarOrcamentoUseCase,
    DeletarOrcamentoUseCase,
    ListarOrcamentosUseCase,
    ObterOrcamentoUseCase,
)
from src.orcamentos.domain.services import SolarCalculatorService
from src.orcamentos.domain.value_objects import FaixaMaterialEletrico
from src.orcamentos.infrastructure.dependencies import (
    get_atualizar_orcamento_use_case,
    get_criar_orcamento_use_case,
    get_deletar_orcamento_use_case,
    get_listar_orcamentos_use_case,
    get_obter_orcamento_use_case,
)
from src.premissas.application.use_cases import ObterPremissaAtivaUseCase
from src.premissas.infrastructure.dependencies import get_obter_premissa_ativa_use_case
from src.shared.exceptions import ForbiddenError
from src.tenant.domain.entities import Tenant

router = APIRouter(prefix="/api/v1/orcamentos", tags=["orcamentos"])


@router.post("/", response_model=OrcamentoResponse, status_code=status.HTTP_201_CREATED)
async def criar_orcamento(
    dto: CriarOrcamentoRequest,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    use_case: CriarOrcamentoUseCase = Depends(get_criar_orcamento_use_case),
) -> OrcamentoResponse:
    orcamento = await use_case.execute(dto, tenant.id, user.role, user.id)
    return OrcamentoResponse.model_validate(orcamento)


@router.get("/", response_model=OrcamentoListResponse)
async def listar_orcamentos(
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    use_case: ListarOrcamentosUseCase = Depends(get_listar_orcamentos_use_case),
    cliente_id: UUID | None = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
) -> OrcamentoListResponse:
    items, total = await use_case.execute(
        tenant.id, user.role, user.id, cliente_id=cliente_id, offset=offset, limit=limit
    )
    return OrcamentoListResponse(
        items=[OrcamentoResponse.model_validate(o) for o in items],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.get("/{orcamento_id}", response_model=OrcamentoResponse)
async def obter_orcamento(
    orcamento_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    use_case: ObterOrcamentoUseCase = Depends(get_obter_orcamento_use_case),
) -> OrcamentoResponse:
    orcamento = await use_case.execute(orcamento_id, tenant.id, user.role, user.id)
    return OrcamentoResponse.model_validate(orcamento)


@router.put("/{orcamento_id}", response_model=OrcamentoResponse)
async def atualizar_orcamento(
    orcamento_id: UUID,
    dto: AtualizarOrcamentoRequest,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    use_case: AtualizarOrcamentoUseCase = Depends(get_atualizar_orcamento_use_case),
) -> OrcamentoResponse:
    orcamento = await use_case.execute(orcamento_id, dto, tenant.id, user.role, user.id)
    return OrcamentoResponse.model_validate(orcamento)


@router.delete("/{orcamento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_orcamento(
    orcamento_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    use_case: DeletarOrcamentoUseCase = Depends(get_deletar_orcamento_use_case),
) -> None:
    if user.role != "admin":
        raise ForbiddenError("Apenas admin pode deletar orcamentos")
    await use_case.execute(orcamento_id, tenant.id)


@router.post(
    "/calcular-material-eletrico", response_model=CalcularMaterialEletricoResponse
)
async def calcular_material_eletrico(
    dto: CalcularMaterialEletricoRequest,
    tenant: Tenant = Depends(get_current_tenant),
    premissa_use_case: ObterPremissaAtivaUseCase = Depends(get_obter_premissa_ativa_use_case),
) -> CalcularMaterialEletricoResponse:
    premissa = await premissa_use_case.execute(tenant.id)
    faixas = [
        FaixaMaterialEletrico(
            Decimal(str(f["potencia_min"])),
            Decimal(str(f["potencia_max"])),
            Decimal(str(f["valor"])),
        )
        for f in premissa.faixas_material_eletrico
    ]
    valor = SolarCalculatorService.calcular_material_eletrico(
        dto.potencia_inversor_kwp, faixas
    )
    return CalcularMaterialEletricoResponse(valor=valor)
