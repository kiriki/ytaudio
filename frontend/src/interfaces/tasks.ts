export interface IClTask {
  action: string
  task_id: string
  task_status: string
  task_result: number
}

export interface IVideoTask {
  id: number
  url: string
  addedDate: string
  sourceId: string
  extractor: string
  title: string
  channel: string
  uploaderId: string
  duration: number
  uploadDate: string
  thumbnail: string
  info: object
  file: string
  fileSize: number
  user: number
}
