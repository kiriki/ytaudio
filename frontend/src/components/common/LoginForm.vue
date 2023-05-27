<template>
  <div>
    <div
      v-if="loggedin"
      class="logout"
    >
      <el-button @click="logout">
        Logout
      </el-button>
    </div>
    <el-row
      v-else
      class="login"
    >
      <el-form
        ref="loginFormRef"
        :model="formData"
        :rules="rules"
        label-position="left"
        label-width="100px"
        size="small"
      >
        <el-form-item
          ref="username"
          label="User Name:"
          prop="username"
        >
          <el-input
            v-model="formData.username"
            @keyup.enter="$refs.passInput.focus()"
          />
        </el-form-item>
        <el-form-item
          ref="passwordRef"
          label="Password:"
          prop="password"
        >
          <el-input
            ref="passInput"
            v-model="formData.password"
            type="password"
            @keyup.enter="submit"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            @click="submit"
          >
            Login
          </el-button>
        </el-form-item>
      </el-form>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { ElFormItem, ElNotification } from 'element-plus'
import type { ElForm } from 'element-plus'

import { useAuthStore } from '@/stores/auth'

const store = useAuthStore()

const formData = ref({
  username: '',
  password: '',
})

const rules = ref({
  username: [
    {
      required: true,
      message: 'Please input username',
      trigger: 'blur',
    },
  ],
  password: [
    {
      required: true,
      message: 'Please input password',
      trigger: 'blur',
    },
  ],
})

const loginFormRef = ref<InstanceType<typeof ElForm> | null>(null)
const passwordRef = ref<InstanceType<typeof ElFormItem> | null>(null)

const loggedin = computed(() => store.isAuth)

const submit = async () => {
  console.info('do login')
  try {
    if (loginFormRef.value) await loginFormRef.value.validate()
    await doSubmit()
  } catch (e) {
    console.log('not valid', e)
  }
}

const doSubmit = async () => {
  console.log('doSubmit')
  try {
    await store.login(formData.value)
    ElNotification.success({
      title: 'Success',
      message: 'Login is ok',
    })

  } catch ({ response: { status, statusText, data } }) {
    console.error('login error')
    passwordRef.value?.resetField()

    const message = (data as object).detail || `${status} (${statusText})`

    ElNotification.error({
      title: 'Login Error',
      message,
    })
  }
}

const logout = async () => {
  console.log('do logout')
  await store.logout()

  ElNotification.success({
    title: 'Success',
    message: 'Logout',
  })
}

</script>

<style>
.login {
  margin: 120px auto;
  width: 25em;
  min-width: 300px;
  /*background-color: #eaebf2;*/
}

.logout {
  padding: 10px 0;
}
</style>
