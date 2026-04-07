import { ref, onUnmounted } from 'vue'
import { createTaskWebSocket } from '@/api/ws'
import { useTaskStore } from '@/stores/task'

export function useTaskWebSocket() {
  const ws = ref<WebSocket | null>(null)
  const connected = ref(false)
  const taskStore = useTaskStore()

  function connect(taskId: string) {
    disconnect()
    ws.value = createTaskWebSocket(
      taskId,
      (data) => {
        taskStore.appendLog(data)
        if (data.type === 'status') {
          taskStore.updateTaskStatus(taskId, data.status, data.error)
        }
      },
      () => {
        connected.value = false
      }
    )
    ws.value.onopen = () => {
      connected.value = true
    }
  }

  function disconnect() {
    if (ws.value) {
      ws.value.close()
      ws.value = null
      connected.value = false
    }
  }

  onUnmounted(() => {
    disconnect()
  })

  return { connected, connect, disconnect }
}
