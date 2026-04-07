"""WebSocket broadcast bridge.

Registers a callback into config.push_queue so that every log message
is also forwarded to connected WebSocket clients.
"""

import asyncio
import logging
from typing import Dict, Set

from fastapi import WebSocket

logger = logging.getLogger("VideoTrans")

# {uuid: set[WebSocket]} — active connections per task
_connections: Dict[str, Set[WebSocket]] = {}
_lock = asyncio.Lock()
_loop: asyncio.AbstractEventLoop | None = None


def init_bridge(loop: asyncio.AbstractEventLoop):
    """Called once at FastAPI lifespan startup to register the broadcast hook."""
    global _loop
    _loop = loop

    from videotrans.configure import config
    config._ws_broadcast_fn = _on_push_queue


async def register(uuid: str, ws: WebSocket):
    async with _lock:
        _connections.setdefault(uuid, set()).add(ws)


async def unregister(uuid: str, ws: WebSocket):
    async with _lock:
        s = _connections.get(uuid)
        if s:
            s.discard(ws)
            if not s:
                del _connections[uuid]


def _on_push_queue(uuid: str, jsondata):
    """Callback invoked from config.push_queue (runs in a worker thread).

    Schedules an async broadcast into the event loop.
    """
    if _loop is None or _loop.is_closed():
        return
    try:
        _loop.call_soon_threadsafe(asyncio.ensure_future, _broadcast(uuid, jsondata))
    except RuntimeError:
        pass


async def _broadcast(uuid: str, jsondata):
    """Send a message to all WebSocket clients watching this uuid."""
    async with _lock:
        clients = list(_connections.get(uuid, set()))
    dead = []
    for ws in clients:
        try:
            await ws.send_json(jsondata)
        except Exception:
            dead.append(ws)
    if dead:
        async with _lock:
            s = _connections.get(uuid)
            if s:
                for ws in dead:
                    s.discard(ws)
                if not s:
                    del _connections[uuid]
