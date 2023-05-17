<script setup lang="ts">
import { Ref, ref, watch } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElInput, ElMessage } from 'element-plus'
import api from '@/api'
import { useNotifyStore } from '@/stores/notify'
import VideoTask from '@/components/VideoTask.vue'

const UrlInputRef: Ref<typeof ElInput | null> = ref(null)
const input = ref('')
const currentTaskData = ref({})
const currentTaskId: Ref<number | null> = ref(null)

const store = useNotifyStore()

const onEsc = () => {
  UrlInputRef.value?.clear()
  // UrlInputRef.value?.blur()
}
const handleAddTask = async () => {
  console.log('handleAddTask')
  const { data } = await api().post('tasks/', { 'url': input.value })
  currentTaskData.value = data
  console.log(data)
  UrlInputRef.value?.clear()
}

watch(() => store.message, (value) => {
  if (!value) return
  const { data } = value
  if ('error' in data) {
    ElMessage(data.error)
  }

  if ('action' in data) {
    if (data.action === 'reload') {
      console.log('reload task')
      currentTaskId.value = data.task_pk
      reloadCurrentTask()
    }
  }
  // if (currentTask.value) {
  //   currentTask.value.task_status = value.data.state
  //   currentTask.value.task_result = value.data.meta['current_value']
  // }
})
const reloadCurrentTask = async () => {
  const { data } = await api().get(`tasks/${currentTaskId.value}`)
  currentTaskData.value = data
}

</script>

<template>
  <el-row>
    <el-col :span="6">
      <el-input
        ref="UrlInputRef"
        v-model="input" placeholder="Video url" clearable size="small"
        @keyup.enter="handleAddTask"
        @keydown.esc="onEsc"
      >
        <template #append>
          <el-button @click="handleAddTask" type="primary" :icon="Plus">
            Add
          </el-button>
        </template>
      </el-input>
    </el-col>
  </el-row>
  <pre>
    {{ input }}
  </pre>
  <h3>task:</h3>
  <video-task :model-value="currentTaskData" />
</template>

<style scoped>

</style>
