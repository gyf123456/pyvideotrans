"""Shared state and utilities for the Web API."""

import re
import time
import threading
import traceback
from pathlib import Path
from queue import Empty

from videotrans.configure.config import ROOT_DIR, TEMP_DIR, app_cfg, logger
from videotrans.util import tools
from videotrans.task._speech2text import SpeechToText
from videotrans.task._translate_srt import TranslateSrt
from videotrans.task.trans_create import TransCreate
from videotrans.task._dubbing import DubbingSrt
from videotrans.task.taskcfg import TaskCfgSTT, TaskCfgTTS, TaskCfgSTS, TaskCfgVTT

# --- In-memory task store (same pattern as api.py) ---
TASKS: dict = {}
TASKS_LOCK = threading.Lock()

# Upload directory
UPLOAD_DIR = Path(ROOT_DIR) / "upload"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def build_common_params(file_path: str) -> dict:
    """Build common params from a file path, mirroring api.py logic."""
    _file_obj = tools.format_video(Path(file_path).absolute().as_posix())
    _nospacebasename = re.sub(r'[\s\. #*?!:"]', '-', _file_obj["basename"])
    _cache_folder = f'{TEMP_DIR}/{_file_obj["uuid"]}'
    _target_dir = f'{ROOT_DIR}/output/{_nospacebasename}'
    common_params = {'name': file_path, "cache_folder": _cache_folder, "target_dir": _target_dir}
    common_params.update(_file_obj)
    Path(_cache_folder).mkdir(parents=True, exist_ok=True)
    Path(_target_dir).mkdir(parents=True, exist_ok=True)
    return common_params


def drain_logs(uuid: str) -> list:
    """Drain all pending log entries from uuid_logs_queue for given uuid."""
    logs = []
    q = app_cfg.uuid_logs_queue.get(uuid)
    if q is None:
        return logs
    while True:
        try:
            entry = q.get_nowait()
            logs.append(entry)
        except Empty:
            break
    return logs


def run_task(task_uuid: str, task_type: str, params: dict):
    """Execute a task in a background thread, updating TASKS dict."""
    try:
        with TASKS_LOCK:
            TASKS[task_uuid]['status'] = 'running'

        if task_type == 'stt':
            trk = SpeechToText(cfg=TaskCfgSTT(**params), out_format='srt')
            trk.prepare()
            trk.recogn()
            trk.diariz()
            trk.task_done()

        elif task_type == 'tts':
            trk = DubbingSrt(cfg=TaskCfgTTS(**params), out_ext='wav')
            trk.dubbing()
            trk.align()
            trk.task_done()

        elif task_type == 'sts':
            trk = TranslateSrt(cfg=TaskCfgSTS(**params), out_format=0)
            trk.trans()
            trk.task_done()

        elif task_type == 'vtv':
            app_cfg.current_status = 'ing'
            trk = TransCreate(cfg=TaskCfgVTT(**params))
            trk.prepare()
            trk.recogn()
            trk.trans()
            trk.dubbing()
            trk.align()
            trk.assembling()
            trk.task_done()

        with TASKS_LOCK:
            TASKS[task_uuid]['status'] = 'done'

    except Exception as e:
        logger.exception(f'Task {task_uuid} failed: {e}')
        with TASKS_LOCK:
            TASKS[task_uuid]['status'] = 'error'
            TASKS[task_uuid]['error'] = f'{e}\n{traceback.format_exc()}'
