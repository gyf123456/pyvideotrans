"""GET /api/system/info, GET /api/system/health — system information."""

import platform
import sys

from fastapi import APIRouter

from videotrans.configure.config import app_cfg, ROOT_DIR
from videotrans.web.models import ApiResponse

router = APIRouter()


@router.get("/api/system/health", response_model=ApiResponse)
async def health_check():
    return ApiResponse(data={"status": "ok"})


@router.get("/api/system/info", response_model=ApiResponse)
async def system_info():
    gpu_count = app_cfg.NVIDIA_GPU_NUMS

    # Try to get torch/cuda info
    cuda_available = False
    torch_version = ""
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        torch_version = torch.__version__
    except ImportError:
        pass

    return ApiResponse(data={
        "platform": sys.platform,
        "python_version": platform.python_version(),
        "torch_version": torch_version,
        "cuda_available": cuda_available,
        "gpu_count": gpu_count,
        "root_dir": ROOT_DIR,
    })
