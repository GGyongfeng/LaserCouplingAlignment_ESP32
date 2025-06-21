#ifndef WEB_SERVER_H
#define WEB_SERVER_H

#include <esp_err.h>
#include <esp_event.h>
#include <esp_http_server.h>

// 针对非Linux目标的特定包含
#if !CONFIG_IDF_TARGET_LINUX
#include <esp_wifi.h>   // WiFi功能
#include <esp_system.h> // ESP系统功能
#include "nvs_flash.h"  // NVS闪存
#endif

// 定义HTTP查询键的最大长度
#define EXAMPLE_HTTP_QUERY_KEY_MAX_LEN (64)

// 启动Web服务器并返回服务器句柄
httpd_handle_t start_webserver(void);

// // 停止Web服务器
#if !CONFIG_IDF_TARGET_LINUX
esp_err_t stop_webserver(httpd_handle_t server);

// 断开连接事件处理程序
void disconnect_handler(void *arg, esp_event_base_t event_base, int32_t event_id, void *event_data);
// 连接事件处理程序
void connect_handler(void *arg, esp_event_base_t event_base, int32_t event_id, void *event_data);
#endif // !CONFIG_IDF_TARGET_LINUX

#endif // WEB_SERVER_H