# 将 CSV 内容作为字符串粘贴到这里
csv_text = """
Name, Age, Country
Alice, 30, USA
Bob, 25, Canada
Charlie, 35, UK
"""

def format_csv_text(csv_text):
    # 将文本按行分割
    lines = csv_text.strip().splitlines()
    # 按逗号分隔每一行，并去除多余的空格
    rows = [line.split(',') for line in lines]
    rows = [[cell.strip() for cell in row] for row in rows]
    
    # 计算每列的最大宽度
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*rows)]

    # 格式化输出为对齐文本
    formatted_text = ""
    for row in rows:
        line = "  ".join(f"{cell:<{col_widths[i]}}" for i, cell in enumerate(row))
        formatted_text += line + "\n"

    return formatted_text

# 格式化输出
aligned_text = format_csv_text(csv_text)
print(aligned_text)


from tabulate import tabulate

# 将 CSV 内容作为字符串粘贴到这里
csv_text = """
Name, Age, Country
Alice, 30, USA
Bob, 25, Canada
Charlie, 35, UK
"""

def format_csv_as_ascii_table(csv_text):
    # 将文本按行分割
    lines = csv_text.strip().splitlines()
    # 按逗号分隔每一行，并去除多余的空格
    rows = [line.split(',') for line in lines]
    rows = [[cell.strip() for cell in row] for row in rows]

    # 第一个列表作为表头，其余作为内容
    headers, *data = rows

    # 使用 tabulate 格式化为 ASCII 表格
    ascii_table = tabulate(data, headers, tablefmt="grid")
    return ascii_table

# 输出 ASCII 表格
ascii_table = format_csv_as_ascii_table(csv_text)
print(ascii_table)

#!/bin/bash

# 将 CSV 内容作为多行字符串粘贴在这里
csv_data="Name,Age,Country
Alice,30,USA
Bob,25,Canada
Charlie,35,UK"

# 使用 awk 将数据格式化为带边框的表格
echo "$csv_data" | awk -F',' '
{
    if(NR==1){
        print "+---------+-----+---------+"
        printf "| %-7s | %-3s | %-7s |\n", $1, $2, $3
        print "+---------+-----+---------+"
    } else {
        printf "| %-7s | %-3s | %-7s |\n", $1, $2, $3
    }
}
END {
    print "+---------+-----+---------+"
}'



#!/bin/bash

# 将 CSV 内容作为多行字符串粘贴在这里
csv_data="Name,Age,Country
Alice,30,USA
Bob,25,Canada
Charlie,35,UK"

# 将 CSV 数据转换为表格格式并打印
echo "$csv_data" | column -t -s,




#!/bin/bash

# 将 CSV 内容作为多行字符串粘贴在这里
csv_data="Name,Age,Country
Alice,30,USA
Bob,25,Canada
Charlie,35,United Kingdom"

# 读取数据并计算每列的最大宽度
IFS=',' # 使用逗号作为分隔符
max_widths=() # 存储每列最大宽度

# 第一遍扫描，找到每列的最大宽度
while IFS=',' read -r -a fields; do
    for i in "${!fields[@]}"; do
        field_length=${#fields[i]}
        if [[ -z ${max_widths[i]} ]] || (( field_length > max_widths[i] )); then
            max_widths[i]=$field_length
        fi
    done
done <<< "$csv_data"

# 输出表格顶部边框
border="+"
for width in "${max_widths[@]}"; do
    border+="$(printf '%0.s-' $(seq 1 $((width + 2))))+"
done
echo "$border"

# 第二遍扫描并格式化输出表格内容
while IFS=',' read -r -a fields; do
    # 输出表格行
    printf "|"
    for i in "${!fields[@]}"; do
        printf " %-*s |" "${max_widths[i]}" "${fields[i]}"
    done
    echo
    # 输出表头下方边框
    if [[ $header_printed -eq 0 ]]; then
        echo "$border"
        header_printed=1
    fi
done <<< "$csv_data"

# 输出表格底部边框
echo "$border"


