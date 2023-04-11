import api from '@/api'
import { defineStore } from 'pinia'

import User from '@/components/UserClass'
import { useAuthStore } from './auth'

interface State {
  users: Array<User>
  total: number
}

export const useUsersStore = defineStore({
  id: 'users',

  state: (): State => ({
    users: [],
    total: 0
  }),

  actions: {
    async loadUsers () {
      console.debug('load users')
      const auth = useAuthStore()

      this.users = []

      try {
        const res = await api().get('users/')

        for (const data of res.data.results) {
          this.users.push(new User(data))
        }
        this.total = res.data.count

      } catch ({ response: { status, statusText, data: { code } } }) {
        if (code === 'token_not_valid') {
          await auth.refresh()
        }
      }
    }
  },
})
