import httpx
from fastapi import HTTPException, status

from app.core.config import settings


class YandexOAuth:
    def __init__(self):
        self.client_id = settings.YANDEX_CLIENT_ID
        self.client_secret = settings.YANDEX_CLIENT_SECRET
        self.redirect_uri = settings.YANDEX_REDIRECT_URI
        self.token_url = settings.TOKEN_URL
        self.user_info_url = settings.USER_INFO_URL

    async def get_access_token(self, code: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uri": self.redirect_uri,
                }
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to get access token from Yandex"
                )
            return response.json()["access_token"]

    async def get_user_info(self, access_token: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.user_info_url,
                headers={"Authorization": f"OAuth {access_token}"}
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to get user info from Yandex"
                )
            return response.json()

    def get_authorization_url(self) -> str:
        return (
            f"https://oauth.yandex.ru/authorize"
            f"?response_type=code"
            f"&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
        )


yandex_oauth = YandexOAuth()
