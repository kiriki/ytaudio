<template>
  <el-config-provider
    namespace="ep"
    v-bind="config"
  >
    <el-container v-if="isAuth">
      <el-header v-if="true">
        <el-row
          align="middle"
          justify="space-between"
          type="flex"
        >
          <el-col :span="6">

          </el-col>
          <el-col
            :span="1"
            style="display: flex"
          >
            <LoginForm />
            <button
              class="border-none bg-transparent cursor-pointer"
              @click="toggleDark()"
            >
              <i
                inline-flex
                i="dark:ep-moon ep-sunny"
              />
            </button>
          </el-col>
        </el-row>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu :router="true">
            <el-menu-item index="/">Home</el-menu-item>
            <el-menu-item index="/users">Users</el-menu-item>
            <el-menu-item index="/tasks">Tasks</el-menu-item>
            <el-menu-item index="/debug">Debug </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
    <div v-else>
      <LoginForm />
    </div>
  </el-config-provider>
</template>

<script lang="ts" setup>
import { computed, onMounted } from 'vue'
import ru from 'element-plus/lib/locale/lang/ru'

import LoginForm from '@/components/common/LoginForm.vue'
import { toggleDark } from '@/composables'
import { useAuthStore } from '@/stores/auth'
import { useNotifyStore } from '@/stores/notify'

const config = { locale: ru, size: 'small', zIndex: 3000 }
const authStore = useAuthStore()
const notifyStore = useNotifyStore()

const isAuth = computed(() => authStore.isAuth)

onMounted(() => {
  console.log('App is mounted!')
  // todo проверять валидность токена, если присутствует
  authStore.loginRestore()
  notifyStore.notificationsConnect(0)
})
</script>

<style lang="scss">
#app {
  font-weight: normal;
  //text-align: center;
  color: var(--ep-text-color-primary);
}

header {
  line-height: 1.5;
  max-height: 100vh;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}

a, .green {
  text-decoration: none;
  //color: hsla(160, 100%, 37%, 1);
  //определено в @/styles/index.scss";
  transition: 0.4s;
}

@media (hover: hover) {
  a:hover {
    //background-color: hsla(160, 100%, 37%, 0.2);
  }
}

.ep-row {
  margin-bottom: 20px;

  &:last-child {
    margin-bottom: 0;
  }
}

.ep-col {
  //border-radius: 4px;
}

.ep-main {
  padding: 5px;
}
</style>
