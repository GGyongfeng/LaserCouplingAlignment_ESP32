#include "freertos/FreeRTOS.h"  // 引入 FreeRTOS 头文件，用于任务管理和调度
#include "freertos/event_groups.h"  // 引入事件组头文件，用于任务间通信
#include "esp_wifi.h"  // 引入 ESP32 WiFi 头文件，用于 WiFi 功能
#include "esp_log.h"  // 引入日志头文件，用于打印日志
#include "esp_event.h"  // 引入事件处理头文件，用于处理 WiFi 事件
#include "nvs_flash.h"  // 引入 NVS 头文件，用于非易失性存储
#include "configs.h"  // 引入配置文件

/* WiFi 事件处理函数 */
#ifndef WIFI_SCAN_H
#define WIFI_SCAN_H

/* 根据配置选择扫描方法 */
#if CONFIG_EXAMPLE_WIFI_ALL_CHANNEL_SCAN
#define DEFAULT_SCAN_METHOD WIFI_ALL_CHANNEL_SCAN  // 全信道扫描
#elif CONFIG_EXAMPLE_WIFI_FAST_SCAN
#define DEFAULT_SCAN_METHOD WIFI_FAST_SCAN  // 快速扫描
#else
#define DEFAULT_SCAN_METHOD WIFI_FAST_SCAN  // 默认使用快速扫描
#endif /*CONFIG_EXAMPLE_SCAN_METHOD*/

/* 根据配置选择连接 AP 的排序方法 */
#if CONFIG_EXAMPLE_WIFI_CONNECT_AP_BY_SIGNAL
#define DEFAULT_SORT_METHOD WIFI_CONNECT_AP_BY_SIGNAL  // 按信号强度排序
#elif CONFIG_EXAMPLE_WIFI_CONNECT_AP_BY_SECURITY
#define DEFAULT_SORT_METHOD WIFI_CONNECT_AP_BY_SECURITY  // 按安全性排序
#else
#define DEFAULT_SORT_METHOD WIFI_CONNECT_AP_BY_SIGNAL  // 默认按信号强度排序
#endif /*CONFIG_EXAMPLE_SORT_METHOD*/

/* 根据配置设置快速扫描的阈值 */
#if CONFIG_EXAMPLE_FAST_SCAN_THRESHOLD
#define DEFAULT_RSSI CONFIG_EXAMPLE_FAST_SCAN_MINIMUM_SIGNAL  // 最小信号强度
#if CONFIG_EXAMPLE_FAST_SCAN_WEAKEST_AUTHMODE_OPEN
#define DEFAULT_AUTHMODE WIFI_AUTH_OPEN  // 最弱认证模式为开放网络
#elif CONFIG_EXAMPLE_FAST_SCAN_WEAKEST_AUTHMODE_WEP
#define DEFAULT_AUTHMODE WIFI_AUTH_WEP  // 最弱认证模式为 WEP
#elif CONFIG_EXAMPLE_FAST_SCAN_WEAKEST_AUTHMODE_WPA
#define DEFAULT_AUTHMODE WIFI_AUTH_WPA_PSK  // 最弱认证模式为 WPA
#elif CONFIG_EXAMPLE_FAST_SCAN_WEAKEST_AUTHMODE_WPA2
#define DEFAULT_AUTHMODE WIFI_AUTH_WPA2_PSK  // 最弱认证模式为 WPA2
#else
#define DEFAULT_AUTHMODE WIFI_AUTH_OPEN  // 默认最弱认证模式为开放网络
#endif
#if CONFIG_SOC_WIFI_SUPPORT_5G
#define DEFAULT_RSSI_5G_ADJUSTMENT CONFIG_EXAMPLE_FAST_SCAN_RSSI_5G_ADJUSTMENT  // 5G 信号强度调整值
#else
#define DEFAULT_RSSI_5G_ADJUSTMENT 0  // 默认 5G 信号强度调整值为 0
#endif
#else
#define DEFAULT_RSSI -127  // 默认信号强度为 -127
#define DEFAULT_AUTHMODE WIFI_AUTH_OPEN  // 默认认证模式为开放网络
#define DEFAULT_RSSI_5G_ADJUSTMENT 0  // 默认 5G 信号强度调整值为 0
#endif /*CONFIG_EXAMPLE_FAST_SCAN_THRESHOLD*/

void wifi_init(void);

// 设置WiFi连接成功的回调函数
void wifi_set_connected_callback(void (*callback)(void));

#endif /* WIFI_SCAN_H */