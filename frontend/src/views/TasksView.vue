<template>
  <h2>Tasks</h2>
  <el-row>
    <el-col :span="6">
      <el-input v-model="input" placeholder="Please input" clearable size="small" />
      <el-button @click="handleAddTask" type="primary" :icon="Plus">Add</el-button>
    </el-col>
  </el-row>
  <el-table :data="tasksData">
    <el-table-column label="Video" width="300">
      <template #default="{row}">
        <el-link :href="row.url" target="_blank">
          {{ row.title }}
        </el-link>
      </template>
    </el-table-column>
    <el-table-column prop="duration" label="Duration" width="80">
      <template #default="{row}">
        <time class="time">{{ formatTime(row.duration) }}</time>
      </template>
    </el-table-column>
    <el-table-column prop="upload_date" label="upload date" width="200" />
    <el-table-column prop="file" label="File" width="200">
      <template #default="{row}">
        <a :href="row.file" target="_blank" download>mp3</a>
      </template>
    </el-table-column>
    <el-table-column prop="user" label="user" width="200" />
  </el-table>
</template>

<script setup lang="ts">
import { Plus } from '@element-plus/icons-vue'
import { onMounted, ref, watch } from 'vue'

import api from '@/api'
import { useNotifyStore } from '@/stores/notify'
import { formatTime } from '@/filters/formatters'

const store = useNotifyStore()

const tasksData = ref([])
const input = ref('')
const dialogVisible = ref(false)

onMounted(async () => {
  console.log('mounted')
  // await store.loadUsers()
  await reloadTasks()
})

const handleAddTask = async () => {
  const res = await api().post('tasks/', { 'url': input.value })
}

watch(() => store.message, (value) => {
  if (value.data?.action === 'reload') {
    reloadTasks()
  }
  // if (currentTask.value) {
  //   currentTask.value.task_status = value.data.state
  //   currentTask.value.task_result = value.data.meta['current_value']
  // }
})
const reloadTasks = async () => {
  const res = await api().get('tasks')
  tasksData.value = res.data.results
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>

</style>
