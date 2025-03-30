from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.auth import router as auth_router
from app.api.routers.audio import router as audio_router
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

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(audio_router, prefix="/audio", tags=["audio"])
