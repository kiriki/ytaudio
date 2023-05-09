<script setup lang="ts">
import api from '@/api'
import { Ref, ref } from 'vue'
import { ElMessage } from 'element-plus'

const isRunningTask = ref(false)
const currentTask: Ref<IClTask | null> = ref(null)

interface IClTask {
  action: string
  task_id: string
  task_status: string
  task_result: number
}

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

const startTask = async (taskName: string, params = {}) => {
  const { data } = await api().post('tasks/run_task/', { task_name: taskName, params })
  console.log('task created and run')
  ElMessage(`Task ${taskName} is started ${data.task_id}`)
  console.log(data)
  return data as IClTask
}

const runSampleTask = async () => {
  console.log('runSampleTask')
  isRunningTask.value = true
  currentTask.value = await startTask('sample_task_progress', { steps: 5 })
  await waitTaskDone(currentTask.value.task_id)//  wait for result
  isRunningTask.value = false
}

const waitTaskDone = async (taskId: string) => {
  console.log('waitTaskDone', taskId)
  while (isRunningTask.value) {
    await sleep(1000)
    const params = { task_id: taskId }
    const { data }: { data: IClTask } = await api().get('tasks/get_task_status', { params })
    currentTask.value = data // call on progress here ?
    console.log('waitTaskDone', data)
    if (currentTask.value.task_status === 'SUCCESS' || currentTask.value.task_status === 'FAILURE') break
  }

  console.log('task is done: ', currentTask.value)
  return currentTask.value
}

const chatSocket = new WebSocket(`ws://${window.location.host}/ws/tasks/`)

chatSocket.onopen = (e) => {
  console.log('ws tasks open')
  console.log(e)
}

chatSocket.onmessage = (e) => {
  console.log('ws tasks msg')
  const data = JSON.parse(e.data)
  console.log(data)
  // if (currentTask.value) {
  //   currentTask.value.task_status = data.data.state
  //   currentTask.value.task_result = data.data.meta['current_value']
  // }
}

chatSocket.onclose = (e) => {
  console.log('ws tasks close')
  console.log(e)
}

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
