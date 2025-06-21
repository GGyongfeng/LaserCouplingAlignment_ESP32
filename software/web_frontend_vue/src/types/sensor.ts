// 传感器响应接口定义
export interface SensorData {
  success: boolean
  value: number
}

export interface SensorResponse {
  sensor1: SensorData
  sensor2: SensorData
}