import pandas as pd

# 创建第一个 DataFrame
data1 = {
    'A': [1, 2, 3, 4],
    'B': ['a', 'b', 'c', 'd'],
    'C': ['W', 'X', 'Y', 'Z']
}
df1 = pd.DataFrame(data1)

# 创建第二个 DataFrame
data2 = {
    'A': [3, 4, 5, 6],
    'B': ['c', 'd', 'e', 'f'],
    'D': ['V', 'W', 'X', 'Y']
}
df2 = pd.DataFrame(data2)

# 并集：使用 how='outer' 来包含两个 DataFrame 中的所有行
union_df = pd.merge(df1, df2, on=['A', 'B'], how='outer')
print("Union of df1 and df2:")
print(union_df)
print("\n")  # 添加空行以便更好的阅读输出

# 交集：使用 how='inner' 只包含两个 DataFrame 中都有的行
intersection_df = pd.merge(df1, df2, on=['A', 'B'], how='inner')
print("Intersection of df1 and df2:")
print(intersection_df)
print("\n")

# 补集：使用 how='left' 和 indicator=True 找出 df1 中独有的行
complement_df1 = pd.merge(df1, df2, on=['A', 'B'], how='left', indicator=True)
complement_df1 = complement_df1[complement_df1['_merge'] == 'left_only'].drop(columns=['_merge', 'D'])
print("Complement of df1 relative to df2:")
print(complement_df1)
print("\n")

# 补集：使用 how='right' 和 indicator=True 找出 df2 中独有的行
complement_df2 = pd.merge(df1, df2, on=['A', 'B'], how='right', indicator=True)
complement_df2 = complement_df2[complement_df2['_merge'] == 'right_only'].drop(columns=['_merge', 'C'])
print("Complement of df2 relative to df1:")
print(complement_df2)

