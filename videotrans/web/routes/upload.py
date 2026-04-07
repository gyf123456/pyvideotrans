"""POST /api/upload — file upload endpoint."""

import time
from fastapi import APIRouter, UploadFile, File, HTTPException

from videotrans.web.deps import UPLOAD_DIR
from videotrans.web.models import ApiResponse

router = APIRouter()


@router.post("/api/upload", response_model=ApiResponse)
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Empty filename")

    save_path = UPLOAD_DIR / file.filename
    if save_path.exists():
        stem = save_path.stem
        suffix = save_path.suffix
        save_path = UPLOAD_DIR / f"{stem}_{int(time.time())}{suffix}"

    content = await file.read()
    save_path.write_bytes(content)

    return ApiResponse(data={"filepath": str(save_path)})
