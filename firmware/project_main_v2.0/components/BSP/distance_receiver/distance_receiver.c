#include "distance_receiver.h"
#include "usart.h" // 引入usart头文件

static const char *TAG = "distance_receiver"; // 定义日志标签

DistanceResult single_distance_receiver(int mode)
{
    // 参数mode：为0时读取第一个传感器的数据，为1时读取第二个传感器的数据
    uint8_t send_data[8];
    if (mode == 0)
    {
        uint8_t temp_data[] = {0x01, 0x03, 0x00, 0x10, 0x00, 0x02, 0xC5, 0xCE};
        memcpy(send_data, temp_data, sizeof(temp_data));
        // ESP_LOGI(TAG, "准备发送数据到传感器1，数据内容：");
    }
    else
    {
        uint8_t temp_data[] = {0x02, 0x03, 0x00, 0x10, 0x00, 0x02, 0xC5, 0xFD};
        memcpy(send_data, temp_data, sizeof(temp_data));
        // ESP_LOGI(TAG, "准备发送数据到传感器2，数据内容：");
    }
    // 打印发送数据的内容
    // for (int i = 0; i < 8; i++) {
    //     printf("%02X ", send_data[i]);
    // }
    // printf("\n");

    // 在发送前清空接收缓冲区
    uart_flush(USART1_NUM);

    // 发送数据并等待一段时间确保数据完全发送
    uart_write_bytes(USART1_NUM, send_data, sizeof(send_data));
    // ESP_LOGI(TAG, "发送字节数: %d", written_bytes);
    vTaskDelay(2 / portTICK_PERIOD_MS); // 减少等待时间至2ms

    // 接收数据
    uint8_t recv_data[BUF_SIZE];    // 接收缓冲区
    memset(recv_data, 0, BUF_SIZE); // 对缓冲区清零

    size_t len = 0;
    int retry_count = 0;
    const int max_retries = 3;

    while (retry_count < max_retries)
    {
        uart_get_buffered_data_len(USART1_NUM, &len);
        // ESP_LOGI(TAG, "重试次数: %d, 当前缓冲区数据长度: %d", retry_count, len);

        if (len > 0)
        { // 只要有数据就先读出来
            size_t read_len = len > BUF_SIZE ? BUF_SIZE : len;
            len = uart_read_bytes(USART1_NUM, recv_data, read_len, 200 / portTICK_PERIOD_MS);

            // 打印接收到的数据内容
            // ESP_LOGI(TAG, "接收数据内容: ");
            // for (int i = 0; i < len; i++) {
            //     printf("%02X ", recv_data[i]);
            // }
            // printf("\n");

            // 检查数据是否完整且有效
            if (len >= 9 && recv_data[0] == (mode == 0 ? 0x01 : 0x02) && recv_data[1] == 0x03)
            {
                break;
            }
        }
        vTaskDelay(10 / portTICK_PERIOD_MS); // 增加等待时间
        retry_count++;
    }

    if (len < 9)
    {
        ESP_LOGE(TAG, "single_distance_receiver--未接收到任何数据或数据不完整");
    }

    DistanceResult result = {0}; // 初始化所有成员为0
    // 处理数据
    if (len >= 9 && recv_data[0] == (mode == 0 ? 0x01 : 0x02) && recv_data[1] == 0x03)
    {
        uint32_t value = (recv_data[3] << 24) | (recv_data[4] << 16) | (recv_data[5] << 8) | recv_data[6];
        if (mode == 0)
        {
            result.displacement1 = (float)value / 10000.0;
            result.success1 = true;
            result.success2 = false;
            result.displacement2 = -1.0;
        }
        else
        {
            result.displacement2 = (float)value / 10000.0;
            result.success2 = true;
            result.success1 = false;
            result.displacement1 = -1.0;
        }
    }
    else
    {
        ESP_LOGE(TAG, "接收到无效数据：");
        ESP_LOGE(TAG, "数据长度: %d", len);
        ESP_LOGE(TAG, "数据内容: ");
        for (int i = 0; i < len; i++)
        {
            printf("%02X ", recv_data[i]);
        }
        printf("\n");
        if (mode == 0)
        {
            result.success1 = false;
            result.displacement1 = -1.0;
            result.success2 = false;
            result.displacement2 = -1.0;
        }
        else
        {
            result.success2 = false;
            result.displacement2 = -1.0;
            result.success1 = false;
            result.displacement1 = -1.0;
        }
    }
    return result;
}

DistanceResult distance_receiver(int num_reads)
{
    float total_displacement1 = 0.0;
    float total_displacement2 = 0.0;
    int successful_reads1 = 0;
    int successful_reads2 = 0;

    ESP_LOGI(TAG, "开始多次读取两个传感器, 次数: %d", num_reads);

    for (int i = 0; i < num_reads; i++)
    {
        // 读取传感器1
        DistanceResult result1 = single_distance_receiver(0);
        if (result1.success1)
        {
            total_displacement1 += result1.displacement1;
            successful_reads1++;
        }
        vTaskDelay(3 / portTICK_PERIOD_MS); // 减少两次读取之间的延时至3ms

        // 读取传感器2
        DistanceResult result2 = single_distance_receiver(1);
        if (result2.success2)
        {
            total_displacement2 += result2.displacement2;
            successful_reads2++;
        }
        vTaskDelay(3 / portTICK_PERIOD_MS); // 减少延时至3ms
    }

    DistanceResult final_result;

    // 处理传感器1结果
    if (successful_reads1 > 0)
    {
        final_result.success1 = true;
        final_result.displacement1 = total_displacement1 / successful_reads1;
        ESP_LOGI(TAG, "传感器1读取完成，平均位移: %.4f mm", final_result.displacement1);
    }
    else
    {
        final_result.success1 = false;
        final_result.displacement1 = -1.0;
        ESP_LOGE(TAG, "传感器1读取失败，未能成功读取任何数据");
    }

    // 处理传感器2结果
    if (successful_reads2 > 0)
    {
        final_result.success2 = true;
        final_result.displacement2 = total_displacement2 / successful_reads2;
        ESP_LOGI(TAG, "传感器2读取完成，平均位移: %.4f mm", final_result.displacement2);
    }
    else
    {
        final_result.success2 = false;
        final_result.displacement2 = -1.0;
        ESP_LOGE(TAG, "传感器2读取失败，未能成功读取任何数据");
    }

    return final_result;
}