idf_component_register(SRC_DIRS "handlers" "."
                    INCLUDE_DIRS "." "include"
                    REQUIRES esp_http_server
                            esp_wifi
                            nvs_flash
                            esp_netif
                            protocol_examples_common
                            esp_event
                            esp-tls
                            esp_system
                            BSP
                            spiffs)