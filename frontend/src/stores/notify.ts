import { defineStore } from 'pinia'
import connect from '@/notifications/connect'

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

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

    receiveNotification (payload) {
      console.log('receiveNotification')
      console.log(payload)
      this.message = payload
    },

    async notificationsConnect (counter: number) {
      console.log('notificationsConnect', counter)
      if (counter > 1) {
        await sleep(1000)
      }
      connect(counter)
    }
  }
})
