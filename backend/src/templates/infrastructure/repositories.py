from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.templates.domain.entities import Template, TipoTemplate
from src.templates.infrastructure.models import TemplateModel


class SQLAlchemyTemplateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, template: Template) -> Template:
        model = TemplateModel(**template.model_dump())
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return Template.model_validate(model)

    async def get_by_id(self, id: UUID, tenant_id: UUID) -> Template | None:
        result = await self.session.execute(
            select(TemplateModel).where(
                TemplateModel.id == id, TemplateModel.tenant_id == tenant_id
            )
        )
        model = result.scalar_one_or_none()
        return Template.model_validate(model) if model else None

    async def get_ativo_by_tipo(self, tenant_id: UUID, tipo: TipoTemplate) -> Template | None:
        result = await self.session.execute(
            select(TemplateModel).where(
                TemplateModel.tenant_id == tenant_id,
                TemplateModel.tipo == tipo.value,
                TemplateModel.ativo.is_(True),
            ).order_by(TemplateModel.created_at.desc())
        )
        model = result.scalars().first()
        return Template.model_validate(model) if model else None

    async def list_by_tenant(self, tenant_id: UUID) -> list[Template]:
        result = await self.session.execute(
            select(TemplateModel)
            .where(TemplateModel.tenant_id == tenant_id)
            .order_by(TemplateModel.created_at.desc())
        )
        return [Template.model_validate(m) for m in result.scalars().all()]

    async def update(self, template: Template) -> Template:
        result = await self.session.execute(
            select(TemplateModel).where(TemplateModel.id == template.id)
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Template {template.id} não encontrado")
        for key, value in template.model_dump(exclude={"id", "created_at"}).items():
            setattr(model, key, value)
        await self.session.flush()
        await self.session.refresh(model)
        return Template.model_validate(model)

    async def delete(self, id: UUID, tenant_id: UUID) -> None:
        result = await self.session.execute(
            select(TemplateModel).where(
                TemplateModel.id == id, TemplateModel.tenant_id == tenant_id
            )
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.flush()
