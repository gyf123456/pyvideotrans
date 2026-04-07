"""GET/PUT /api/config/settings and /api/config/params — configuration management."""

from fastapi import APIRouter

from videotrans.configure.config import settings, params
from videotrans.web.models import ApiResponse, ConfigUpdateRequest

router = APIRouter()


# --- Settings (cfg.json) ---

@router.get("/api/config/settings", response_model=ApiResponse)
async def get_settings():
    return ApiResponse(data=settings.to_dict())


@router.put("/api/config/settings", response_model=ApiResponse)
async def update_settings(req: ConfigUpdateRequest):
    settings.parse_init(update_data=req.data)
    return ApiResponse(data=settings.to_dict())


# --- Params (params.json) ---

@router.get("/api/config/params", response_model=ApiResponse)
async def get_params():
    return ApiResponse(data=params.to_dict())


@router.put("/api/config/params", response_model=ApiResponse)
async def update_params(req: ConfigUpdateRequest):
    params.getset_params(update_data=req.data)
    return ApiResponse(data=params.to_dict())
