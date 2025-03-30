from typing import List, Optional, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import AudioFile
from app.schemas.audio import AudioFileCreate


class CRUDAudio:
    def __init__(self, model: Type[AudioFile]):
        self.model = model

    async def create_audio_file(
        self, db: AsyncSession, *, user_id: int, filename: str, storage_path: str
    ) -> AudioFile:
        db_obj = self.model(
            user_id=user_id,
            filename=filename,
            original_filename=filename,
            storage_path=storage_path
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_user_audio_files(
        self, db: AsyncSession, *, user_id: int
    ) -> List[AudioFile]:
        result = await db.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        return list(result.scalars().all())

    async def get_audio_file(
        self, db: AsyncSession, *, id: int, user_id: int
    ) -> Optional[AudioFile]:
        result = await db.execute(
            select(self.model).where(
                self.model.id == id,
                self.model.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def delete_audio_file(
        self, db: AsyncSession, *, id: int, user_id: int
    ) -> Optional[AudioFile]:
        audio_file = await self.get_audio_file(db, id=id, user_id=user_id)
        if audio_file:
            await db.delete(audio_file)
            await db.commit()
        return audio_file


audio = CRUDAudio(AudioFile)
