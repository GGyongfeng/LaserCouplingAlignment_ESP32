set(src_dirs
            WDT)

set(include_dirs
            WDT)

set(requires
            driver
            esp_timer
            esp_wifi
            nvs_flash
            json
            spiffs
            bt
            wifi_provisioning
            esp_http_server)

idf_component_register(SRC_DIRS ${src_dirs} INCLUDE_DIRS ${include_dirs} REQUIRES ${requires})

component_compile_options(-ffast-math -O3 -Wno-error=format=-Wno-format)