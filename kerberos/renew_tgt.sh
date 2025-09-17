#!/bin/bash

KEYTAB_FILE="/path/to/your.keytab"
PRINCIPAL="your_principal@YOUR_REALM"

while true; do
    # 获取 TGT
    kinit -kt "$KEYTAB_FILE" "$PRINCIPAL"
    if [ $? -ne 0 ]; then
        echo "Failed to obtain TGT"
        exit 1
    fi

    while true; do
        # 获取 TGT 过期时间
        EXPIRY_TIME=$(klist | grep "Expires" | awk '{print $3, $4}')
        EXPIRY_TIMESTAMP=$(date -d "$EXPIRY_TIME" +%s)
        CURRENT_TIMESTAMP=$(date +%s)

        # 计算距离过期时间的剩余时间
        REMAINING_TIME=$((EXPIRY_TIMESTAMP - CURRENT_TIMESTAMP))

        # 如果剩余时间少于一小时，则立即续订
        if [ "$REMAINING_TIME" -le 3600 ]; then
            echo "TGT is about to expire in less than an hour, attempting to renew..."
            kinit -R
            if [ $? -eq 0 ]; then
                echo "TGT renewed successfully"
            else
                echo "Failed to renew TGT, exiting..."
                break  # 跳出内层循环，重新获取 TGT
            fi
        else
            # 等待剩余时间的一部分再进行检查
            sleep $((REMAINING_TIME - 3600))  # 续订前一小时检查
        fi
    done
done
