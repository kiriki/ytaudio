<script setup lang="ts">
import { ref, Ref } from 'vue'
import { ElMessage } from 'element-plus'

import type { IClTask } from '@/interfaces/tasks'
import type { IVideoTask } from '@/components/task'

import { dateShort, formatBytes, formatTime } from '@/filters/formatters'
import api from '@/api'
import { Download } from '@element-plus/icons-vue'

const props = defineProps<{
  videoData: IVideoTask
}>()

const currentTask: Ref<IClTask | null> = ref(null)

const runGetAudioTask = async () => {
  console.log('runSampleTask')
  currentTask.value = await startTask('fetch_audio_task',
    {
      video_source_id: props.videoData.id
    }
  )
}

const startTask = async (taskName: string, params = {}) => {
  const { data } = await api().post('tasks/run_task/', { task_name: taskName, params })
  ElMessage(`Task ${taskName} is started ${data.task_id}`)
  return data as IClTask
}
</script>

<template>
  <el-card style="width: 400px; padding: 5px">
    <div class="bottom">
      <el-tag type="info">{{ props.videoData.extractor }}</el-tag>
      <el-link
        type="primary"
        :href="`https://www.youtube.com/${props.videoData.uploader_id}`">
        {{ props.videoData.channel }}
      </el-link>
      <time class="time">{{ formatTime(props.videoData.duration) }}</time>
    </div>

    <a :href="props.videoData.url" target="_blank">
      <img
        :src="props.videoData.thumbnail"
        class="image"
      />
    </a>
    <div style="padding: 14px">
      <span>{{ props.videoData.title }}</span> {{ dateShort(props.videoData.upload_date) }}<br>
      <div>
        <el-button class="button" @click="runGetAudioTask">Get Audio</el-button>
      </div>
      <div v-if="props.videoData.file">
        <el-button
          type="success"
          :icon="Download"
          round
          tag="a"
          :href="props.videoData.file"
          download
        >
          Download ({{ formatBytes(props.videoData.file_size) }})
        </el-button>
      </div>
    </div>
  </el-card>
  <pre v-if="false">
    {{ props.videoData }}
  </pre>
</template>

<style scoped>
.image {
  width: 350px;
  display: block;
  padding: 10px;
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
