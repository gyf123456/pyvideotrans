"""GET /api/languages — supported language list."""

from fastapi import APIRouter

from videotrans.web.models import ApiResponse

router = APIRouter()


@router.get("/api/languages", response_model=ApiResponse)
async def get_languages():
    from videotrans import translator
    # Return list of {code, name} from LANGNAME_DICT
    result = [{"code": code, "name": name} for code, name in translator.LANGNAME_DICT.items()]
    return ApiResponse(data=result)
