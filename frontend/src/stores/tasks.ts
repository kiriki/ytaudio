import { defineStore } from 'pinia'
import api from '@/api'

interface State {
  stateValue: Array<object>
}

export const use$StoreId$Store = defineStore({
  id: '$StoreId$',

  state: (): State => ({
    stateValue: [],
  }),

  getters: {
    getStateValue: state => {
      return state.stateValue
    }
  },

  actions: {
    async action1 () {
      return
    },
  },
})
