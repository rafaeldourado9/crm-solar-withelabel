from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from fastapi.responses import FileResponse, Response

from src.auth.domain.entities import User
from src.auth.infrastructure.dependencies import get_current_tenant, get_current_user
from src.shared.exceptions import ValidationError
from src.templates.application.dtos import TemplateResponse
from src.templates.application.use_cases import (
    DeletarTemplateUseCase,
    ListarTemplatesUseCase,
    ObterTemplateBytesUseCase,
    UploadTemplateUseCase,
)
from src.templates.infrastructure.dependencies import (
    get_deletar_template_use_case,
    get_listar_templates_use_case,
    get_obter_template_bytes_use_case,
    get_upload_template_use_case,
)
from src.tenant.domain.entities import Tenant

router = APIRouter(prefix="/api/v1/templates", tags=["templates"])

_TIPOS_VALIDOS = {"orcamento", "proposta", "contrato"}
_MIME_DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


@router.post("", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
async def upload_template(
    arquivo: UploadFile = File(...),
    nome: str = Form(...),
    tipo: str = Form(...),
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    use_case: UploadTemplateUseCase = Depends(get_upload_template_use_case),
) -> TemplateResponse:
    if tipo not in _TIPOS_VALIDOS:
        raise ValidationError(f"Tipo inválido. Use: {', '.join(_TIPOS_VALIDOS)}")
    if not arquivo.filename or not arquivo.filename.endswith(".docx"):
        raise ValidationError("Apenas arquivos .docx são aceitos")
    conteudo = await arquivo.read()
    return await use_case.execute(tenant.id, nome, tipo, conteudo, arquivo.filename)


@router.get("", response_model=list[TemplateResponse])
async def listar_templates(
    tenant: Tenant = Depends(get_current_tenant),
    use_case: ListarTemplatesUseCase = Depends(get_listar_templates_use_case),
) -> list[TemplateResponse]:
    return await use_case.execute(tenant.id)


@router.get("/{template_id}/download")
async def download_template(
    template_id: UUID,
    tenant: Tenant = Depends(get_current_tenant),
    use_case: ObterTemplateBytesUseCase = Depends(get_obter_template_bytes_use_case),
) -> Response:
    conteudo, nome = await use_case.execute(template_id, tenant.id)
    return Response(
        content=conteudo,
        media_type=_MIME_DOCX,
        headers={"Content-Disposition": f'attachment; filename="{nome}.docx"'},
    )


@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_template(
    template_id: UUID,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    use_case: DeletarTemplateUseCase = Depends(get_deletar_template_use_case),
) -> None:
    await use_case.execute(template_id, tenant.id)
