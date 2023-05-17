import { defineStore } from 'pinia'

export const useLsStore = defineStore({
  id: 'ls',
  state: () => ({}),
  getters: {},

  actions: {
    load (key: string) {
      console.log(`ls localStorage load: ${key}`)
      if (localStorage.getItem(key)) {
        return JSON.parse(localStorage.getItem(key) || '')
      }
    },

    store (key: string, data: any) {
      console.log(`ls localStorage store: ${key}`)
      localStorage.setItem(key, JSON.stringify(data))
    }
  }
})
