from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_s3_client, get_db
from app.core.config import settings
from app.crud import crud_audio
from app.db.models import User
from app.schemas.audio import AudioFilePublic

router = APIRouter()


@router.post("/upload", response_model=AudioFilePublic)
async def upload_audio(
    file: UploadFile = File(...),
    filename: str = Form(None),
    current_user: User = Depends(get_current_user),
    s3_client = Depends(get_s3_client),
    db: AsyncSession = Depends(get_db)
):
    if not file.content_type.startswith('audio/'):
        raise HTTPException(
            status_code=400,
            detail="File must be an audio file"
        )

    file_extension = Path(file.filename).suffix
    s3_object_key = f"user_{current_user.id}/{uuid4().hex}{file_extension}"

    await s3_client.upload_fileobj(
        file.file,
        settings.MINIO_BUCKET_NAME,
        s3_object_key
    )

    audio_file = await crud_audio.audio.create_audio_file(
        db,
        user_id=current_user.id,
        filename=filename or file.filename,
        storage_path=s3_object_key
    )

    return audio_file


@router.get("/", response_model=list[AudioFilePublic])
async def get_audio_files(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    audio_files = await crud_audio.audio.get_user_audio_files(db, user_id=current_user.id)
    return audio_files
