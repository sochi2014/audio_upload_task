import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.auth.jwt import create_access_token, create_refresh_token
from app.auth.yandex import yandex_oauth
from app.core.config import settings
from app.crud.crud_user import user
from app.schemas.token import Token
from app.schemas.user import UserCreate

router = APIRouter()


@router.get("/yandex/login")
async def yandex_login():
    """
    Перенаправляет пользователя на страницу авторизации Яндекс
    """
    return {"url": yandex_oauth.get_authorization_url()}


@router.get("/yandex/callback")
async def yandex_callback(
        code: str,
        db: AsyncSession = Depends(get_db)
) -> Token:
    """
    Обрабатывает callback от Яндекс OAuth
    """
    # Получаем токен доступа от Яндекс
    access_token = await yandex_oauth.get_access_token(code)

    # Получаем информацию о пользователе
    user_info = await yandex_oauth.get_user_info(access_token)

    # Проверяем, существует ли пользователь
    db_user = await user.get_by_yandex_id(db, user_info["id"])

    if not db_user:
        full_name = user_info.get("real_name", "")
        last_name = full_name.split()[-1] if full_name and len(full_name.split()) > 1 else ""
        
        user_in = UserCreate(
            yandex_id=user_info["id"],
            email=user_info["default_email"],
            first_name=user_info["real_name"],
            last_name=last_name
        )
        db_user = await user.create(db, obj_in=user_in)

    # Создаем JWT токены
    return Token(
        access_token=create_access_token(subject=db_user.id),
        refresh_token=create_refresh_token(subject=db_user.id)
    )


@router.post("/token/refresh")
async def refresh_token(
        refresh_token: str,
        db: AsyncSession = Depends(get_db)
) -> Token:
    """
    Обновляет access token используя refresh token
    """
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    db_user = await user.get(db, id=int(user_id))
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return Token(
        access_token=create_access_token(subject=db_user.id),
        refresh_token=create_refresh_token(subject=db_user.id)
    )
