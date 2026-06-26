from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from app.core.config import get_settings


async def store_resume(file: UploadFile) -> tuple[str, str]:
    settings = get_settings()
    if file.content_type not in settings.allowed_resume_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume must be a PDF, DOC, or DOCX file.",
        )

    safe_name = Path(file.filename or "resume").name
    extension = Path(safe_name).suffix
    storage_name = f"{uuid4()}{extension}"
    storage_path = settings.upload_dir / storage_name

    size = 0
    with storage_path.open("wb") as target:
        chunk = await file.read(1024 * 1024)
        while chunk:
            size += len(chunk)
            if size > settings.max_resume_bytes:
                target.close()
                storage_path.unlink(missing_ok=True)
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="Resume is larger than the configured upload limit.",
                )
            target.write(chunk)
            chunk = await file.read(1024 * 1024)

    return safe_name, str(storage_path)
