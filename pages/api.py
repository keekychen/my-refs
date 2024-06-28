import requests
import csv

# 用于发送请求的函数
def fetch_data(base_url, params):
    """发送API请求并返回JSON响应"""
    response = requests.get(base_url, params=params)
    return response.json()

# 基础 URL 和参数列表
base_url = 'https://api.example.com/data'
parameters_list = [{'param1': 'value1', 'param2': 'value2'}, {'param1': 'value3', 'param2': 'value4'}]

# 存储所有结果的列表
results = []

# 遍历参数列表，发送请求并收集数据
for params in parameters_list:
    result = fetch_data(base_url, params)
    results.append(result)

# 将结果写入 CSV 文件
csv_file = 'results.csv'
csv_columns = results[0].keys()  # 假设所有JSON对象都有相同的键

with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in results:
        writer.writerow(data)

print("CSV文件已保存")

