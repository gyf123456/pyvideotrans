export type Settings = Record<string, any>
export type Params = Record<string, any>

export interface FileItem {
  name: string
  path: string
  size: number
}

export interface SystemInfo {
  platform: string
  python_version: string
  torch_version: string
  cuda_available: boolean
  gpu_count: number
  root_dir: string
}
