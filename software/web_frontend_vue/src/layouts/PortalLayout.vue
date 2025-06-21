<!--
使用说明：
1. 适用场景：企业官网、门户网站、产品展示等
2. 特点：
   - 响应式顶部导航
   - 可折叠的移动端菜单
   - 通用页脚
   - 宽屏适配
3. 使用方法：
   import { PortalLayout } from '@/layouts/PortalLayout.vue'
   
   <PortalLayout>
     <template #nav>
       导航菜单内容 
     </template>
     <template #default>
       主要内容 
     </template>
     <template #footer>
     自定义页脚内容 
     </template>
   </PortalLayout>
-->

<template>
  <el-container class="portal-layout">
    <!-- 顶部导航 -->
    <el-header class="header">
      <div class="nav-container">
        <div class="logo">
          <img src="@/assets/measure.svg" style="width: 60px; height: 30px" />
          <span>激光测距器</span>
        </div>

        <!-- 桌面端导航 -->
        <div class="desktop-nav" v-show="!isMobile">
          <slot name="nav">
            <!-- 默认导航内容 -->
            <el-menu mode="horizontal" :router="true">
              <el-menu-item index="/">首页</el-menu-item>
              <el-menu-item index="/settings">设置</el-menu-item>
              <el-menu-item index="/contact">联系我们</el-menu-item>
            </el-menu>
          </slot>
        </div>

        <!-- 移动端菜单按钮 -->
        <div class="mobile-nav" v-show="isMobile">
          <el-button @click="toggleMobileMenu">
            <el-icon>
              <Menu />
            </el-icon>
          </el-button>
        </div>
      </div>

      <!-- 移动端导航抽屉 -->
      <el-drawer v-model="showMobileMenu" direction="rtl" size="80%" title="导航菜单">
        <slot name="nav">
          <!-- 默认移动端导航内容 -->
          <el-menu mode="vertical" :router="true">
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/settings">设置</el-menu-item>
            <el-menu-item index="/contact">联系我们</el-menu-item>
          </el-menu>
        </slot>
      </el-drawer>
    </el-header>

    <!-- 主要内容区域 -->
    <el-main class="main-content">
      <router-view></router-view>
    </el-main>

    <!-- 页脚 -->
    <el-footer class="footer">
      <slot name="footer">
        <div class="footer-content">
          <div class="footer-section">
            <h3>关于我们</h3>
            <p>公司简介</p>
            <p>联系方式</p>
          </div>
          <div class="footer-section">
            <h3>服务支持</h3>
            <p>帮助中心</p>
            <p>常见问题</p>
          </div>
          <div class="footer-section">
            <h3>联系我们</h3>
            <p>电话：123-456-7890</p>
            <p>邮箱：contact@example.com</p>
          </div>
        </div>
        <div class="copyright">
          © {{ new Date().getFullYear() }} Your Company. All rights reserved.
        </div>
      </slot>
    </el-footer>
  </el-container>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Menu } from '@element-plus/icons-vue'

const isMobile = ref(false)
const showMobileMenu = ref(false)

const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<style scoped>
.portal-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  padding: 0;
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  height: 40px;
  display: flex;
  align-items: center;
}

.main-content {
  flex: 1;
  padding: 0;
  background-color: #fff;
}

.footer {
  background-color: #2c3e50;
  color: #fff;
  padding: 20px 20px;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}

.footer-section h3 {
  margin-bottom: 20px;
  font-size: 18px;
}

.footer-section p {
  margin: 10px 0;
  color: #a8b2bc;
}

.copyright {
  text-align: center;
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* 响应式设计 */
@media screen and (max-width: 768px) {
  .footer {
    background-color: #DDE3E9;
  }

  .footer-content {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .nav-container {
    padding: 0 16px;
  }

  .desktop-nav {
    display: none;
  }

  .footer-section h3 {
    color: #5F6368;
  }
}

@media screen and (min-width: 769px) {
  .mobile-nav {
    display: none;
  }
}

.desktop-nav {
  flex: 1;
  margin-left: 40px;
}

.desktop-nav :deep(.el-menu) {
  border: none;
  width: 100%;
  display: flex;
}

.desktop-nav :deep(.el-menu--horizontal > .el-menu-item) {
  height: 60px;
  line-height: 60px;
  color: #333;
}

.el-drawer :deep(.el-menu) {
  border-right: none;
  background-color: transparent;
}

.el-drawer :deep(.el-menu-item) {
  color: #333;
}
</style>