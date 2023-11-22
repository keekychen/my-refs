import pandas as pd
import matplotlib.pyplot as plt

# 创建一个示例 DataFrame
data = {'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Age': [25, 30, 35, 40, 45],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']}
df = pd.DataFrame(data)

# CURD 操作
# 增加数据 - 在 DataFrame 中增加一行
new_row = {'Name': 'Frank', 'Age': 50, 'City': 'Boston'}
df = df.append(new_row, ignore_index=True)

# 修改数据 - 修改第一行的年龄
df.at[0, 'Age'] = 26

# 删除数据 - 删除 Age 列
df_dropped = df.drop(columns=['Age'])

# 插入行 - 在索引 2 的位置插入一行
df.loc[5.5] = {'Name': 'Zoe', 'Age': 32, 'City': 'San Francisco'}
df = df.sort_index().reset_index(drop=True)

# 分组统计（Group By）- 按城市分组并计算每个城市的人数
group_by_city = df.groupby('City').size()

# 数据聚合（Aggregation）- 计算每个城市的最大年龄和最小年龄
age_aggregation = df.groupby('City')['Age'].agg([min, max])

# 数据排序（Sorting）- 根据年龄降序排序
sorted_df = df.sort_values(by='Age', ascending=False)

# 数据过滤（Filtering）- 筛选年龄大于 35 的记录
filtered_df = df[df['Age'] > 35]

# 描述性统计（Descriptive Statistics）- 获取年龄的描述性统计数据
descriptive_stats = df['Age'].describe()

# 缺失值处理（Handling Missing Data）- 人为地创建一些缺失值
df_with_missing = df.copy()
df_with_missing.at[2, 'Age'] = None
# 处理缺失值：用平均年龄填充
df_filled = df_with_missing.fillna(df_with_missing['Age'].mean())

# 数据转换（Data Transformation）- 创建一个新列，根据年龄划分年龄组
df['Age Group'] = pd.cut(df['Age'], bins=[0, 30, 40, 50, 60], labels=['0-30', '31-40', '41-50', '51-60'])

# 使用 matplotlib 绘制图表 - 绘制每个城市的平均年龄的条形图
pivot_table = df.pivot_table(values='Age', index='City', aggfunc='mean')
plt.figure(figsize=(10, 6))
plt.bar(pivot_table.index, pivot_table['Age'])
plt.xlabel('City')
plt.ylabel('Average Age')
plt.title('Average Age per City')
plt.xticks(rotation=45)
plt.show()

# 打印这些操作的结果
df, df_dropped, group_by_city, age_aggregation, sorted_df, filtered_df, descriptive_stats, df_with_missing, df_filled





import pandas as pd
import matplotlib.pyplot as plt

# 创建一个示例 DataFrame
data = {'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Age': [25, 30, 35, 40, 45],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']}
df = pd.DataFrame(data)

# CURD 操作
# 增加数据 - 在 DataFrame 中增加一行
new_row = {'Name': 'Frank', 'Age': 50, 'City': 'Boston'}
df = df.append(new_row, ignore_index=True)

# 修改数据 - 修改第一行的年龄
df.at[0, 'Age'] = 26

# 删除数据 - 删除 Age 列
df_dropped = df.drop(columns=['Age'])

# 插入行 - 在索引 2 的位置插入一行
df.loc[5.5] = {'Name': 'Zoe', 'Age': 32, 'City': 'San Francisco'}
df = df.sort_index().reset_index(drop=True)

# 分组统计（Group By）- 按城市分组并计算每个城市的人数
group_by_city = df.groupby('City').size()

# 数据聚合（Aggregation）- 计算每个城市的最大年龄和最小年龄
age_aggregation = df.groupby('City')['Age'].agg([min, max])

# 数据排序（Sorting）- 根据年龄降序排序
sorted_df = df.sort_values(by='Age', ascending=False)

# 数据过滤（Filtering）- 筛选年龄大于 35 的记录
filtered_df = df[df['Age'] > 35]

# 描述性统计（Descriptive Statistics）- 获取年龄的描述性统计数据
descriptive_stats = df['Age'].describe()

# 缺失值处理（Handling Missing Data）- 人为地创建一些缺失值
df_with_missing = df.copy()
df_with_missing.at[2, 'Age'] = None
# 处理缺失值：用平均年龄填充
df_filled = df_with_missing.fillna(df_with_missing['Age'].mean())

# 数据转换（Data Transformation）- 创建一个新列，根据年龄划分年龄组
df['Age Group'] = pd.cut(df['Age'], bins=[0, 30, 40, 50, 60], labels=['0-30', '31-40', '41-50', '51-60'])

# 使用 matplotlib 绘制图表 - 绘制每个城市的平均年龄的条形图
pivot_table = df.pivot_table(values='Age', index='City', aggfunc='mean')
plt.figure(figsize=(10, 6))
plt.bar(pivot_table.index, pivot_table['Age'])
plt.xlabel('City')
plt.ylabel('Average Age')
plt.title('Average Age per City')
plt.xticks(rotation=45)
plt.show()

# 打印这些操作的结果
df, df_dropped, group_by_city, age_aggregation, sorted_df, filtered_df, descriptive_stats, df_with_missing, df_filled




import pandas as pd

# 1. 创建 DataFrame
data = {'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Age': [25, 30, 35, 40, 45],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']}
df = pd.DataFrame(data)

# 2. 基本查询操作
# 打印整个 DataFrame
print("整个 DataFrame:")
print(df)

# 3. 条件筛选
# 筛选 Age 大于 30 的行
filtered_df = df[df['Age'] > 30]
print("\n年龄大于 30 的行:")
print(filtered_df)

# 4. 增加数据
# 在 DataFrame 中增加一行
new_row = {'Name': 'Frank', 'Age': 50, 'City': 'Boston'}
df = df.append(new_row, ignore_index=True)
print("\n增加一行后的 DataFrame:")
print(df)

# 5. 修改数据
# 修改第一行的年龄
df.at[0, 'Age'] = 26
print("\n修改第一行年龄后的 DataFrame:")
print(df)

# 6. 删除数据
# 删除 Age 列
df_dropped = df.drop(columns=['Age'])
print("\n删除 'Age' 列后的 DataFrame:")
print(df_dropped)

# 7. 操作行和列
# 选取特定的列
selected_columns = df[['Name', 'City']]
print("\n只选取 'Name' 和 'City' 列:")
print(selected_columns)

# 8. 操作单元格
# 修改特定单元格的值
df.at[2, 'City'] = 'Miami'
print("\n修改特定单元格后的 DataFrame:")
print(df)

# 9. 求唯一值
# 获取 'City' 列的唯一值
unique_cities = df['City'].unique()
print("\n'City' 列的唯一值:")
print(unique_cities)

# 10. 合并数据集
# 创建另一个 DataFrame 用于合并
additional_data = {'Name': ['Grace', 'Henry'], 'Age': [28, 33], 'City': ['Seattle', 'Denver']}
additional_df = pd.DataFrame(additional_data)
merged_df = pd.concat([df, additional_df], ignore_index=True)
print("\n合并两个 DataFrame 后:")
print(merged_df)



import matplotlib.pyplot as plt

# 继续使用之前的 DataFrame
# 插入行 - 在索引 2 的位置插入一行
new_data = {'Name': 'Zoe', 'Age': 32, 'City': 'San Francisco'}
df.loc[2.5] = new_data
df = df.sort_index().reset_index(drop=True)

# 生成数据透视表 - 以城市为行，统计每个城市的平均年龄
pivot_table = df.pivot_table(values='Age', index='City', aggfunc='mean')

# 绘制图表 - 绘制每个城市的平均年龄的条形图
plt.figure(figsize=(10, 6))
plt.bar(pivot_table.index, pivot_table['Age'])
plt.xlabel('City')
plt.ylabel('Average Age')
plt.title('Average Age per City')
plt.xticks(rotation=45)
plt.show()

# 打印更新后的 DataFrame 和数据透视表
df, pivot_table


