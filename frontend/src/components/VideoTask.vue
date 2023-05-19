<script setup lang="ts">
import type { IVideoTask } from '@/components/task'
import api from '@/api'
import { ElMessage } from 'element-plus'

const props = defineProps<{
  videoData: IVideoTask
}>()

const formatTime = (seconds: number) => {
  const timeString = new Date(seconds * 1000).toISOString().slice(11, 19)
  return timeString.startsWith('00') ? timeString.slice(3) : timeString
}

const runGetAudioTask = async () => {
  console.log('runSampleTask')
  // isRunningTask.value = true
  currentTask.value = await startTask('sample_task_progress', { steps: 5 })
}

const startTask = async (taskName: string, params = {}) => {
  const { data } = await api().post('tasks/run_task/', { task_name: taskName, params })

  ElMessage(`Task ${taskName} is started ${data.task_id}`)

  return data as IClTask
}


</script>

<template>
  <el-card style="width: 400px">
    <a :href="props.videoData.url" target="_blank">
      <img
        :src="props.videoData.thumbnail"
        class="image"
      />
    </a>
    <div style="padding: 14px">
      <span>{{ props.videoData.title }}</span> <br>
      <span>{{ props.videoData.channel }}</span>
      <div class="bottom">
        <time class="time">{{ formatTime(props.videoData.duration) }}</time>
        <time class="time">{{ props.videoData.extractor }}</time>
      </div>
      <div>
        <el-button class="button" @click="runGetAudioTask">Get Audio</el-button>
      </div>
    </div>
  </el-card>
  <pre>
    {{ props.videoData }}
  </pre>
</template>

<style scoped>
.image {
  width: 320px;
  display: block;
}

.time {
  font-size: 12px;
  color: #999;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.button {
  padding: 0;
  min-height: auto;
}
</style>
