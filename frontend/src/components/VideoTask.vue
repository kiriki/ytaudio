<script setup lang="ts">
import { computed, ref, Ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Download } from '@element-plus/icons-vue'

import api from '@/api'
import type { IClTask, IVideoTask } from '@/interfaces/tasks'
import { dateShort, formatBytes, formatTime } from '@/filters/formatters'
import { useTasksStore } from '@/stores/tasks'
import { notifier } from '@/ems'

const props = defineProps<{
  videoData: IVideoTask
}>()

const storeTasks = useTasksStore()

const currentTask: Ref<IClTask | null> = ref(null)
const videoData: Ref<IVideoTask> = ref(props.videoData)
const isLoading: Ref<boolean> = computed(() => !videoData.value.title)
const progressData = ref({ status: '', downloaded: 0, total: 0 })

const progressPercent: Ref<number> = computed(() =>
  Math.round(progressData.value.downloaded / progressData.value.total * 100) || 0
)
const isDownloading: Ref<boolean> = computed(() => progressData.value.status === 'downloading')
const isExtracting: Ref<boolean> = computed(() => progressData.value.status === 'finished')

const runGetAudioTask = async () => {
  console.log('runSampleTask')
  videoData.value.file = ''
  currentTask.value = await startTask('fetch_audio_task',
    {
      video_source_id: videoData.value.id
    }
  )
}

const startTask = async (taskName: string, params = {}) => {
  const { data } = await api().post('tasks/run_task/', { task_name: taskName, params })
  ElMessage(`Task ${taskName} is started ${data.task_id}`)
  return data as IClTask
}

watch(props.videoData, () => {
  videoData.value = props.videoData
})

watch(() => storeTasks.currentTask, (value: IVideoTask | null) => {
  if (value) videoData.value = value
})

notifier.on('ws_message', value => {
  if (!value) return
  const { data } = value

  if ('error' in data) ElMessage(data.error)
  if ('action' in data) {
    if (data.action === 'reload') {
      console.log('reload task')

      storeTasks.setCurrentTaskId(data.task_pk)
      storeTasks.loadCurrentTask()

      progressData.value.status = 'reloaded'
    }
  }

  if ('progress' in data) {
    console.log('on progress')
    console.log(data.progress)
    progressData.value.status = data.progress.status
    progressData.value.downloaded = data.progress.downloaded
    progressData.value.total = data.progress.total
  }
})

</script>

<template>
  <el-card style="width: 400px; padding: 5px" v-loading="isLoading">
    <div class="bottom">
      <el-tag type="info">{{ videoData.extractor }}</el-tag>
      <el-link
        type="primary"
        :href="`https://www.youtube.com/${videoData.uploaderId}`">
        {{ videoData.channel }}
      </el-link>
      <time class="time">{{ formatTime(videoData.duration) }}</time>
    </div>
    <a :href="videoData.url" target="_blank">
      <img
        :src="videoData.thumbnail"
        class="image"
      />
    </a>
    <div style="padding: 14px">
      <span>{{ videoData.title }}</span> {{ dateShort(videoData.uploadDate) }}<br>
      <div>
        <el-button class="button" @click="runGetAudioTask">Get Audio</el-button>
      </div>
      <el-progress v-if="isDownloading || isExtracting"
                   :percentage="progressPercent"
                   :text-inside="true"
                   :stroke-width="20"
      />
      <el-button
        v-if="isDownloading"
        type="primary" loading round>downloading...
      </el-button>
      <el-button
        v-if="isExtracting"
        type="warning" loading round>processing...
      </el-button>
      <div v-if="videoData.file">
        <el-button
          type="success"
          :icon="Download"
          round
          tag="a"
          :href="videoData.file"
          download
        >
          Download ({{ formatBytes(videoData.fileSize) }})
        </el-button>
      </div>
    </div>
  </el-card>
  <pre v-if="false">
    {{ videoData }}
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
