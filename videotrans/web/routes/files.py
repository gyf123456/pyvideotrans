"""GET /api/files, GET /api/files/download — output file management."""

import os
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

from videotrans.configure.config import ROOT_DIR
from videotrans.web.deps import TASKS, TASKS_LOCK
from videotrans.web.models import ApiResponse

router = APIRouter()

# All output files live under ROOT_DIR/output
OUTPUT_DIR = Path(ROOT_DIR) / "output"


@router.get("/api/files", response_model=ApiResponse)
async def list_files(task_id: str = Query("", description="Optional task_id to filter files")):
    if task_id:
        with TASKS_LOCK:
            task = TASKS.get(task_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")
        target_dir = Path(task['target_dir'])
    else:
        target_dir = OUTPUT_DIR

    if not target_dir.is_dir():
        return ApiResponse(data=[])

    files = []
    for f in sorted(target_dir.iterdir()):
        if f.is_file():
            files.append({
                "name": f.name,
                "path": str(f),
                "size": f.stat().st_size,
            })
    return ApiResponse(data=files)


@router.get("/api/files/download")
async def download_file(path: str = Query(..., description="Absolute file path to download")):
    file_path = Path(path).resolve()

    # Path traversal protection: must be under ROOT_DIR/output or ROOT_DIR/upload
    allowed_roots = [
        Path(ROOT_DIR, "output").resolve(),
        Path(ROOT_DIR, "upload").resolve(),
    ]
    if not any(str(file_path).startswith(str(root)) for root in allowed_roots):
        raise HTTPException(status_code=403, detail="Access denied: path outside allowed directories")

    if not file_path.is_file():
        raise HTTPException(status_code=404, detail=f"File not found: {path}")

    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type="application/octet-stream",
    )
