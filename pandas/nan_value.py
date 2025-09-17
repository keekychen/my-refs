import pandas as pd
import numpy as np

# 创建示例数据
data1 = {
    'A': [1, 2, 3, 4],
    'B': ['a', 'b', 'c', None]
}
df1 = pd.DataFrame(data1)

data2 = {
    'A': [3, 4, 5, 6],
    'C': [None, 'd', 'e', 'f']
}
df2 = pd.DataFrame(data2)

# 合并两个 DataFrame，使用外连接保留所有数据
merged_df = pd.merge(df1, df2, on='A', how='outer')
print("Merged DataFrame:")
print(merged_df)

# 删除含有空值的行
cleaned_df = merged_df.dropna()
print("\nDataFrame after dropping rows with NaNs:")
print(cleaned_df)

# 填充固定值
filled_df = merged_df.fillna(value=0)
print("\nDataFrame after filling NaNs with zero:")
print(filled_df)

# 用前一个值填充空值
forward_filled_df = merged_df.fillna(method='ffill')
print("\nDataFrame after forward filling NaNs:")
print(forward_filled_df)

# 用列的平均值填充（仅适用于数值列）
if merged_df['A'].dtype in ['float64', 'int64']:
    merged_df['A'] = merged_df['A'].fillna(merged_df['A'].mean())
print("\nDataFrame after filling NaNs with mean values in column 'A':")
print(merged_df)

# 插值填充（假设适用于数字类型）
interpolated_df = merged_df.interpolate(method='linear')
print("\nDataFrame after interpolation of NaNs:")
print(interpolated_df)

# 使用条件逻辑填充，这里使用numpy的where方法
# 假设我们知道列C的NaN应该用字符串'unknown'填充
merged_df['C'] = np.where(pd.isna(merged_df['C']), 'unknown', merged_df['C'])
print("\nDataFrame after conditional filling of NaNs in column 'C':")
print(merged_df)
