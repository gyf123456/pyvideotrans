export interface TaskStatusResponse {
  task_id: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  task_type: string
  file: string
  target_dir: string
  error: string | null
  logs: any[]
}

export interface TaskSummary {
  task_id: string
  status: string
  task_type: string
  file: string
  target_dir: string
  error: string | null
  created_at: number | null
}
