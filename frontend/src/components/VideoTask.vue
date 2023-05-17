<script setup lang="ts">
import type { IVideoTask } from '@/components/task'

const props = defineProps<{
  videoData: IVideoTask
}>()

</script>

<template>
  <!--  Video task-->
  <!--  <pre>-->
  <!--    {{ props.videoData }}-->
  <!--  </pre>-->
  <el-card :body-style="{ padding: '0px' }">
    <img
      :src="props.videoData.thumbnail"
      class="image"
    />
    <div style="padding: 14px">
      <span>{{ props.videoData.title }}</span> <br>
      <span>{{ props.videoData.channel }}</span>
      <div class="bottom">
        <time class="time">{{ props.videoData.extractor }}</time>
        <el-button text class="button">Operating</el-button>
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
</style>
