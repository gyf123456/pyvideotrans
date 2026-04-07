"""GET /api/voices, POST /api/tts/preview — voice roles and TTS preview."""

import tempfile
import time
import threading
from pathlib import Path

from fastapi import APIRouter, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel

from videotrans.web.models import ApiResponse
from videotrans import tts
from videotrans.util import help_role
from videotrans.util.contants import LISTEN_TEXT

router = APIRouter()

# Mapping from tts_type id to role-loading function.
# Functions that need no args or just return a list.
_ROLE_LOADERS = {
    tts.EDGE_TTS: lambda lang: help_role.get_edge_rolelist(),
    tts.AZURE_TTS: lambda lang: help_role.get_azure_rolelist(),
    tts.ELEVENLABS_TTS: lambda lang: help_role.get_elevenlabs_role(),
    tts.PIPER_TTS: lambda lang: help_role.get_piper_role(),
    tts.QWEN3LOCAL_TTS: lambda lang: help_role.get_qwen3tts_rolelist(),
    tts.DOUBAO_TTS: lambda lang: help_role.get_doubao_rolelist(),
    tts.DOUBAO2_TTS: lambda lang: help_role.get_doubao2_rolelist(),
    tts.MINIMAXI_TTS: lambda lang: help_role.get_minimaxi_rolelist(),
    tts.KOKORO_TTS: lambda lang: help_role.get_kokoro_rolelist(),
    tts.GPTSOVITS_TTS: lambda lang: help_role.get_gptsovits_role(),
    tts.COSYVOICE_TTS: lambda lang: help_role.get_cosyvoice_role(),
    tts.FISHTTS: lambda lang: help_role.get_fishtts_role(),
    tts.F5_TTS: lambda lang: help_role.get_f5tts_role(),
    tts.VITSCNEN_TTS: lambda lang: help_role.get_vits_role(),
    tts.Supertonic_TTS: lambda lang: help_role.get_supertonic_rolelist(),
    tts.GLM_TTS: lambda lang: help_role.get_glmtts_rolelist(),
    tts.CHATTERBOX_TTS: lambda lang: help_role.get_chatterbox_role(),
}


@router.get("/api/voices", response_model=ApiResponse)
async def get_voices(
    tts_type: int = Query(..., description="TTS provider ID"),
    language: str = Query("", description="Language code (for providers that filter by language)"),
):
    loader = _ROLE_LOADERS.get(tts_type)
    if loader is None:
        # For providers without a dedicated loader, return a generic list or empty
        return ApiResponse(data=[])

    try:
        roles = loader(language)
    except Exception as e:
        return ApiResponse(code=1, msg=f"Failed to load voices: {e}", data=[])

    # Normalize: roles may be a list of strings, a dict keyed by language, or None
    if roles is None:
        return ApiResponse(data=[])

    if isinstance(roles, dict):
        # Roles dict can be:
        # 1. {lang: {display_name: tech_name, ...}}  e.g. edge-tts, azure-tts
        # 2. {lang: [name, ...]}  e.g. kokoro
        # 3. {name: value, ...}  flat dict e.g. gptsovits
        result = []
        for lang_key, val in roles.items():
            if isinstance(val, dict):
                for display_name, tech_name in val.items():
                    # Use tech_name as the value sent back to backend,
                    # display_name as label shown to user
                    result.append({
                        "name": str(tech_name) if tech_name and tech_name != display_name else display_name,
                        "label": display_name,
                        "language": lang_key,
                    })
            elif isinstance(val, list):
                for name in val:
                    result.append({"name": name, "language": lang_key})
            else:
                result.append({"name": lang_key})
        return ApiResponse(data=result)

    # List of strings
    if isinstance(roles, list):
        if roles and isinstance(roles[0], str):
            return ApiResponse(data=[{"name": r} for r in roles])
        return ApiResponse(data=roles)

    return ApiResponse(data=[])


# --- TTS Preview ---

class TtsPreviewRequest(BaseModel):
    tts_type: int
    voice_role: str
    language: str = "zh-cn"
    voice_rate: str = "+0%"
    volume: str = "+0%"
    pitch: str = "+0Hz"
    text: str = ""


@router.post("/api/tts/preview")
async def tts_preview(req: TtsPreviewRequest):
    if not req.voice_role or req.voice_role == "No":
        return ApiResponse(code=1, msg="请先选择配音角色")

    if req.voice_role == "clone":
        return ApiResponse(code=1, msg="克隆音色无法试听")

    # Determine preview text
    text = req.text.strip() if req.text.strip() else None
    if not text:
        lang_key = req.language.split("-")[0] if req.language else "zh"
        text = LISTEN_TEXT.get(req.language) or LISTEN_TEXT.get(lang_key) or LISTEN_TEXT.get("en")
    if not text:
        return ApiResponse(code=1, msg="该语言暂不支持试听")

    # Generate temp audio file
    voice_dir = Path(tempfile.gettempdir()) / "pyvideotrans"
    voice_dir.mkdir(parents=True, exist_ok=True)
    voice_file = str(voice_dir / f"{time.time()}.wav")

    queue_tts = [{
        "text": text,
        "role": str(req.voice_role),
        "rate": req.voice_rate,
        "volume": req.volume,
        "pitch": req.pitch,
        "filename": voice_file,
        "tts_type": req.tts_type,
        "language": req.language,
    }]

    # Run TTS synchronously in a thread
    error_msg = None

    def do_tts():
        nonlocal error_msg
        try:
            tts.run(
                queue_tts=queue_tts,
                language=req.language,
                play=False,
                is_test=True,
                tts_type=req.tts_type,
            )
        except Exception as e:
            error_msg = str(e)

    t = threading.Thread(target=do_tts)
    t.start()
    t.join(timeout=60)

    if error_msg:
        return ApiResponse(code=1, msg=f"试听失败: {error_msg}")

    if not Path(voice_file).exists():
        return ApiResponse(code=1, msg="试听生成失败，未生成音频文件")

    return FileResponse(
        path=voice_file,
        media_type="audio/wav",
        filename="preview.wav",
    )
