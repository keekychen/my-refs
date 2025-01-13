#!/bin/bash

input="=+Uxt"  # 要解密的字符串

echo "Decrypting Caesar cipher for: $input"
for shift in {1..25}; do
  # 构造字母表的位移
  upper=$(echo {A..Z} | sed "s/ //g")
  lower=$(echo {a..z} | sed "s/ //g")
  shifted_upper=$(echo $upper | cut -c$((shift+1))-26)$upper | cut -c1-$shift
  shifted_lower=$(echo $lower | cut -c$((shift+1))-26)$lower | cut -c1-$shift

  # 使用 tr 进行解密
  result=$(echo "$input" | tr "$shifted_upper$shifted_lower" "$upper$lower")
  echo "Shift $shift: $result"
done

