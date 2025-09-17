#!/bin/bash

# 凯撒加密/解密函数
caesar_cipher() {
  local input="$1"   # 输入的字符串
  local shift="$2"   # 偏移量
  local mode="$3"    # 模式：encrypt 或 decrypt
  local result=""
  
  # 如果是解密，偏移量取反
  [[ "$mode" == "decrypt" ]] && shift=$((26 - shift))
  
  # 构造字母表
  local upper="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  local lower="abcdefghijklmnopqrstuvwxyz"
  local shifted_upper="${upper:$shift}${upper:0:$shift}"
  local shifted_lower="${lower:$shift}${lower:0:$shift}"
  
  # 使用 tr 进行替换
  result=$(echo "$input" | tr "$upper$lower" "$shifted_upper$shifted_lower")
  echo "$result"
}

# 穷举所有偏移量
caesar_bruteforce() {
  local input="$1"  # 输入的加密字符串
  echo "Bruteforce decryption for: $input"
  
  for shift in {1..25}; do
    local decrypted=$(caesar_cipher "$input" "$shift" "decrypt")
    echo "Shift $shift: $decrypted"
  done
}

# 示例用法
input="Uxt"  # 加密字符串
echo "Original string: $input"

# 加密示例
shift=5
encrypted=$(caesar_cipher "$input" "$shift" "encrypt")
echo "Encrypted (shift $shift): $encrypted"

# 解密示例
decrypted=$(caesar_cipher "$encrypted" "$shift" "decrypt")
echo "Decrypted (shift $shift): $decrypted"

# 穷举所有解密方式
caesar_bruteforce "$encrypted"

