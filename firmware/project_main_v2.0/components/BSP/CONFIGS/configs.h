#ifndef __CONFIGS_H_
#define __CONFIGS_H_

#include "driver/gpio.h"

/* 引脚和串口定义 */
#define BOOT_GPIO_PIN   GPIO_NUM_0
#define USART1_NUM            UART_NUM_1    /* 一号uart */
#define USART1_TX_GPIO_PIN   GPIO_NUM_17    /* 一号uart TX引脚*/
#define USART1_RX_GPIO_PIN   GPIO_NUM_18    /* 一号uart RX引脚*/
#define USART2_NUM            UART_NUM_2    /* 二号uart */
#define USART2_TX_GPIO_PIN   GPIO_NUM_43
#define USART2_RX_GPIO_PIN   GPIO_NUM_44

/* wifi配置 */
// #define WIFI_SSID "360WiFi-34632B" // 默认 WiFi SSID
// #define WIFI_PWD "88888888"  // 默认 WiFi 密码
#define WIFI_SSID "TP-LINK_204" // 默认 WiFi SSID
#define WIFI_PWD "11235812"  // 默认 WiFi 密码
#define IP_ADDR "192.168.1.10" // 默认 ip 地址
#define WEB_SERVER_PORT 8080 // 默认端口号

// IO操作
#define BOOT            gpio_get_level(BOOT_GPIO_PIN)

#endif