#include "handlers.h"
#include "cors_utils.h"

static const char *TAG = "echo_handler";

/**
 * @brief HTTP POST 请求处理函数：接收客户端 POST 的数据并原样返回（Echo Server）
 * 
 * @param req 指向 httpd_req_t 的请求结构体，包含了 HTTP 请求的所有信息（如头、体、连接等）
 * 
 * @return
 *  - ESP_OK：处理成功
 *  - ESP_FAIL：发生错误（读取数据失败）
 * 
 * ✅ 示例请求（curl 命令）：
 * curl -X POST http://<ESP32_IP>/echo -d "Hello, ESP32!"
 * 
 * ✅ 请求体（Request Body）:
 * -----------------------------
 * Hello, ESP32!
 * -----------------------------
 * 
 * ✅ 返回内容（Response Body）:
 * -----------------------------
 * Hello, ESP32!
 * -----------------------------
 */
esp_err_t echo_post_handler(httpd_req_t *req)
{
    char buf[100];                     // 用于接收客户端发来的数据，每次最多接收 100 字节
    int ret;                           // 实际接收到的字节数
    int remaining = req->content_len;  // 还剩多少内容没读，初始为整个 POST 请求体的长度

    while (remaining > 0)
    {
        // 从客户端读取数据（最多读取 buf 大小或剩余长度中较小的部分）
        ret = httpd_req_recv(req, buf, MIN(remaining, sizeof(buf)));

        if (ret <= 0)
        {
            // 如果读取超时则重试
            if (ret == HTTPD_SOCK_ERR_TIMEOUT)
            {
                continue;
            }
            // 如果是其他错误，返回失败
            return ESP_FAIL;
        }

        // 将收到的数据原样返回给客户端（作为响应的一部分）
        httpd_resp_send_chunk(req, buf, ret);

        // 更新剩余长度
        remaining -= ret;

        // 打印收到的数据（用于调试）
        ESP_LOGI(TAG, "=========== RECEIVED DATA ==========");
        ESP_LOGI(TAG, "%.*s", ret, buf);  // 打印实际接收到的数据内容
        ESP_LOGI(TAG, "====================================");
    }

    // 设置CORS头部
    add_cors_headers(req);

    // 发送 NULL 块表示响应结束（Chunked 响应模式）
    httpd_resp_send_chunk(req, NULL, 0);
    return ESP_OK;
}

const httpd_uri_t echo = {
    .uri = "/echo",
    .method = HTTP_POST,
    .handler = echo_post_handler,
    .user_ctx = NULL
};