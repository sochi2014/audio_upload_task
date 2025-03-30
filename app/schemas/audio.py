from datetime import datetime
from pydantic import BaseModel


class AudioFileBase(BaseModel):
    filename: str
    storage_path: str


class AudioFileCreate(AudioFileBase):
    user_id: int


class AudioFilePublic(AudioFileBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
