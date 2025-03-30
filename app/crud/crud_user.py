from typing import Optional, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser:
    def __init__(self, model: Type[User]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[User]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(self.model).where(self.model.email == email))
        return result.scalar_one_or_none()

    async def get_by_yandex_id(self, db: AsyncSession, yandex_id: str) -> Optional[User]:
        result = await db.execute(select(self.model).where(self.model.yandex_id == yandex_id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, obj_in: UserCreate) -> User:
        db_obj = self.model(
            yandex_id=obj_in.yandex_id,
            email=obj_in.email,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self, db: AsyncSession, db_obj: User, obj_in: UserUpdate
    ) -> User:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, db_obj: User) -> User:
        await db.delete(db_obj)
        await db.commit()
        return db_obj


user = CRUDUser(User)
