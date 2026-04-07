import { defineStore } from 'pinia'
import { ref } from 'vue'
import { listTasks, getTask } from '@/api/tasks'
import type { TaskSummary, TaskStatusResponse } from '@/types/task'

export const useTaskStore = defineStore('task', () => {
  const tasks = ref<TaskSummary[]>([])
  const activeTask = ref<TaskStatusResponse | null>(null)
  const activeLogs = ref<any[]>([])

  async function loadTasks() {
    tasks.value = await listTasks()
  }

  async function loadTask(taskId: string) {
    const data = await getTask(taskId)
    activeTask.value = data
    return data
  }

  function appendLog(log: any) {
    activeLogs.value.push(log)
  }

  function clearLogs() {
    activeLogs.value = []
  }

  function updateTaskStatus(taskId: string, status: string, error?: string) {
    const t = tasks.value.find(x => x.task_id === taskId)
    if (t) {
      t.status = status
      if (error) t.error = error
    }
    if (activeTask.value?.task_id === taskId) {
      activeTask.value.status = status as any
      if (error) activeTask.value.error = error
    }
  }

  return { tasks, activeTask, activeLogs, loadTasks, loadTask, appendLog, clearLogs, updateTaskStatus }
})
