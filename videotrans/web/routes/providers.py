"""GET /api/providers/{type} — list service providers for recognition/translation/tts."""

from fastapi import APIRouter, HTTPException

from videotrans.web.models import ApiResponse

router = APIRouter()


def _get_provider_list(provider_type: str) -> list:
    if provider_type == "recognition":
        from videotrans import recognition
        return [{"id": k, "name": v} for k, v in recognition._ID_NAME_DICT.items()]
    elif provider_type == "translation":
        from videotrans import translator
        return [{"id": k, "name": v} for k, v in translator._ID_NAME_DICT.items()]
    elif provider_type == "tts":
        from videotrans import tts
        return [{"id": k, "name": v} for k, v in tts._ID_NAME_DICT.items()]
    else:
        return None


@router.get("/api/providers/{provider_type}", response_model=ApiResponse)
async def get_providers(provider_type: str):
    result = _get_provider_list(provider_type)
    if result is None:
        raise HTTPException(status_code=400, detail=f"Invalid provider type: {provider_type}. Must be one of: recognition, translation, tts")
    return ApiResponse(data=result)
