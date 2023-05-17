import { defineStore } from 'pinia'
import api from '@/api'
import type { IVideoTask } from '@/components/task'
import { useLsStore } from '@/stores/ls'

interface State {
  currentTaskId: number | null
  currentTask: IVideoTask | null
}

const LS_CURRENT_TASK_ID = 'current_task_id'

export const useTasksStore = defineStore({
  id: 'tasks',

  state: (): State => ({
    currentTaskId: null,
    currentTask: null,
  }),

  getters: {
    getStateValue: state => {
      return state.stateValue
    }
  },

  actions: {
    setCurrentTaskId (taskId: number) {
      this.currentTaskId = taskId
      this.storeCurrentTaskId()
    },

    loadCurrentTaskId () {
      const ls = useLsStore()
      const t = ls.load(LS_CURRENT_TASK_ID)
      if (t) this.currentTaskId = +t
    },

    storeCurrentTaskId () {
      const ls = useLsStore()
      ls.store(LS_CURRENT_TASK_ID, this.currentTaskId)
    },

    async loadCurrentTask () {
      this.loadCurrentTaskId()
      if (!this.currentTaskId) return
      const { data } = await api().get(`tasks/${this.currentTaskId}`)
      this.currentTask = <IVideoTask>data
    },

    async getTaskFromUrl (videoUrl: string) {
      const { data } = await api().post('tasks/', { 'url': videoUrl })
      this.currentTask = <IVideoTask>data
      // this.setCurrentTaskId(this.currentTask.id)
    }
  },
})
