#include "handlers.h"
#include "cors_utils.h"

esp_err_t http_404_error_handler(httpd_req_t *req, httpd_err_code_t err)
{
    // 设置CORS头部
    add_cors_headers(req);

    // 如果客户端请求的是 /hello
    if (strcmp("/hello", req->uri) == 0)
    {
        // 向客户端返回自定义 404 错误信息
        httpd_resp_send_err(req, HTTPD_404_NOT_FOUND, "/hello URI is not available");
        // 返回 ESP_OK，保持 socket 打开
        return ESP_OK;
    }
    // 如果客户端请求的是 /echo
    else if (strcmp("/echo", req->uri) == 0)
    {
        // 向客户端返回自定义 404 错误信息
        httpd_resp_send_err(req, HTTPD_404_NOT_FOUND, "/echo URI is not available");
        // 返回 ESP_FAIL，通知服务器关闭 socket
        return ESP_FAIL;
    }

    // 其它未定义的 URI，统一返回 404 并关闭连接
    httpd_resp_send_err(req, HTTPD_404_NOT_FOUND, "Some 404 error message");
    return ESP_FAIL;
}