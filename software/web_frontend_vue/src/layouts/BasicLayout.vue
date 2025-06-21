<!--
使用说明：
1. 适用场景：简单的页面布局，如登录页、注册页、详情页等
2. 特点：
   - 简洁的页面结构
   - 可选的顶部导航和页脚
   - 居中的内容区域
3. 使用方法：
   import { BasicLayout } from '@/layouts/BasicLayout.vue'
   
   <BasicLayout>
     <template #header>
         可选的顶部内容     
     </template>
     <template #default>
       主要内容 
     </template>
     <template #footer>
       可选的底部内容 
     </template>
   </BasicLayout>
-->

<template>
  <el-container class="basic-layout">
    <!-- 顶部区域 -->
    <el-header v-if="$slots.header" class="header">
      <slot name="header"></slot>
    </el-header>

    <!-- 主要内容区域 -->
    <el-main class="main-content">
      <div class="content-wrapper">
        <slot></slot>
      </div>
    </el-main>

    <!-- 底部区域 -->
    <el-footer v-if="$slots.footer" class="footer">
      <slot name="footer"></slot>
    </el-footer>
  </el-container>
</template>

<script lang="ts" setup>
// 组件逻辑
</script>

<style scoped>
.basic-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  position: sticky;
  top: 0;
  z-index: 100;
}

.main-content {
  flex: 1;
  padding: 24px;
  background-color: #f0f2f5;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  background-color: #fff;
  padding: 24px;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.footer {
  background-color: #f7f9fc;
  text-align: center;
  padding: 24px;
}

/* 响应式设计 */
@media screen and (max-width: 768px) {
  .main-content {
    padding: 16px;
  }

  .content-wrapper {
    padding: 16px;
  }

  .header, .footer {
    padding: 12px;
  }
}

@media screen and (max-width: 480px) {
  .main-content {
    padding: 8px;
  }

  .content-wrapper {
    padding: 12px;
  }
}
</style> 