"""Pydantic request/response models for the Web API."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


# --- Generic response wrapper ---

class ApiResponse(BaseModel):
    code: int = 0
    msg: str = "ok"
    data: Any = None


# --- Upload ---

class UploadResponse(BaseModel):
    filepath: str


# --- Task creation ---

class TaskCreateRequest(BaseModel):
    task: str  # stt / tts / sts / vtv
    name: str  # server-side file path (from /api/upload)

    # STT params
    recogn_type: int = 0
    detect_language: str = "auto"
    model_name: str = "tiny"
    is_cuda: bool = False
    remove_noise: bool = False
    enable_diariz: bool = False
    nums_diariz: int = -1
    rephrase: int = 0
    fix_punc: bool = False

    # TTS params
    tts_type: int = 0
    voice_role: Optional[str] = None
    voice_rate: str = "+0%"
    volume: str = "+0%"
    pitch: str = "+0Hz"
    voice_autorate: bool = False
    video_autorate: bool = False
    align_sub_audio: bool = False
    target_language_code: Optional[str] = None

    # STS params
    translate_type: int = 0
    source_language_code: Optional[str] = None

    # VTV params
    is_separate: bool = False
    recogn2pass: bool = False
    subtitle_type: int = 1
    clear_cache: bool = True


class TaskCreateResponse(BaseModel):
    task_id: str
    target_dir: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    task_type: str
    file: str
    target_dir: str
    error: Optional[str] = None
    logs: List[Any] = []


class TaskSummary(BaseModel):
    task_id: str
    status: str
    task_type: str
    file: str
    target_dir: str
    error: Optional[str] = None
    created_at: Optional[float] = None


# --- Config ---

class ConfigUpdateRequest(BaseModel):
    """Partial update — only provided keys are applied."""
    data: Dict[str, Any]


# --- Provider ---

class ProviderItem(BaseModel):
    id: int
    name: str


# --- Voice ---

class VoiceItem(BaseModel):
    name: str
