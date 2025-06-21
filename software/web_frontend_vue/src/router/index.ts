/**
 * 路由配置文件
 * 
 * 使用说明：
 * 1. 布局组件配置
 *    - 可以根据不同的场景使用不同的布局组件
 *    - AdminLayout: 管理后台布局（带侧边栏和顶部导航）
 *    - BasicLayout: 基础布局（简单页面布局）
 *    - PortalLayout: 门户网站布局（带响应式导航和页脚）
 * 
 * 2. 路由配置
 *    - path: 路由路径
 *    - name: 路由名称，用于编程式导航
 *    - component: 路由组件，支持动态导入
 *    - meta: 路由元信息，可包含标题、权限等信息
 * 
 * 3. 使用示例：
 *    - 普通路由：{ path: '/home', name: 'Home', component: Home }
 *    - 带布局的路由：使用 children 配置子路由
 *    - 懒加载路由：component: () => import('@/views/xxx.vue')
 */

import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import PortalLayout from '@/layouts/PortalLayout.vue'

// 定义路由配置
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: PortalLayout,
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/home/index.vue'),
        meta: { title: '首页' }
      },
      {
        path: '/settings',
        name: 'Settings',
        component: () => import('@/views/settings/index.vue'),
        meta: { title: '系统设置' }
      }
    ]
  },
  {
    // 404 页面
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/404.vue'),
    meta: { title: '页面未找到' }
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 路由守卫
router.beforeEach((to, _from, next) => {
  // 设置页面标题
  document.title = `${to.meta.title || '默认标题'} - ${import.meta.env.VITE_APP_TITLE || 'My Vue App'}`
  next()
})

export default router