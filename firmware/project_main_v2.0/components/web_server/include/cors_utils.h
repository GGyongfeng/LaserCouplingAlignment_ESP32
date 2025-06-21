#ifndef _CORS_UTILS_H_
#define _CORS_UTILS_H_

#include <esp_http_server.h>

/**
 * @brief 为HTTP响应添加CORS（跨域资源共享）头部
 * 
 * @param req HTTP请求结构体
 */
static inline void add_cors_headers(httpd_req_t *req)
{
    httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
    httpd_resp_set_hdr(req, "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
    httpd_resp_set_hdr(req, "Access-Control-Allow-Headers", "Content-Type");
}

#endif // _CORS_UTILS_H_