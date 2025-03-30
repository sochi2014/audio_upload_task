from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import auth, audio, admin
from app.core.config import settings
from app.core.s3 import s3_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    bucket_exists = await s3_client.ensure_bucket_exists()
    if not bucket_exists:
        print("Warning: Failed to ensure bucket exists!")
    yield


app = FastAPI(title="Audio Upload Service", lifespan=lifespan)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(audio.router, prefix="/audio", tags=["audio"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
