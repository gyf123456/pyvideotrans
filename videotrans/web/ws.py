"""WebSocket endpoint for real-time task log streaming."""

import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from videotrans.web import progress

router = APIRouter()


@router.websocket("/ws/{task_id}")
async def websocket_task(ws: WebSocket, task_id: str):
    await ws.accept()
    await progress.register(task_id, ws)
    try:
        # Keep the connection alive — wait for client close or disconnect
        while True:
            # We don't expect meaningful client messages; just await to detect close.
            await ws.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        await progress.unregister(task_id, ws)
