import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
// import filters from './filters'

import "@/styles/index.scss";
import 'uno.css'

// If you want to use ElMessage, import it.
import 'element-plus/theme-chalk/src/message.scss'
import 'element-plus/theme-chalk/src/notification.scss'
import 'element-plus/theme-chalk/src/message-box.scss'

const app = createApp(App)

app.use(createPinia())
app.use(router)
// app.use(filters)

app.mount('#app')

const dev = import.meta.env.NODE_ENV !== 'production'
console.log(`dev = ${dev}`)
