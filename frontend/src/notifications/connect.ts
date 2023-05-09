import { useNotifyStore } from '@/stores/notify'

const BASE_HTTP_PROTO = 'http'
const WS_PROTO = `ws${window.location.protocol.slice(BASE_HTTP_PROTO.length)}`
const WS_URL = `${WS_PROTO}${window.location.host}/ws/tasks/`

const onOpen = () => {
  console.debug('Notification connection success')
  const store = useNotifyStore()
  store.resetCounter()
}

const onClose = async (event: CloseEvent) => {
  console.error('Notification connection close', event)
  const store = useNotifyStore()
  await store.notificationsConnect()
}

const onMessage = (event: MessageEvent) => {
  const store = useNotifyStore()
  try {
    const payload = JSON.parse(event.data)
    store.receiveNotification(payload)
  } catch (e) {
    console.error('Error in receive ws message', e)
  }
}

const onError = (event: Event) => {
  console.error('Notification connection error', event)
}

const connect = () => {
  const socket = new WebSocket(WS_URL)
  socket.onclose = onClose
  socket.onopen = onOpen
  socket.onmessage = onMessage
  socket.onerror = onError
}

export default connect
