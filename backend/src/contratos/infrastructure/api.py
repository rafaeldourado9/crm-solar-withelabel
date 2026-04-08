from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from src.auth.domain.entities import User
from src.auth.infrastructure.dependencies import get_current_tenant, get_current_user
from src.contratos.application.dtos import (
    AtualizarContratoRequest,
    ContratoListResponse,
    ContratoResponse,
    CriarContratoRequest,
)
from src.contratos.application.use_cases import (
    AtualizarContratoUseCase,
    CriarContratoUseCase,
    ListarContratosUseCase,
    ObterContratoUseCase,
)
from src.contratos.infrastructure.dependencies import (
    get_atualizar_contrato_use_case,
    get_criar_contrato_use_case,
    get_listar_contratos_use_case,
    get_obter_contrato_use_case,
)
from src.documentos.infrastructure.docx_adapter import gerar_docx
from src.documentos.infrastructure.pdf_adapter import gerar_pdf_contrato
from src.documentos.domain.services import numero_por_extenso
from src.tenant.domain.entities import Tenant

router = APIRouter(prefix="/api/v1/contratos", tags=["contratos"])


@router.post("", response_model=ContratoResponse, status_code=status.HTTP_201_CREATED)
async def criar_contrato(
    dto: CriarContratoRequest,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    use_case: CriarContratoUseCase = Depends(get_criar_contrato_use_case),
) -> ContratoResponse:
    return await use_case.execute(dto, tenant.id, user)


@router.get("", response_model=ContratoListResponse)
async def listar_contratos(
    cliente_id: UUID | None = None,
    status_filtro: str | None = None,
    offset: int = 0,
    limit: int = 20,
    tenant: Tenant = Depends(get_current_tenant),
    use_case: ListarContratosUseCase = Depends(get_listar_contratos_use_case),
) -> ContratoListResponse:
    return await use_case.execute(tenant.id, cliente_id, status_filtro, offset, limit)


@router.get("/{contrato_id}", response_model=ContratoResponse)
async def obter_contrato(
    contrato_id: UUID,
    tenant: Tenant = Depends(get_current_tenant),
    use_case: ObterContratoUseCase = Depends(get_obter_contrato_use_case),
) -> ContratoResponse:
    return await use_case.execute(contrato_id, tenant.id)


@router.put("/{contrato_id}", response_model=ContratoResponse)
async def atualizar_contrato(
    contrato_id: UUID,
    dto: AtualizarContratoRequest,
    tenant: Tenant = Depends(get_current_tenant),
    use_case: AtualizarContratoUseCase = Depends(get_atualizar_contrato_use_case),
) -> ContratoResponse:
    return await use_case.execute(contrato_id, tenant.id, dto)


@router.get("/{contrato_id}/gerar-pdf")
async def gerar_pdf(
    contrato_id: UUID,
    tenant: Tenant = Depends(get_current_tenant),
    use_case: ObterContratoUseCase = Depends(get_obter_contrato_use_case),
) -> Response:
    contrato = await use_case.execute(contrato_id, tenant.id)
    variaveis = {
        "cliente_nome": contrato.cliente_nome,
        "cliente_cpf_cnpj": contrato.cliente_cpf_cnpj,
        "cliente_endereco": contrato.cliente_endereco,
        "cliente_cidade": contrato.cliente_cidade,
        "cliente_estado": contrato.cliente_estado,
        "cliente_cep": contrato.cliente_cep,
        "empresa_razao_social": contrato.empresa_razao_social,
        "empresa_cnpj": contrato.empresa_cnpj,
        "empresa_endereco": contrato.empresa_endereco,
        "empresa_cidade": contrato.empresa_cidade,
        "empresa_cep": contrato.empresa_cep,
        "empresa_representante_nome": contrato.empresa_representante_nome,
        "empresa_representante_cpf": contrato.empresa_representante_cpf,
        "banco_nome": contrato.banco_nome,
        "banco_agencia": contrato.banco_agencia,
        "banco_conta": contrato.banco_conta,
        "banco_titular": contrato.banco_titular,
        "potencia_total": f"{contrato.potencia_total_kwp:.2f}",
        "quantidade_paineis": str(contrato.quantidade_paineis),
        "valor_total": f"{contrato.valor_total:,.2f}".replace(",", "."),
        "valor_total_extenso": numero_por_extenso(contrato.valor_total),
        "numero_parcelas": str(contrato.numero_parcelas),
        "valor_parcela": f"{contrato.valor_parcela:,.2f}".replace(",", "."),
        "valor_parcela_extenso": numero_por_extenso(contrato.valor_parcela),
        "prazo_execucao_dias": str(contrato.prazo_execucao_dias),
        "garantia_instalacao_meses": str(contrato.garantia_instalacao_meses),
        "foro_comarca": contrato.foro_comarca,
    }
    pdf_bytes = gerar_pdf_contrato(variaveis)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="contrato-{contrato.numero}.pdf"'},
    )
