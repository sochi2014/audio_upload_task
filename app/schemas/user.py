from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: Optional[str] = None


class UserCreate(UserBase):
    yandex_id: str


class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: int
    yandex_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    pass
