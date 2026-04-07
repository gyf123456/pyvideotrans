import client from './client'
import type { ApiResponse, TaskCreateRequest, TaskCreateResponse } from '@/types/api'
import type { TaskStatusResponse, TaskSummary } from '@/types/task'

export async function createTask(data: TaskCreateRequest) {
  const res = await client.post<ApiResponse<TaskCreateResponse>>('/api/task', data)
  return res.data.data
}

export async function getTask(taskId: string) {
  const res = await client.get<ApiResponse<TaskStatusResponse>>(`/api/task/${taskId}`)
  return res.data.data
}

export async function listTasks() {
  const res = await client.get<ApiResponse<TaskSummary[]>>('/api/tasks')
  return res.data.data
}
