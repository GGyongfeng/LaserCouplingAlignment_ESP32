<template>
  <div class="settings">
    <el-card class="settings-card">
      <template #header>
        <h3>系统设置</h3>
      </template>
      
      <el-form :model="form" label-width="120px">
        <el-form-item label="自动测量间隔">
          <el-input-number
            v-model="form.measureInterval"
            :min="1"
            :max="60"
            :step="1"
          /> 秒
        </el-form-item>

        <el-form-item label="数据保存路径">
          <el-input v-model="form.savePath" placeholder="请输入数据保存路径" />
        </el-form-item>

        <el-form-item label="图表显示范围">
          <el-select v-model="form.chartRange" placeholder="请选择">
            <el-option label="最近10条" value="10" />
            <el-option label="最近50条" value="50" />
            <el-option label="全部数据" value="all" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="saveSettings">保存设置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const SETTINGS_KEY = 'laser-coupling-settings'

const form = reactive({
  measureInterval: 5,
  savePath: 'D:\\测量数据',
  chartRange: '50'
})

const loadSettings = () => {
  const savedSettings = localStorage.getItem(SETTINGS_KEY)
  if (savedSettings) {
    const settings = JSON.parse(savedSettings)
    Object.assign(form, settings)
  }
}

const saveSettings = () => {
  localStorage.setItem(SETTINGS_KEY, JSON.stringify(form))
  ElMessage.success('设置保存成功')
}

onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
.settings {
  padding: 20px;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.settings-card {
  max-width: 800px;
  margin: 0 auto;
}
</style>