#include "handlers.h"
#include "distance_receiver.h"
#include "cors_utils.h"
#include <stdio.h>  // 添加stdio头文件用于sprintf

esp_err_t get_distance_handler(httpd_req_t *req)
{
    // 读取传感器数据
    DistanceResult result = distance_receiver(10);

    // 构造JSON响应
    char json_buffer[256];
    snprintf(json_buffer, sizeof(json_buffer),
            "{\"sensor1\": {\"success\": %s, \"value\": %.4f}, \"sensor2\": {\"success\": %s, \"value\": %.4f}}",
            result.success1 ? "true" : "false", result.displacement1,
            result.success2 ? "true" : "false", result.displacement2);

    // 设置CORS和JSON响应头
    add_cors_headers(req);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, json_buffer, HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

const httpd_uri_t get_distance = {
    .uri = "/getdistance",
    .method = HTTP_GET,
    .handler = get_distance_handler,
    .user_ctx = NULL
};