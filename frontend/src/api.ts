import type { AxiosRequestConfig, AxiosResponse } from 'axios'
import { AxiosError } from 'axios'
import axios from 'axios'

import { useAuthStore } from '@/stores/auth'

interface ErrorData {
  code: string
  detail: string
  messages: Array<object>
}

axios.defaults.baseURL = (import.meta.env.VUE_APP_API_ENDPOINT ?? '') as string

const api = (path = '') => {
  const authStore = useAuthStore()
  const defaultOptions: AxiosRequestConfig = {
    baseURL: `${axios.defaults.baseURL}/api/${path}`,
    paramsSerializer: { indexes: null },
    headers: { Authorization: authStore.jwtToken }
  }
  const instance = axios.create({ ...defaultOptions })

  const refreshTokenWp = async (axiosFn: () => Promise<AxiosResponse>) => {
    try {
      return await axiosFn()
    } catch (e) {
      if (e instanceof AxiosError<ErrorData>) {
        if (e.response?.data.code === 'token_not_valid') {
          await authStore.refresh()
          instance.defaults.headers.Authorization = authStore.jwtToken
          return axiosFn()
        } else {
          console.error('api call error', e.response?.data || e)
          throw e
        }
      } else throw e
    }
  }

  return {
    get: (url = '', options = {}) =>
      refreshTokenWp(() => instance.get(url, { ...options })),
    options: (url = '', options = {}) =>
      refreshTokenWp(() => instance.options(url, { ...options })),
    post: (url = '', data = {}, options = {}) =>
      refreshTokenWp(() => instance.post(url, data, { ...options })),
    postRaw: (url = '', data = {}, options = {}) => instance.post(url, data, { ...options }),
    put: (url = '', data: object, options = {}) =>
      refreshTokenWp(() => instance.put(url, data, { ...options })),
    patch: (url = '', data: object, options = {}) =>
      refreshTokenWp(() => instance.patch(url, data, { ...options })),
    delete: (url = '', options = {}) =>
      refreshTokenWp(() => instance.delete(url, { ...options }))
  }
}

export default api
