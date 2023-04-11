<template>
  <div class="hello">
    <h2>Users</h2>
    {{ users }}
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useUsersStore } from '@/stores/users'

defineProps({
  msg: {
    type: String,
    default: ''
  }
})
const store = useUsersStore()
const users = computed(() => store.users)

onMounted(async () => {
  console.log('mounted')
  await store.loadUsers()
})
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
