import { defineStore } from 'pinia'
import connect from '@/notifications/connect'
import { sleep } from '@/utils/tools'

const RECONNECT_DELAY = 3000
const MAX_RECONNECT_COUNT = 11

export const useNotifyStore = defineStore({
  id: 'notify',
  state: () => ({
    counter: 0,
    message: null
  }),
  getters: {
    doubleCount: (state) => state.counter * 2
  },
  actions: {
    increment () {
      this.counter++
    },

    resetCounter () {
      this.counter = 0
    },

    receiveNotification (payload) {
      console.log('receiveNotification')
      console.log(payload)
      this.message = payload
    },

    async notificationsConnect () {
      console.log(`ws reconnect... attempt ${this.counter}`)
      this.increment()
      if (this.counter > 1) await sleep(RECONNECT_DELAY)
      if (this.counter <= MAX_RECONNECT_COUNT) connect()
    }
  }
})
