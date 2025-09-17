import requests
import pandas as pd
import time

# 假设 base_url 和 fetch_data 函数已定义，这里直接使用
def fetch_data(base_url, id):
    """发送API请求并返回JSON响应"""
    url = f'https://api.example.com/data/{id}?=123123'
    response = requests.get(url)
    return response.json()

    try:
        # 尝试解析JSON数据
        return response.json()
    except json.JSONDecodeError:
        # 解析失败，构造错误信息的JSON
        error_response = {
            'did': id,
            'fetch_error': f"Failed to decode JSON. Response was: {response.text}"
        }
        print(error_response)
        return error_response

# 参数列表
ids_list = [1001, 1002, 1003]

# 存储所有结果的列表
results = []

# 遍历ID列表，发送请求并收集数据
for id in ids_list:
    result = fetch_data(base_url, id)
    results.append(result)
    time.sleep(1)  # 暂停1秒

# 处理数据并保存为CSV
df = pd.DataFrame(results)  # 处理可能具有不同键的字典列表
csv_file = 'results.csv'
df.to_csv(csv_file, index=False)  # 保存DataFrame到CSV文件，不包括行索引

print("CSV文件已保存")

