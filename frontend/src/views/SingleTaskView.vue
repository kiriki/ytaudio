<script setup lang="ts">
import { computed, onMounted, ref, Ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElInput, ElMessage } from 'element-plus'
import { useTasksStore } from '@/stores/tasks'

import VideoTask from '@/components/VideoTask.vue'
import { AxiosError } from 'axios'

const UrlInputRef: Ref<typeof ElInput | null> = ref(null)
const UrlInputData = ref('')

const storeTasks = useTasksStore()

const currentTask = computed(() => storeTasks.currentTask)

const onEsc = () => UrlInputRef.value?.clear()

const handleAddTask = async () => {
  console.log('handleAddTask')
  try {
    await storeTasks.getTaskFromUrl(UrlInputData.value)
  } catch (e) {
    if (e instanceof AxiosError) {
      for (const errorKey in e.response?.data) {
        e.response.data[errorKey].forEach((errorValue: string) =>
          ElMessage.error(`${errorKey}: ${errorValue}`))
      }
    }
  }
  UrlInputRef.value?.clear()
}

onMounted(() => storeTasks.loadCurrentTask())


</script>

<template>
  <el-row>
    <el-col :span="6">
      <el-input
        ref="UrlInputRef"
        v-model="UrlInputData" placeholder="Video url" clearable size="small"
        @keyup.enter="handleAddTask"
        @keydown.esc="onEsc"
      >
        <template #append>
          <el-button @click="handleAddTask" type="primary" :icon="Plus">
            Load
          </el-button>
        </template>
      </el-input>
    </el-col>
  </el-row>
  <!--  <pre v-if="currentTask">{{ currentTask.id }}</pre>-->
  <video-task :videoData="currentTask" v-if="currentTask" />
</template>

<style scoped>

</style>
