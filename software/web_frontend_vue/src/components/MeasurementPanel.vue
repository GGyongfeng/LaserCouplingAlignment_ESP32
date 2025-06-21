<template>
  <div class="measurement-panel">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>传感器测量数据</h3>
          <div class="button-group">
            <el-button type="primary" @click="startMeasure" :loading="measuring">测量</el-button>
            <el-button :type="autoMeasuring ? 'danger' : 'primary'" @click="toggleAutoMeasure">
              {{ autoMeasuring ? '停止自动测量' : '自动测量' }}
            </el-button>
          </div>
        </div>
      </template>

      <!-- 传感器数据显示 -->
      <div class="sensor-data">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card shadow="hover">
              <template #header>轴向激光传感器</template>
              <div class="sensor-value" :class="{ 'error': !sensor1Status }">
                {{ sensor1Value }}
              </div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card shadow="hover">
              <template #header>径向激光传感器</template>
              <div class="sensor-value" :class="{ 'error': !sensor2Status }">
                {{ sensor2Value }}
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 图表显示 -->
      <div class="chart-section">
        <div class="chart-header">
          <div class="chart-title">测量数据图表</div>
          <div class="title-buttons">
            <el-button @click="clearData" size="small">清零</el-button>
            <el-button type="success" @click="exportData" size="small">导出数据</el-button>
          </div>
        </div>
        <div class="chart-container" ref="chartRef"></div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { measureSensors } from '@/api/sensor'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'
import { ElMessageBox } from 'element-plus'

// 状态变量
const measuring = ref(false)
const autoMeasuring = ref(false)
const sensor1Value = ref('--')
const sensor2Value = ref('--')
const sensor1Status = ref(true)
const sensor2Status = ref(true)
const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null
let autoMeasureInterval: number | null = null

// 数据存储
const measureData = ref<Array<{ time: string; sensor1: number; sensor2: number }>>(
  JSON.parse(localStorage.getItem('SENSOR_DATA') || '[]')
);

// 初始化图表
const initChart = () => {
  if (chartRef.value) {
    chart = echarts.init(chartRef.value)
    const option: EChartsOption = {
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: ['轴向激光传感器', '径向激光传感器']
      },
      xAxis: {
        type: 'category',
        data: []
      },
      yAxis: [
        {
          type: 'value',
          name: '轴向距离(mm)',
          position: 'left',
          scale: true
        },
        {
          type: 'value',
          name: '径向距离(mm)',
          position: 'right',
          scale: true,
          offset: 0
        }
      ],
      series: [
        {
          name: '轴向激光传感器',
          type: 'line',
          yAxisIndex: 0,
          data: []
        },
        {
          name: '径向激光传感器',
          type: 'line',
          yAxisIndex: 1,
          data: []
        }
      ]
    }
    chart.setOption(option)
  }
}

// 更新图表数据
const updateChart = () => {
  if (!chart) return

  const times = measureData.value.map(item => item.time)
  const sensor1Data = measureData.value.map(item => item.sensor1)
  const sensor2Data = measureData.value.map(item => item.sensor2)

  chart.setOption({
    xAxis: {
      data: times
    },
    series: [
      {
        data: sensor1Data
      },
      {
        data: sensor2Data
      }
    ]
  })
}

