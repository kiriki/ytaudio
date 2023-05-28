<script setup lang="ts">
import { Ref, ref } from 'vue'
import { ElMessage } from 'element-plus'

import api from '@/api'
import { notifier } from '@/ems'
import type { IClTask } from '@/interfaces/tasks'

const currentTask: Ref<IClTask | null> = ref(null)

const startTask = async (taskName: string, params = {}) => {
  const { data } = await api().post('tasks/run_task/', { task_name: taskName, params })
  console.log('task created and run')
  ElMessage(`Task ${taskName} is started ${data.task_id}`)
  console.log(data)
  return data as IClTask
}

const runSampleTask = async () => {
  console.log('runSampleTask')
  currentTask.value = await startTask('sample_task_progress', { steps: 5 })
}

notifier.on('ws_message', e => {
  console.log('emitter ws_message', e)
  if (currentTask.value) {
    currentTask.value.task_status = e.data.state
    currentTask.value.task_result = e.data.meta['current_value']
  }
})

</script>

<template>
  <el-button @click="runSampleTask">sample_task_progress</el-button>
  <br>
  currentTaskId = {{ currentTask?.task_id }} <br>
  status = {{ currentTask?.task_status }} <br>
  result = {{ currentTask?.task_result }}
</template>

<style scoped>

</style>
