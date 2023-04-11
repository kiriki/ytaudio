import { defineStore } from 'pinia'
import axios from 'axios'

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

const TOKEN_OBTAIN_URL = 'api/token/'
const TOKEN_REFRESH_URL = 'api/token/refresh/'
// const TOKEN_VERIFY_URL = 'api/token/verify/'
const LS_TOKEN_KEY = 'jwttoken'
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
      const res = await axios.post(TOKEN_OBTAIN_URL, creds)
      console.log('success post login credentials')
      this.tokens = res.data
      this.storeToLs()
    },

    logout () {
      localStorage.removeItem(LS_TOKEN_KEY)
      this.$reset()
    },

    async checkToken () {
      // todo check if token is valid
    },

    loginRestore () {
      // load Tokens
      // set store state if token exists the local storage
      const data = JSON.parse(localStorage.getItem(LS_TOKEN_KEY) || '""')
      if (data) this.tokens = data
    },
    storeToLs () {
      localStorage.setItem(LS_TOKEN_KEY, JSON.stringify(this.tokens))
    },

    async refresh () {
      console.log('refresh JWT')
      try {
        const res = await axios.post(TOKEN_REFRESH_URL, { refresh: this.tokens.refresh })
        this.tokens.access = res.data.access
        this.storeToLs()
      } catch (e) {
        this.logout()
      }
    }
  }
})
