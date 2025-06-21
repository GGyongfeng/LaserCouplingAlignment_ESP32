#include "wifi_scan.h"
#include "esp_netif.h"
#include "lwip/ip4_addr.h"

static const char *TAG = "scan";

// 添加回调函数指针
static void (*wifi_connected_callback)(void) = NULL;

static void event_handler(void *arg, esp_event_base_t event_base,
                          int32_t event_id, void *event_data)
{
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START)
    {
        ESP_LOGI(TAG, "正在连接到 WiFi: %s ...", WIFI_SSID);
        esp_wifi_connect();
    }
    else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_CONNECTED)
    {
        ESP_LOGI(TAG, "WiFi 已连接到: %s，等待获取 IP...", WIFI_SSID);
    }
    else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED)
    {
        ESP_LOGI(TAG, "与 WiFi: %s 的连接断开，尝试重连...", WIFI_SSID);
        esp_wifi_connect();
    }
    else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP)
    {
        ip_event_got_ip_t *event = (ip_event_got_ip_t *)event_data;
        ESP_LOGI(TAG, "IP地址获取成功\nIP:	" IPSTR "\n网关:	" IPSTR "\n子网掩码:	" IPSTR,
                 IP2STR(&event->ip_info.ip), IP2STR(&event->ip_info.gw), IP2STR(&event->ip_info.netmask));
        
        // 在获取到IP后调用回调函数
        if (wifi_connected_callback) {
            wifi_connected_callback();
        }
    }
}

// 添加设置回调函数的接口
void wifi_set_connected_callback(void (*callback)(void))
{
    wifi_connected_callback = callback;
}

void wifi_init(void)
{
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    ESP_ERROR_CHECK(esp_event_handler_instance_register(WIFI_EVENT, ESP_EVENT_ANY_ID, &event_handler, NULL, NULL));
    ESP_ERROR_CHECK(esp_event_handler_instance_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &event_handler, NULL, NULL));

    esp_netif_t *sta_netif = esp_netif_create_default_wifi_sta();
    assert(sta_netif);

    // 配置静态IP
    esp_netif_dhcpc_stop(sta_netif); // 停止DHCP客户端
    esp_netif_ip_info_t ip_info = {0};
    ip_info.ip.addr = esp_ip4addr_aton(IP_ADDR);
    IP4_ADDR(&ip_info.gw, 192, 168, 1, 1);
    IP4_ADDR(&ip_info.netmask, 255, 255, 255, 0);
    esp_err_t err = esp_netif_set_ip_info(sta_netif, &ip_info);
    if (err != ESP_OK)
    {
        ESP_LOGW(TAG, "静态IP设置失败 (错误码 0x%x)，回退到DHCP模式", err);
        esp_netif_dhcpc_start(sta_netif); // 回退到DHCP模式
    }
    else
    {
        ESP_LOGI(TAG, "Static IP configured successfully");
    }

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = WIFI_SSID,
            .password = WIFI_PWD,
            .scan_method = DEFAULT_SCAN_METHOD,
            .sort_method = DEFAULT_SORT_METHOD,
            .threshold.rssi = DEFAULT_RSSI,
            .threshold.authmode = WIFI_AUTH_WPA2_PSK, // 显式指定WPA2
            .threshold.rssi_5g_adjustment = DEFAULT_RSSI_5G_ADJUSTMENT,
        },
    };
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());
}