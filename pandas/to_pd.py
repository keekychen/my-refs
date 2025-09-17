import pandas as pd

# 用于存储解析数据的列表
data = []

# 打开并读取文件
with open('ad_groups.txt', 'r') as file:
    group = {}  # 用于存储单个组的信息
    for line in file:
        line = line.strip()
        if not line:  # 如果是空行，跳过处理
            continue
        if line.startswith('Name:'):  # 检测到新组的开始
            if group:  # 如果当前组字典不为空，说明前一个组的数据已经完整
                data.append(group)
                group = {}  # 重置字典以开始新组
        key, value = line.split(': ', 1)  # 分割键和值
        group[key] = value  # 将键值对添加到字典

    # 确保最后一个组的数据也被添加
    if group:
        data.append(group)

# 创建 DataFrame
df = pd.DataFrame(data)
print(df)

