from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    yandex_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    yandex_id: str
    first_name: str
    last_name: str = ""


class UserUpdate(UserBase):
    pass


class UserPublic(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


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
