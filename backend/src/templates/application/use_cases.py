"""Use cases do módulo Templates."""
import os
from uuid import UUID

from src.shared.exceptions import NotFoundError, ValidationError
from src.templates.application.dtos import TemplateResponse
from src.templates.domain.entities import Template, TipoTemplate
from src.templates.domain.repositories import TemplateRepository
from src.documentos.infrastructure.docx_adapter import extrair_variaveis_docx


UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/tmp/templates")


class UploadTemplateUseCase:
    def __init__(self, repo: TemplateRepository):
        self.repo = repo

    async def execute(
        self, tenant_id: UUID, nome: str, tipo: str, conteudo: bytes, filename: str
    ) -> TemplateResponse:
        try:
            tipo_enum = TipoTemplate(tipo)
        except ValueError:
            raise ValidationError(f"Tipo inválido: {tipo}. Use: orcamento, proposta, contrato")

        variaveis = list(extrair_variaveis_docx(conteudo))

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        arquivo_path = os.path.join(UPLOAD_DIR, f"{tenant_id}_{tipo}_{filename}")
        with open(arquivo_path, "wb") as f:
            f.write(conteudo)

        # Desativar templates anteriores do mesmo tipo
        existente = await self.repo.get_ativo_by_tipo(tenant_id, tipo_enum)
        if existente:
            existente.ativo = False
            await self.repo.update(existente)

        template = Template(
            tenant_id=tenant_id,
            nome=nome,
            tipo=tipo_enum,
            arquivo_path=arquivo_path,
            tamanho_bytes=len(conteudo),
            variaveis_encontradas=variaveis,
            ativo=True,
        )
        criado = await self.repo.create(template)
        return TemplateResponse.model_validate(criado)


class ListarTemplatesUseCase:
    def __init__(self, repo: TemplateRepository):
        self.repo = repo

    async def execute(self, tenant_id: UUID) -> list[TemplateResponse]:
        templates = await self.repo.list_by_tenant(tenant_id)
        return [TemplateResponse.model_validate(t) for t in templates]


class ObterTemplateBytesUseCase:
    def __init__(self, repo: TemplateRepository):
        self.repo = repo

    async def execute(self, template_id: UUID, tenant_id: UUID) -> tuple[bytes, str]:
        template = await self.repo.get_by_id(template_id, tenant_id)
        if not template:
            raise NotFoundError("Template não encontrado")
        with open(template.arquivo_path, "rb") as f:
            return f.read(), template.nome


class DeletarTemplateUseCase:
    def __init__(self, repo: TemplateRepository):
        self.repo = repo

    async def execute(self, template_id: UUID, tenant_id: UUID) -> None:
        template = await self.repo.get_by_id(template_id, tenant_id)
        if not template:
            raise NotFoundError("Template não encontrado")
        if os.path.exists(template.arquivo_path):
            os.remove(template.arquivo_path)
        await self.repo.delete(template_id, tenant_id)
