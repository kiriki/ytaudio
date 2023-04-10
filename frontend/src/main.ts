import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
// import "@/styles/index.scss"
import 'uno.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

const dev = import.meta.env.NODE_ENV !== 'production'
console.log(`dev = ${dev}`)
