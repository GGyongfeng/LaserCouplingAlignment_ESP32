#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "nvs_flash.h"
#include "esp_system.h"
#include "esp_chip_info.h"
#include "esp_psram.h"
#include "esp_flash.h"
#include "driver/uart.h"
#include "driver/gpio.h"
#include "esp_log.h" // 引入ESP日志库
#include "esp_netif.h"
#include "lwip/init.h"
#include <string.h>
#include "esp_http_server.h" // 添加 HTTP 服务器头文件

// 自定义库
#include "distance_receiver.h" // 位移接收器
#include "usart.h"             // uart串口
#include "wdt.h"               // 看门狗
#include "wifi_scan.h"         // wifi扫描
#include "web_server.h"        // web服务器

static const char *TAG = "main"; // 定义日志标签

/**
 * @brief       WiFi连接成功的回调处理函数
 * @details     当WiFi连接成功后，启动Web服务器
 * @param       void - 无参数
 * @return      void - 无返回值
 * @note        使用静态变量server保存Web服务器句柄，避免重复创建
 */
httpd_handle_t server = NULL;

static void wifi_connected_handler(void)
{
    server = start_webserver();
}

/**
 * @brief       程序入口
 * @param       无
 * @retval      无
 */
void app_main(void)
{
    // 定义变量
    esp_err_t ret;

    /* 初始化NVS */
    ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND)
    {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    // 设置WiFi连接成功的回调函数
    wifi_set_connected_callback(wifi_connected_handler);

    // 组件初始化
    wdt_init(5000, 20000000); /* 初始化定时器 超时20秒 */
    usart_init(115200);       /* 初始化串口 */
    wifi_init();              /* 初始化WiFi */

    // 主循环
    while (1) {
        ESP_LOGI(TAG, "Hello world!");
        restart_timer(20000000);
        vTaskDelay(10000 / portTICK_PERIOD_MS);
    }
}
