#include "handlers.h"

// 添加查询键的最大长度定义
#define EXAMPLE_HTTP_QUERY_KEY_MAX_LEN (64)

static const char *TAG = "hello_handler";

esp_err_t hello_get_handler(httpd_req_t *req)
{
    // 定义缓冲区指针和长度变量
    char *buf;
    size_t buf_len;

    /* 获取请求头中Host字段的值长度并分配内存
     * 长度加1是为了存储字符串结束符'\0' */
    buf_len = httpd_req_get_hdr_value_len(req, "Host") + 1;
    if (buf_len > 1)  // 如果找到Host头
    {
        // 动态分配内存
        buf = malloc(buf_len);
        // 检查内存分配是否成功，失败则返回内存不足错误
        ESP_RETURN_ON_FALSE(buf, ESP_ERR_NO_MEM, TAG, "buffer alloc failed");
        
        // 获取Host头的具体值
        if (httpd_req_get_hdr_value_str(req, "Host", buf, buf_len) == ESP_OK)
        {
            // 打印Host头的值
            ESP_LOGI(TAG, "Found header => Host: %s", buf);
        }
        // 释放动态分配的内存
        free(buf);
    }

    // 处理Test-Header-2头，逻辑同上
    buf_len = httpd_req_get_hdr_value_len(req, "Test-Header-2") + 1;
    if (buf_len > 1)
    {
        buf = malloc(buf_len);
        ESP_RETURN_ON_FALSE(buf, ESP_ERR_NO_MEM, TAG, "buffer alloc failed");
        if (httpd_req_get_hdr_value_str(req, "Test-Header-2", buf, buf_len) == ESP_OK)
        {
            ESP_LOGI(TAG, "Found header => Test-Header-2: %s", buf);
        }
        free(buf);
    }

    // 处理Test-Header-1头，逻辑同上
    buf_len = httpd_req_get_hdr_value_len(req, "Test-Header-1") + 1;
    if (buf_len > 1)
    {
        buf = malloc(buf_len);
        ESP_RETURN_ON_FALSE(buf, ESP_ERR_NO_MEM, TAG, "buffer alloc failed");
        if (httpd_req_get_hdr_value_str(req, "Test-Header-1", buf, buf_len) == ESP_OK)
        {
            ESP_LOGI(TAG, "Found header => Test-Header-1: %s", buf);
        }
        free(buf);
    }

    /* 读取URL查询字符串的长度并分配内存 */
    buf_len = httpd_req_get_url_query_len(req) + 1;
    if (buf_len > 1)  // 如果URL中包含查询参数
    {
        // 分配内存存储查询字符串
        buf = malloc(buf_len);
        ESP_RETURN_ON_FALSE(buf, ESP_ERR_NO_MEM, TAG, "buffer alloc failed");
        
        // 获取完整的查询字符串
        if (httpd_req_get_url_query_str(req, buf, buf_len) == ESP_OK)
        {
            ESP_LOGI(TAG, "Found URL query => %s", buf);
            // 定义参数缓冲区和解码后的参数缓冲区
            char param[EXAMPLE_HTTP_QUERY_KEY_MAX_LEN], dec_param[EXAMPLE_HTTP_QUERY_KEY_MAX_LEN] = {0};
            
            // 解析query1参数
            if (httpd_query_key_value(buf, "query1", param, sizeof(param)) == ESP_OK)
            {
                ESP_LOGI(TAG, "Found URL query parameter => query1=%s", param);
                // URI解码参数值
                example_uri_decode(dec_param, param, strnlen(param, EXAMPLE_HTTP_QUERY_KEY_MAX_LEN));
                ESP_LOGI(TAG, "Decoded query parameter => %s", dec_param);
            }
            
            // 解析query3参数
            if (httpd_query_key_value(buf, "query3", param, sizeof(param)) == ESP_OK)
            {
                ESP_LOGI(TAG, "Found URL query parameter => query3=%s", param);
                example_uri_decode(dec_param, param, strnlen(param, EXAMPLE_HTTP_QUERY_KEY_MAX_LEN));
                ESP_LOGI(TAG, "Decoded query parameter => %s", dec_param);
            }
            
            // 解析query2参数
            if (httpd_query_key_value(buf, "query2", param, sizeof(param)) == ESP_OK)
            {
                ESP_LOGI(TAG, "Found URL query parameter => query2=%s", param);
                example_uri_decode(dec_param, param, strnlen(param, EXAMPLE_HTTP_QUERY_KEY_MAX_LEN));
                ESP_LOGI(TAG, "Decoded query parameter => %s", dec_param);
            }
        }
        // 释放查询字符串缓冲区
        free(buf);
    }

    /* 设置自定义响应头 */
    httpd_resp_set_hdr(req, "Custom-Header-1", "Custom-Value-1");
    httpd_resp_set_hdr(req, "Custom-Header-2", "Custom-Value-2");

    /* 发送响应
     * 响应内容为处理函数上下文中的字符串 */
    const char *resp_str = (const char *)req->user_ctx;
    httpd_resp_send(req, resp_str, HTTPD_RESP_USE_STRLEN);

    /* 发送HTTP响应后，原始的HTTP请求头信息会丢失
     * 通过尝试读取Host头来验证这一点 */
    if (httpd_req_get_hdr_value_len(req, "Host") == 0)
    {
        ESP_LOGI(TAG, "Request headers lost");
    }
    // 返回成功状态
    return ESP_OK;
}

const httpd_uri_t hello = {
    .uri = "/hello",
    .method = HTTP_GET,
    .handler = hello_get_handler,
    .user_ctx = "Hello World!"
};