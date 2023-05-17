<script setup lang="ts">
import type { VideoTask } from '@/components/task'

const props = defineProps<{
  modelValue: VideoTask
}>()

</script>

<template>
  {{ props.modelValue.title }}
</template>

<style scoped>

</style>
