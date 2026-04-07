"""
HTTP API server for pyvideotrans translation tasks.

Usage:
    python api.py [--host 0.0.0.0] [--port 9011]

Endpoints:
    POST /api/upload          Upload a file (multipart/form-data)
    POST /api/task            Submit a translation task (JSON)
    GET  /api/task/<task_id>  Query task status and logs
    GET  /api/tasks           List all tasks
"""

import argparse
import re
import sys
import asyncio
import threading
import time
import traceback
from pathlib import Path
from queue import Empty

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from videotrans.util.req_fac import custom_session_factory
import huggingface_hub
huggingface_hub.configure_http_backend(backend_factory=custom_session_factory)

from videotrans.configure import config
config.init_run()
from videotrans.configure.config import ROOT_DIR, app_cfg, TEMP_DIR, logger

from videotrans import recognition, translator, tts
from videotrans.task._speech2text import SpeechToText
from videotrans.task._translate_srt import TranslateSrt
from videotrans.task.trans_create import TransCreate
from videotrans.task._dubbing import DubbingSrt
from videotrans.task.taskcfg import TaskCfgSTT, TaskCfgTTS, TaskCfgSTS, TaskCfgVTT
from videotrans.util import tools
from videotrans.util.gpus import getset_gpu

from flask import Flask, request, jsonify

# --- App Configuration ---
app_cfg.exit_soft = False
app_cfg.exec_mode = 'api'  # Not 'cli', so set_process pushes to uuid_logs_queue

app = Flask(__name__)

# --- In-memory task store ---
TASKS = {}
TASKS_LOCK = threading.Lock()

# Upload directory
UPLOAD_DIR = Path(ROOT_DIR) / "upload"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _build_common_params(file_path: str) -> dict:
    """Build common params from a file path, mirroring cli.py logic."""
    _file_obj = tools.format_video(Path(file_path).absolute().as_posix())
    _nospacebasename = re.sub(r'[\s\. #*?!:"]', '-', _file_obj["basename"])
    _cache_folder = f'{TEMP_DIR}/{_file_obj["uuid"]}'
    _target_dir = f'{ROOT_DIR}/output/{_nospacebasename}'
    common_params = {'name': file_path, "cache_folder": _cache_folder, "target_dir": _target_dir}
    common_params.update(_file_obj)
    Path(_cache_folder).mkdir(parents=True, exist_ok=True)
    Path(_target_dir).mkdir(parents=True, exist_ok=True)
    return common_params


def _drain_logs(uuid: str) -> list:
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


def _run_task(task_uuid: str, task_type: str, params: dict):
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


