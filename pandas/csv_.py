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

