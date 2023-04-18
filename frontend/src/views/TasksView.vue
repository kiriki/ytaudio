<template>
  <h2>Tasks</h2>
  <el-row>
    <el-col :span="6">
      <el-input v-model="input" placeholder="Please input" clearable size="small" />
      <el-button @click="handleAddTask" type="primary" :icon="Plus">Add</el-button>
    </el-col>
  </el-row>
  <el-table :data="tasksData">
    <el-table-column prop="id" label="id" width="50" />
    <el-table-column prop="url" label="utl" width="200" />
    <el-table-column prop="user" label="user" width="200" />
  </el-table>
</template>

<script setup lang="ts">
import { Plus } from '@element-plus/icons-vue'
import { onMounted, ref } from 'vue'

import api from '@/api'

const tasksData = ref([])
const input = ref('')
const dialogVisible = ref(false)

onMounted(async () => {
  console.log('mounted')
  // await store.loadUsers()
  const res = await api().get('tasks')
  tasksData.value = res.data.results
})

const handleAddTask = async () => {
  const res = await api().post('tasks/', { 'url': input.value })
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>

</style>
