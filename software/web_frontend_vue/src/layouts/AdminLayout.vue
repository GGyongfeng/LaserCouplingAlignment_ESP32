<!--
使用说明：
1. 适用场景：管理后台、工作台等需要侧边栏导航的页面
2. 特点：
   - 左侧固定导航栏（移动端可收起）
   - 顶部导航栏
   - 响应式设计
3. 使用方法：
   import { AdminLayout } from '@/layouts/AdminLayout.vue'
   
   <AdminLayout>
     <template #header>
       顶部导航内容
     </template>
     <template #sidebar>
       侧边栏内容
     </template>
     <template #default>
       主要内容
     </template>
   </AdminLayout>
-->

<template>
  <el-container class="admin-layout">
    <!-- 侧边栏 -->
    <el-aside :width="isCollapse ? '64px' : '200px'" class="sidebar">
      <div class="logo-container">
        <el-image 
          v-if="!isCollapse"
          src="https://element-plus.org/images/element-plus-logo.svg"
          style="width: 120px; height: 32px"
          fit="contain"
        />
        <el-image 
          v-else
          src="https://element-plus.org/images/element-plus-logo-small.svg"
          style="width: 32px; height: 32px"
          fit="contain"
        />
      </div>
      <slot name="sidebar">
        <!-- 默认侧边栏内容 -->
        <el-menu
          :collapse="isCollapse"
          :collapse-transition="false"
          class="sidebar-menu"
          background-color="#304156"
          text-color="#fff"
          active-text-color="#409EFF"
        >
          <el-menu-item index="1">
            <el-icon><House /></el-icon>
            <template #title>首页</template>
          </el-menu-item>
          <el-menu-item index="2">
            <el-icon><Document /></el-icon>
            <template #title>文档</template>
          </el-menu-item>
          <el-menu-item index="3">
            <el-icon><Setting /></el-icon>
            <template #title>设置</template>
          </el-menu-item>
        </el-menu>
      </slot>
    </el-aside>

    <!-- 主容器 -->
    <el-container>
      <!-- 顶部导航 -->
      <el-header class="header">
        <div class="header-left">
          <el-button @click="toggleCollapse">
            <el-icon><Fold v-if="!isCollapse"/><Expand v-else/></el-icon>
          </el-button>
        </div>
        <slot name="header">
          <!-- 默认顶部导航内容 -->
          <div class="header-right">
            <el-dropdown>
              <span class="el-dropdown-link">
                管理员 <el-icon><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>个人信息</el-dropdown-item>
                  <el-dropdown-item>退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </slot>
      </el-header>

      <!-- 主要内容区域 -->
      <el-main class="main-content">
        <slot></slot>
      </el-main>
    </el-container>
  </el-container>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { 
  Fold, 
  Expand, 
  House, 
  Document, 
  Setting,
  ArrowDown
} from '@element-plus/icons-vue'

const isCollapse = ref(false)

const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}
</script>

<style scoped>
.admin-layout {
  height: 100vh;
}

.sidebar {
  background-color: #304156;
  transition: width 0.3s;
  overflow: hidden;
}

.logo-container {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2b2f3a;
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
}

.el-dropdown-link {
  cursor: pointer;
  display: flex;
  align-items: center;
  color: #606266;
}

.main-content {
  background-color: #f0f2f5;
  padding: 20px;
}

.sidebar-menu {
  border-right: none;
}

/* 响应式设计 */
@media screen and (max-width: 768px) {
  .sidebar {
    position: fixed;
    z-index: 1000;
    height: 100vh;
    transform: translateX(0);
    transition: transform 0.3s;
  }

  .sidebar.collapsed {
    transform: translateX(-200px);
  }

  .el-main {
    padding-left: 64px;
  }
}
</style> 