# ==================== API Endpoints ====================

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload a file via multipart/form-data. Returns the server-side file path."""
    if 'file' not in request.files:
        return jsonify({"code": 1, "msg": "No 'file' field in form data"}), 400
    f = request.files['file']
    if not f.filename:
        return jsonify({"code": 1, "msg": "Empty filename"}), 400

    save_path = UPLOAD_DIR / f.filename
    # Avoid overwriting: append timestamp if exists
    if save_path.exists():
        stem = save_path.stem
        suffix = save_path.suffix
        save_path = UPLOAD_DIR / f"{stem}_{int(time.time())}{suffix}"

    f.save(str(save_path))
    return jsonify({"code": 0, "msg": "ok", "data": {"filepath": str(save_path)}})


@app.route('/api/task', methods=['POST'])
def create_task():
    """Submit a new translation task. Expects JSON body."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"code": 1, "msg": "Invalid or missing JSON body"}), 400

    task_type = data.get('task')
    if task_type not in ('stt', 'tts', 'sts', 'vtv'):
        return jsonify({"code": 1, "msg": "Invalid 'task' value. Must be one of: stt, tts, sts, vtv"}), 400

    file_path = data.get('name')
    if not file_path or not Path(file_path).exists():
        return jsonify({"code": 1, "msg": f"File not found: {file_path}"}), 400

    # Build common params
    common_params = _build_common_params(file_path)
    task_uuid = common_params['uuid']

    # Build task-specific params
    if task_type == 'stt':
        task_params = {
            "recogn_type": data.get("recogn_type", 0),
            "detect_language": data.get("detect_language", "auto"),
            "model_name": data.get("model_name", "tiny"),
            "is_cuda": data.get("is_cuda", False),
            "remove_noise": data.get("remove_noise", False),
            "enable_diariz": data.get("enable_diariz", False),
            "nums_diariz": data.get("nums_diariz", -1),
            "rephrase": data.get("rephrase", 0),
            "fix_punc": data.get("fix_punc", False),
        }

    elif task_type == 'tts':
        voice_role = data.get("voice_role")
        if not voice_role:
            return jsonify({"code": 1, "msg": "voice_role is required for tts task"}), 400
        task_params = {
            "tts_type": data.get("tts_type", 0),
            "voice_role": voice_role,
            "voice_rate": data.get("voice_rate", "+0%"),
            "volume": data.get("volume", "+0%"),
            "pitch": data.get("pitch", "+0Hz"),
            "is_cuda": data.get("is_cuda", False),
            "voice_autorate": data.get("voice_autorate", False),
            "align_sub_audio": data.get("align_sub_audio", False),
            "target_language_code": data.get("target_language_code"),
        }

    elif task_type == 'sts':
        target_language_code = data.get("target_language_code")
        if not target_language_code:
            return jsonify({"code": 1, "msg": "target_language_code is required for sts task"}), 400
        task_params = {
            "translate_type": data.get("translate_type", 0),
            "source_language_code": data.get("source_language_code", "auto"),
            "target_language_code": target_language_code,
        }

    elif task_type == 'vtv':
        source_language_code = data.get("source_language_code")
        target_language_code = data.get("target_language_code")
        missing = []
        if not source_language_code:
            missing.append("source_language_code")
        if not target_language_code:
            missing.append("target_language_code")
        if missing:
            return jsonify({"code": 1, "msg": f"Missing required params for vtv: {', '.join(missing)}"}), 400

        task_params = {
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
            "recogn_type": data.get("recogn_type", 0),
            "model_name": data.get("model_name", "tiny"),
            "is_cuda": data.get("is_cuda", False),
            "remove_noise": data.get("remove_noise", False),
            "enable_diariz": data.get("enable_diariz", False),
            "nums_diariz": data.get("nums_diariz", -1),
            "rephrase": data.get("rephrase", 0),
            "fix_punc": data.get("fix_punc", False),
            "tts_type": data.get("tts_type", 0),
            "voice_role": data.get("voice_role", "No"),
            "voice_rate": data.get("voice_rate", "+0%"),
            "volume": data.get("volume", "+0%"),
            "pitch": data.get("pitch", "+0Hz"),
            "voice_autorate": data.get("voice_autorate", False),
            "video_autorate": data.get("video_autorate", False),
            "align_sub_audio": data.get("align_sub_audio", False),
            "translate_type": data.get("translate_type", 0),
            "is_separate": data.get("is_separate", False),
            "recogn2pass": data.get("recogn2pass", False),
            "subtitle_type": data.get("subtitle_type", 1),
            "clear_cache": data.get("clear_cache", True),
        }

    params = {**common_params, **task_params}

    # Register task
    with TASKS_LOCK:
        TASKS[task_uuid] = {
            'status': 'pending',
            'task_type': task_type,
            'file': file_path,
            'target_dir': common_params['target_dir'],
            'error': None,
            'logs': [],
            'created_at': time.time(),
        }

    # Launch background thread
    t = threading.Thread(target=_run_task, args=(task_uuid, task_type, params), daemon=True)
    t.start()

    return jsonify({
        "code": 0,
        "msg": "ok",
        "data": {
            "task_id": task_uuid,
            "target_dir": common_params['target_dir'],
        }
    })


@app.route('/api/task/<task_id>', methods=['GET'])
def get_task(task_id):
    """Query task status and drain accumulated logs."""
    with TASKS_LOCK:
        task = TASKS.get(task_id)
    if not task:
        return jsonify({"code": 1, "msg": f"Task not found: {task_id}"}), 404

    # Drain new log entries from the queue
    new_logs = _drain_logs(task_id)
    with TASKS_LOCK:
        task['logs'].extend(new_logs)
        # Return a snapshot
        snapshot = {
            'task_id': task_id,
            'status': task['status'],
            'task_type': task['task_type'],
            'file': task['file'],
            'target_dir': task['target_dir'],
            'error': task['error'],
            'logs': task['logs'],
        }

    return jsonify({"code": 0, "data": snapshot})


@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    """List all tasks (summary without full logs)."""
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
    return jsonify({"code": 0, "data": summaries})


def main():
    parser = argparse.ArgumentParser(description="pyvideotrans HTTP API Server")
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Listen host')
    parser.add_argument('--port', type=int, default=9011, help='Listen port')
    args = parser.parse_args()

    print('Checking GPUs...')
    getset_gpu()

    print(f'Starting API server on {args.host}:{args.port}')
    app.run(host=args.host, port=args.port, debug=False, threaded=True)


if __name__ == '__main__':
    from multiprocessing import freeze_support
    import multiprocessing
    freeze_support()
    try:
        multiprocessing.set_start_method('spawn', force=True)
    except RuntimeError:
        pass
    main()
