import { DateTime } from 'luxon'

export function dateTimeShort (date: string) {
  if (date) return DateTime.fromISO(date).toLocaleString(DateTime.DATETIME_SHORT)
}

export function dateShort (date: string) {
  if (date) return DateTime.fromISO(date).toLocaleString(DateTime.DATE_SHORT)
}

export function dateISO (date: string) {
  if (date) return DateTime.fromISO(date).toFormat('yyyy-MM-dd')
}

export const formatTime = (seconds: number | null) => {
  if (typeof seconds !== 'number') return '00:00'
  const timeString = new Date(seconds * 1000).toISOString().slice(11, 19)
  return timeString.startsWith('00') ? timeString.slice(3) : timeString
}

export const formatBytes = (bytes: number, decimals = 2) => {
  if (bytes == 0) return '0 Bytes'
  const k = 1024
  const dm = decimals || 2
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`
}
