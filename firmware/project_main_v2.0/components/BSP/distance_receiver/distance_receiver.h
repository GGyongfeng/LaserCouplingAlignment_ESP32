#ifndef DISTANCE_RECEIVER_H
#define DISTANCE_RECEIVER_H

#include <stdbool.h>
#include <string.h>
#include "driver/uart.h"
#include "esp_log.h"

typedef struct {
    bool success1;           // 传感器1读取是否成功
    bool success2;           // 传感器2读取是否成功
    float displacement1;     // 传感器1位移值
    float displacement2;     // 传感器2位移值
} DistanceResult;

/**
 * @brief 单次距离接收器
 * 
 * @param mode 传感器模式：0表示第一个传感器，1表示第二个传感器
 * @param silent 是否静默模式：0表示打印日志，1表示不打印日志
 * @return DistanceResult 包含成功标志和位移值的结构体
 */
DistanceResult single_distance_receiver(int mode);

/**
 * @brief 平均距离接收器
 * 
 * 该函数会调用 single_distance_receiver 函数多次，并计算平均位移值。
 * 
 * @param mode 传感器模式：0表示第一个传感器，1表示第二个传感器
 * @param num_reads 读取次数
 * @return DistanceResult 包含成功标志和平均位移值的结构体
 * 
 * @example
 * DistanceResult result = distance_receiver(0, 10);
 * if (result.success) {
 *     printf("平均位移: %.4f mm\n", result.displacement);
 * } else {
 *     printf("读取失败\n");
 * }
 */
// 更新函数声明，移除mode参数
DistanceResult distance_receiver(int num_reads);

#endif // DISTANCE_RECEIVER_H
