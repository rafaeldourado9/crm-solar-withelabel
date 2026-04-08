from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.tenant.application.dtos import (
    AtualizarBrandingRequest,
    AtualizarTenantRequest,
    CriarTenantRequest,
    TenantResponse,
)
from src.tenant.application.use_cases import (
    AtualizarBrandingUseCase,
    AtualizarTenantUseCase,
    CriarTenantUseCase,
    ObterTenantUseCase,
)
from src.tenant.infrastructure.dependencies import (
    get_atualizar_branding_use_case,
    get_atualizar_tenant_use_case,
    get_criar_tenant_use_case,
    get_obter_tenant_use_case,
)

router = APIRouter(prefix="/api/v1/tenants", tags=["tenants"])


@router.post("/", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def criar_tenant(
    dto: CriarTenantRequest,
    use_case: CriarTenantUseCase = Depends(get_criar_tenant_use_case),
) -> TenantResponse:
    """Criar novo tenant (signup)"""
    tenant = await use_case.execute(dto)
    return TenantResponse.model_validate(tenant)


@router.get("/{tenant_id}", response_model=TenantResponse)
async def obter_tenant(
    tenant_id: UUID,
    use_case: ObterTenantUseCase = Depends(get_obter_tenant_use_case),
) -> TenantResponse:
    """Obter dados do tenant por ID"""
    tenant = await use_case.execute(tenant_id)
    return TenantResponse.model_validate(tenant)


@router.put("/{tenant_id}", response_model=TenantResponse)
async def atualizar_tenant(
    tenant_id: UUID,
    dto: AtualizarTenantRequest,
    use_case: AtualizarTenantUseCase = Depends(get_atualizar_tenant_use_case),
) -> TenantResponse:
    """Atualizar dados do tenant"""
    tenant = await use_case.execute(tenant_id, dto)
    return TenantResponse.model_validate(tenant)


@router.put("/{tenant_id}/branding", response_model=TenantResponse)
async def atualizar_branding(
    tenant_id: UUID,
    dto: AtualizarBrandingRequest,
    use_case: AtualizarBrandingUseCase = Depends(get_atualizar_branding_use_case),
) -> TenantResponse:
    """Atualizar branding (logo, cores, domínio)"""
    tenant = await use_case.execute(tenant_id, dto)
    return TenantResponse.model_validate(tenant)
