from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.templates.application.use_cases import (
    DeletarTemplateUseCase,
    ListarTemplatesUseCase,
    ObterTemplateBytesUseCase,
    UploadTemplateUseCase,
)
from src.templates.infrastructure.repositories import SQLAlchemyTemplateRepository


def get_upload_template_use_case(db: AsyncSession = Depends(get_db)) -> UploadTemplateUseCase:
    return UploadTemplateUseCase(SQLAlchemyTemplateRepository(db))


def get_listar_templates_use_case(db: AsyncSession = Depends(get_db)) -> ListarTemplatesUseCase:
    return ListarTemplatesUseCase(SQLAlchemyTemplateRepository(db))


def get_obter_template_bytes_use_case(db: AsyncSession = Depends(get_db)) -> ObterTemplateBytesUseCase:
    return ObterTemplateBytesUseCase(SQLAlchemyTemplateRepository(db))


def get_deletar_template_use_case(db: AsyncSession = Depends(get_db)) -> DeletarTemplateUseCase:
    return DeletarTemplateUseCase(SQLAlchemyTemplateRepository(db))
