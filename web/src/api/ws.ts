export function createTaskWebSocket(taskId: string, onMessage: (data: any) => void, onClose?: () => void) {
  const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:'
  const base = import.meta.env.VITE_API_BASE
  let wsUrl: string
  if (base) {
    const url = new URL(base)
    wsUrl = `${protocol}//${url.host}/ws/${taskId}`
  } else {
    wsUrl = `${protocol}//${location.host}/ws/${taskId}`
  }

  const ws = new WebSocket(wsUrl)

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      onMessage(data)
    } catch {
      onMessage({ text: event.data })
    }
  }

  ws.onclose = () => {
    onClose?.()
  }

  ws.onerror = () => {
    onClose?.()
  }

  return ws
}
