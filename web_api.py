"""
Web API server for pyvideotrans (FastAPI + WebSocket).

Usage:
    python web_api.py [--host 0.0.0.0] [--port 9011]

Swagger docs:
    http://localhost:9011/docs
"""

import argparse
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from videotrans.util.req_fac import custom_session_factory
import huggingface_hub
huggingface_hub.configure_http_backend(backend_factory=custom_session_factory)

from videotrans.configure import config
config.init_run()
from videotrans.configure.config import app_cfg
from videotrans.util.gpus import getset_gpu

# Set exec_mode so push_queue routes logs to uuid_logs_queue (same as api.py)
app_cfg.exit_soft = False
app_cfg.exec_mode = 'api'

from videotrans.web.app import create_app

app = create_app()


def main():
    import uvicorn

    parser = argparse.ArgumentParser(description="pyVideoTrans Web API Server (FastAPI)")
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Listen host')
    parser.add_argument('--port', type=int, default=9011, help='Listen port')
    args = parser.parse_args()

    print('Checking GPUs...')
    getset_gpu()

    print(f'Starting Web API server on {args.host}:{args.port}')
    print(f'Swagger docs: http://{args.host}:{args.port}/docs')
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == '__main__':
    from multiprocessing import freeze_support
    import multiprocessing
    freeze_support()
    try:
        multiprocessing.set_start_method('spawn', force=True)
    except RuntimeError:
        pass
    main()
