import { defineStore } from 'pinia'
import api from '@/api'

interface State {
  tokens: {
    access: string | null,
    refresh: string | null,
  }
}

interface AuthData {
  username: string
  password: string
}

export const useAuthStore = defineStore({
  id: 'auth',

  state: (): State => ({
    tokens: {
      access: null,
      refresh: null,
    }
  }),

  getters: {
    isAuth: (state): boolean => !!state.tokens.refresh,
    jwtToken: (state): string => state.tokens.access ? `JWT ${state.tokens.access}` : ''
  },

  actions: {
    async login (creds: AuthData) {
      const res = await api().post('token/', creds)
      console.log('success post login credentials')
      this.tokens = res.data
      this.storeToLs()
    },

    logout () {
      localStorage.removeItem('jwttoken')
      this.$reset()
    },

    async checkToken () {
      // todo check if token is valid
    },

    loginRestore () {
      // load Tokens
      // set store state if token exists the local storage
      const data = JSON.parse(localStorage.getItem('jwttoken') || '""')
      if (data) this.tokens = data
    },
    storeToLs () {
      localStorage.setItem('jwttoken', JSON.stringify(this.tokens))
    },

    async refresh () {
      console.log('refresh')
      try {
        const res = await api().postRaw('token/refresh/', { refresh: this.tokens.refresh })
        this.tokens.access = res.data.access
        this.storeToLs()
      } catch (e) {
        this.logout()
      }
    }
  }
})
