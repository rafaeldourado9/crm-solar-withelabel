from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.domain.entities import User
from src.auth.infrastructure.models import UserModel
from src.auth.domain.services import PasswordService


class SQLAlchemyUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        model = UserModel(**user.model_dump())
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return User.model_validate(model)

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalar_one_or_none()
        return User.model_validate(model) if model else None

    async def get_by_email(self, email: str, tenant_id: UUID) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(
                UserModel.email == email, UserModel.tenant_id == tenant_id
            )
        )
        model = result.scalar_one_or_none()
        return User.model_validate(model) if model else None

    async def update(self, user: User) -> User:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user.id))
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"User {user.id} não encontrado")

        for key, value in user.model_dump(exclude={"id", "created_at"}).items():
            setattr(model, key, value)

        await self.session.flush()
        await self.session.refresh(model)
        return User.model_validate(model)

    async def list_by_tenant(
        self,
        tenant_id: UUID,
        roles: list[str] | None = None,
    ) -> list[User]:
        query = select(UserModel).where(UserModel.tenant_id == tenant_id)
        if roles:
            query = query.where(UserModel.role.in_(roles))
        query = query.order_by(UserModel.nome)
        result = await self.session.execute(query)
        return [User.model_validate(m) for m in result.scalars().all()]

    async def delete(self, user_id: UUID) -> None:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.flush()

    async def reset_password(self, user_id: UUID, new_password: str) -> None:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalar_one_or_none()
        if model:
            model.hashed_password = PasswordService.hash_password(new_password)
            await self.session.flush()
