import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import './assets/styles/main.scss'

const currentVersion = import.meta.env.VITE_APP_VERSION;
const cachedVersion = localStorage.getItem('app_version');

// 版本号调用.env.VITE_APP_VERSION
// 控制用户版本号，如果版本号不一致，则清除缓存，并强制刷新页面
if (cachedVersion !== currentVersion) {
  localStorage.clear(); // 清除缓存
  localStorage.setItem('app_version', currentVersion);
  window.location.reload(); // 强制刷新页面
}

// 标题调用.env.VITE_APP_TITLE
document.title = import.meta.env.VITE_APP_TITLE || 'My Vue App';

const app = createApp(App);
app.use(router);
app.use(ElementPlus);
app.mount('#app');
