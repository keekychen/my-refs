#!/bin/bash

# 配置参数
encrypted_file="encrypted.gpg"  # 要解密的文件
output_file="decrypted.txt"    # 解密后的输出文件
charset="abcdefghijklmnopqrstuvwxyz0123456789"  # 字符集 (小写字母和数字)
max_length=4  # 密码长度（x 位）

# 生成所有可能的密码组合并尝试解密
try_decrypt() {
  local password="$1"

  # 尝试使用当前密码解密
  echo "Trying password: $password"
  gpg --batch --yes --passphrase "$password" --output "$output_file" --decrypt "$encrypted_file" 2>/dev/null

  # 检查解密是否成功
  if [[ $? -eq 0 ]]; then
    echo "Success! Password: $password"
    exit 0
  fi
}

# 递归生成密码
generate_passwords() {
  local current="$1"
  local length="$2"

  if [[ ${#current} -eq $length ]]; then
    try_decrypt "$current"
    return
  fi

  for (( i=0; i<${#charset}; i++ )); do
    generate_passwords "$current${charset:i:1}" "$length"
  done
}

# 开始穷举所有密码
for length in $(seq 1 $max_length); do
  echo "Testing passwords of length $length..."
  generate_passwords "" "$length"
done

echo "Password not found."
exit 1

#abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.


