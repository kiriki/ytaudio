import { useNotifyStore } from '@/stores/notify'

const BASE_HTTP_PROTO = 'http'
const WS_PROTO = `ws${window.location.protocol.slice(BASE_HTTP_PROTO.length)}`
const WS_URL = `${WS_PROTO}${window.location.host}/ws/tasks/`

const onOpen = () => {
  console.debug('Notification connection success')
}

const onClose = (counter: number) => async (event) => {
  console.error('Notification connection close', event.data)
  const store = useNotifyStore()
  await store.notificationsConnect(counter + 1)
}

const onMessage = (event: object) => {
  const store = useNotifyStore()
  try {
    const payload = JSON.parse(event.data)
    store.receiveNotification(payload)
  } catch (e) {
    console.error('Error in receive ws message', e)
  }
}

const onError = (event: object) => {
  console.error('Notification connection error', event.data)
}

const connect = (counter: number) => {
  const socket = new WebSocket(WS_URL)
  socket.onclose = onClose(counter)
  socket.onopen = onOpen
  socket.onmessage = onMessage
  socket.onerror = onError
}

export default connect