// 开始测量
const startMeasure = async () => {
  measuring.value = true
  try {
    const { data: { sensor1, sensor2 } } = await measureSensors().catch(error => {
      if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
        ElMessageBox.alert('设备未连接或网络超时\n请检查网络设置', '连接错误', {
          confirmButtonText: '确定',
          type: 'error'
        })
        throw error
      }
      throw error
    })
    console.log('完整响应结构:', { sensor1, sensor2 })

    // 验证响应数据结构
    if (!sensor1 || !sensor2) {
      console.error('无效的传感器数据结构:', { sensor1, sensor2 })
      throw new Error('接口响应格式错误')
    }

    // 更新传感器1状态和数值
    sensor1Status.value = sensor1.success
    sensor1Value.value = sensor1.success ?
      (sensor1.value === 0 ? '超出范围' : sensor1.value.toFixed(4)) :
      '设备故障'

    // 更新传感器2状态和数值
    sensor2Status.value = sensor2.success
    sensor2Value.value = sensor2.success ?
      (sensor2.value === 0 ? '超出范围' : sensor2.value.toFixed(4)) :
      '设备故障'

    // 记录数据
    if (sensor1.success && sensor2.success) {
      measureData.value.push({
        time: new Date().toLocaleTimeString(),
        sensor1: sensor1.value,
        sensor2: sensor2.value
      })
      localStorage.setItem('SENSOR_DATA', JSON.stringify(measureData.value));
      updateChart()
    }
  } catch (error: unknown) {
    const axiosError = error as { code?: string; message?: string; isAxiosError?: boolean };
    console.error('测量失败:', error)
    if (axiosError.isAxiosError !== true) {
      ElMessageBox.alert('设备通信异常，请检查连接状态', '测量错误', {
        confirmButtonText: '确定',
        type: 'error'
      })
    }
  } finally {
    measuring.value = false
  }
}

// 清零数据
const clearData = () => {
  measureData.value = [];
  localStorage.removeItem('SENSOR_DATA');
  sensor1Value.value = '--'
  sensor2Value.value = '--'
  updateChart()
}

// 导出数据
const exportData = () => {
  if (measureData.value.length === 0) {
    return
  }

  const csvContent = ['时间,轴向激光传感器,径向激光传感器']
  measureData.value.forEach(record => {
    csvContent.push(`${record.time},${record.sensor1},${record.sensor2}`)
  })

  const blob = new Blob([csvContent.join('\n')], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `sensor_data_${new Date().toISOString().slice(0, 10)}.csv`
  link.click()
}

// 自动测量相关
const toggleAutoMeasure = () => {
  if (autoMeasuring.value) {
    stopAutoMeasure()
  } else {
    showAutoMeasureDialog()
  }
}

const showAutoMeasureDialog = () => {
  ElMessageBox.prompt('请输入测量间隔时间（秒）', {
    title: '自动测量设置',
    inputPattern: /^[0-9]+$/,
    inputErrorMessage: '请输入有效的数字',
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    inputType: 'number',
    inputValue: '5',
    inputValidator: (value) => {
      const num = Number(value)
      return num > 0 && num <= 3600
    }
  }).then(({ value }) => {
    startAutoMeasure(Number(value))
  }).catch(() => { })
}

const startAutoMeasure = (interval: number) => {
  autoMeasuring.value = true
  autoMeasureInterval = window.setInterval(async () => {
    await startMeasure()
  }, interval * 1000)
}

const stopAutoMeasure = () => {
  if (autoMeasureInterval) {
    clearInterval(autoMeasureInterval)
    autoMeasureInterval = null
  }
  autoMeasuring.value = false
}

// 生命周期钩子
onMounted(() => {
  initChart()
  window.addEventListener('resize', () => chart?.resize())
})

onUnmounted(() => {
  stopAutoMeasure()
  chart?.dispose()
  window.removeEventListener('resize', () => chart?.resize())
})
</script>

<style scoped>
.measurement-panel {
  padding: 10px;
}

.card-header {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.title-group {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.card-header h3 {
  margin: 0;
}

.title-buttons {
  display: flex;
  gap: 10px;
}

.button-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.sensor-data {
  margin: 15px 0;
}

.sensor-value {
  font-size: 20px;
  text-align: center;
  padding: 15px;
}

.sensor-value.error {
  color: #f56c6c;
}

.chart-section {
  margin-top: 15px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.chart-title {
  font-size: 16px;
  font-weight: 500;
}

.title-buttons {
  display: flex;
  gap: 10px;
}

.chart-container {
  height: 300px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

@media screen and (min-width: 768px) {
  .measurement-panel {
    padding: 20px;
  }

  .card-header {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }

  .button-group {
    justify-content: flex-end;
  }

  .sensor-value {
    font-size: 24px;
    padding: 20px;
  }

  .chart-container {
    height: 400px;
    margin-top: 20px;
  }
}
</style>