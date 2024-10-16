#!/bin/bash

# 创建项目目录结构
echo "Creating project directories..."
mkdir -p dms

# 进入项目目录
cd dms || exit

# 创建 CSV 数据文件
echo "Creating CSV file..."
cat <<EOL > demand_management.csv
Departments,Products
Sales,Product A
HR,Product B
IT,Product C
EOL

# 创建需求管理系统的 Streamlit 应用代码
echo "Creating Streamlit app file..."
cat <<EOL > demand_management_app.py
import streamlit as st
import pandas as pd

# CSV 文件路径
CSV_FILE = 'demand_management.csv'

# 读取 CSV 文件
def read_csv():
    """Read the CSV file and return the data."""
    return pd.read_csv(CSV_FILE)

# 保存 CSV 文件
def save_csv(df):
    """Save the dataframe to CSV."""
    df.to_csv(CSV_FILE, index=False)

# 动态生成 Tabs，基于 CSV 文件的列
def generate_tabs(df):
    """Generate tabs dynamically based on CSV columns."""
    columns = list(df.columns)  # 将 Pandas Index 转换为列表
    tabs = st.tabs(columns)
    
    for i, col in enumerate(columns):
        with tabs[i]:
            st.subheader(f"Manage {col}")
            
            # 显示当前列的内容
            st.write(df[[col]])

            # 添加新值
            new_value = st.text_input(f"Add new {col} value")
            if st.button(f"Add {col}"):
                # 添加新值到该列
                df.loc[len(df)] = [new_value if c == col else None for c in df.columns]
                save_csv(df)
                # 使用 experimental_rerun 重新运行应用
                st.experimental_rerun()

            # 删除值
            remove_value = st.selectbox(f"Remove {col} value", df[col].dropna())
            if st.button(f"Remove {col}"):
                # 从该列中删除选定的值
                df = df[df[col] != remove_value]
                save_csv(df)
                # 使用 experimental_rerun 重新运行应用
                st.experimental_rerun()

# 报表导出功能
def export_csv(df):
    """Export CSV file for download."""
    st.download_button(
        label="Export to CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='demand_report.csv',
        mime='text/csv'
    )

# 需求查询功能
def query_data(df):
    """Query data from the CSV file."""
    st.subheader("Query Requests")
    query_col = st.selectbox("Select a column to query", df.columns)
    query_value = st.text_input("Enter the value to query")

    if st.button("Search"):
        filtered_df = df[df[query_col] == query_value]
        if not filtered_df.empty:
            st.write(filtered_df)
        else:
            st.write("No matching records found.")

# Streamlit 应用主程序
def main():
    st.title("Demand Management System")
    
    # 读取 CSV 数据
    df = read_csv()

    # 动态生成管理 Tabs
    generate_tabs(df)

    # 需求查询功能
    query_data(df)

    # 导出 CSV 功能
    export_csv(df)

if __name__ == '__main__':
    main()
EOL

# 提示完成
echo "Setup complete. Navigate to the dms directory and run the Streamlit app:"
echo "cd dms"
echo "streamlit run demand_management_app.py"

