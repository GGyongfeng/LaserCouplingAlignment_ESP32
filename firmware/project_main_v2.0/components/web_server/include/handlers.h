#ifndef _HTTP_HANDLERS_H_
#define _HTTP_HANDLERS_H_

// 包含标准C库的头文件
#include <string.h>    // 字符串操作相关函数
#include <stdlib.h>    // 标准库函数
#include <unistd.h>    // POSIX操作系统API
#include <esp_log.h>   // ESP32日志功能
#include <nvs_flash.h> // 非易失性存储（NVS）功能
#include <sys/param.h> // 系统参数定义

// 包含ESP-IDF特定的头文件
#include "esp_netif.h"                // 网络接口抽象层
#include "protocol_examples_common.h" // 协议示例公共函数
#include "protocol_examples_utils.h"  // 协议示例工具函数
#include "esp_tls_crypto.h"           // TLS加密功能
#include <esp_http_server.h>          // HTTP服务器功能
#include "esp_event.h"                // 事件处理系统
#include "esp_tls.h"                  // TLS功能
#include "esp_check.h"                // ESP检查宏

// 声明所有处理函数
esp_err_t hello_get_handler(httpd_req_t *req);
esp_err_t echo_post_handler(httpd_req_t *req);
esp_err_t get_distance_handler(httpd_req_t *req);
esp_err_t ctrl_put_handler(httpd_req_t *req);
esp_err_t http_404_error_handler(httpd_req_t *req, httpd_err_code_t err);

// 声明 URI 结构体
extern const httpd_uri_t hello;
extern const httpd_uri_t echo;
extern const httpd_uri_t ctrl;
extern const httpd_uri_t get_distance;

#endif // _HTTP_HANDLERS_H_