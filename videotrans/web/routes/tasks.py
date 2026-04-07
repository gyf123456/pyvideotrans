"""Task endpoints: POST /api/task, GET /api/task/{id}, GET /api/tasks."""

import time
import threading
from pathlib import Path

from fastapi import APIRouter, HTTPException

from videotrans.web.deps import (
    TASKS, TASKS_LOCK, build_common_params, drain_logs, run_task,
)
from videotrans.web.models import ApiResponse, TaskCreateRequest

router = APIRouter()


@router.post("/api/task", response_model=ApiResponse)
async def create_task(req: TaskCreateRequest):
    if req.task not in ('stt', 'tts', 'sts', 'vtv'):
        raise HTTPException(status_code=400, detail="Invalid 'task' value. Must be one of: stt, tts, sts, vtv")

    if not req.name or not Path(req.name).exists():
        raise HTTPException(status_code=400, detail=f"File not found: {req.name}")

    common_params = build_common_params(req.name)
    task_uuid = common_params['uuid']

    # Build task-specific params
    if req.task == 'stt':
        task_params = {
            "recogn_type": req.recogn_type,
            "detect_language": req.detect_language,
            "model_name": req.model_name,
            "is_cuda": req.is_cuda,
            "remove_noise": req.remove_noise,
            "enable_diariz": req.enable_diariz,
            "nums_diariz": req.nums_diariz,
            "rephrase": req.rephrase,
            "fix_punc": req.fix_punc,
        }

    elif req.task == 'tts':
        if not req.voice_role:
            raise HTTPException(status_code=400, detail="voice_role is required for tts task")
        task_params = {
            "tts_type": req.tts_type,
            "voice_role": req.voice_role,
            "voice_rate": req.voice_rate,
            "volume": req.volume,
            "pitch": req.pitch,
            "is_cuda": req.is_cuda,
            "voice_autorate": req.voice_autorate,
            "align_sub_audio": req.align_sub_audio,
            "target_language_code": req.target_language_code,
        }

    elif req.task == 'sts':
        if not req.target_language_code:
            raise HTTPException(status_code=400, detail="target_language_code is required for sts task")
        task_params = {
            "translate_type": req.translate_type,
            "source_language_code": req.source_language_code or "auto",
            "target_language_code": req.target_language_code,
        }

    elif req.task == 'vtv':
        if not req.source_language_code or not req.target_language_code:
            raise HTTPException(status_code=400, detail="source_language_code and target_language_code are required for vtv task")
        task_params = {
            "source_language_code": req.source_language_code,
            "target_language_code": req.target_language_code,
            "recogn_type": req.recogn_type,
            "model_name": req.model_name,
            "is_cuda": req.is_cuda,
            "remove_noise": req.remove_noise,
            "enable_diariz": req.enable_diariz,
            "nums_diariz": req.nums_diariz,
            "rephrase": req.rephrase,
            "fix_punc": req.fix_punc,
            "tts_type": req.tts_type,
            "voice_role": req.voice_role or "No",
            "voice_rate": req.voice_rate,
            "volume": req.volume,
            "pitch": req.pitch,
            "voice_autorate": req.voice_autorate,
            "video_autorate": req.video_autorate,
            "align_sub_audio": req.align_sub_audio,
            "translate_type": req.translate_type,
            "is_separate": req.is_separate,
            "recogn2pass": req.recogn2pass,
            "subtitle_type": req.subtitle_type,
            "clear_cache": req.clear_cache,
        }

    params = {**common_params, **task_params}

    with TASKS_LOCK:
        TASKS[task_uuid] = {
            'status': 'pending',
            'task_type': req.task,
            'file': req.name,
            'target_dir': common_params['target_dir'],
            'error': None,
            'logs': [],
            'created_at': time.time(),
        }

    t = threading.Thread(target=run_task, args=(task_uuid, req.task, params), daemon=True)
    t.start()

    return ApiResponse(data={"task_id": task_uuid, "target_dir": common_params['target_dir']})


@router.get("/api/task/{task_id}", response_model=ApiResponse)
async def get_task(task_id: str):
    with TASKS_LOCK:
        task = TASKS.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")

    new_logs = drain_logs(task_id)
    with TASKS_LOCK:
        task['logs'].extend(new_logs)
        snapshot = {
            'task_id': task_id,
            'status': task['status'],
            'task_type': task['task_type'],
            'file': task['file'],
            'target_dir': task['target_dir'],
            'error': task['error'],
            'logs': task['logs'],
        }

    return ApiResponse(data=snapshot)


@router.get("/api/tasks", response_model=ApiResponse)
async def list_tasks():
    with TASKS_LOCK:
        summaries = []
        for tid, t in TASKS.items():
            summaries.append({
                'task_id': tid,
                'status': t['status'],
                'task_type': t['task_type'],
                'file': t['file'],
                'target_dir': t['target_dir'],
                'error': t['error'],
                'created_at': t.get('created_at'),
            })
    return ApiResponse(data=summaries)
