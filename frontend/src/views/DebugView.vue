<script setup lang="ts">
import api from '@/api'
import { Ref, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useNotifyStore } from '@/stores/notify'
import { sleep } from '@/utils/tools'
import { notifier } from '@/ems'

const isRunningTask = ref(false)
const currentTask: Ref<IClTask | null> = ref(null)

interface IClTask {
  action: string
  task_id: string
  task_status: string
  task_result: number
}

const startTask = async (taskName: string, params = {}) => {
  const { data } = await api().post('tasks/run_task/', { task_name: taskName, params })
  console.log('task created and run')
  ElMessage(`Task ${taskName} is started ${data.task_id}`)
  console.log(data)
  return data as IClTask
}

const runSampleTask = async () => {
  console.log('runSampleTask')
  // isRunningTask.value = true
  currentTask.value = await startTask('sample_task_progress', { steps: 5 })
  // await waitTaskDone(currentTask.value.task_id)//  wait for result
  // isRunningTask.value = false
}

// const waitTaskDone = async (taskId: string) => {
//   console.log('waitTaskDone', taskId)
//   while (isRunningTask.value) {
//     await sleep(1000)
//     const params = { task_id: taskId }
//     const { data }: { data: IClTask } = await api().get('tasks/get_task_status', { params })
//     currentTask.value = data // call on progress here ?
//     console.log('waitTaskDone', data)
//     if (currentTask.value.task_status === 'SUCCESS' || currentTask.value.task_status === 'FAILURE') break
//   }
//
//   console.log('task is done: ', currentTask.value)
//   return currentTask.value
// }

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
