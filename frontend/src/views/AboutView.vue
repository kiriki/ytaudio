<script setup lang="ts">
import { Refresh } from '@element-plus/icons-vue'
</script>

<template>
  <div class="about">
    <h1>This is an about page</h1>
    <el-button type="warning">
      <el-icon>
        <Refresh />
      </el-icon>
    </el-button>
    <br>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
