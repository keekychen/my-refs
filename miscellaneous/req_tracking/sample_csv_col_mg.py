import os
import gradio as gr
import pandas as pd

# CSV 文件路径
CSV_FILE = "data.csv"

# 读取 CSV 文件
def read_csv():
    """Read the CSV file and return the data."""
    return pd.read_csv(CSV_FILE)

# 更新 CSV 文件
def update_csv(df):
    """Update the CSV file with new data."""
    df.to_csv(CSV_FILE, index=False)

# 获取列的值
def get_column_values(column_name):
    """Return the list of values in the specified column."""
    df = read_csv()
    return df[column_name].dropna().tolist()

# 通用的添加函数
def add_value(column_name, value):
    """Add a new value to the specified column and update the CSV."""
    df = read_csv()
    if value not in df[column_name].values:
        new_row = {col: None for col in df.columns}
        new_row[column_name] = value
        df = df.append(new_row, ignore_index=True)
        update_csv(df)
    return [[v] for v in df[column_name].dropna().tolist()]

# 通用的删除函数
def remove_value(column_name, value):
    """Remove a value from the specified column and update the CSV."""
    df = read_csv()
    df = df[df[column_name] != value]
    update_csv(df)
    return [[v] for v in df[column_name].dropna().tolist()]

# 动态生成的 Gradio 界面
def generate_dynamic_ui():
    with gr.Blocks() as demo:
        df = read_csv()
        columns = df.columns.tolist()

        # 为每一个列创建一个Tab
        for column in columns:
            with gr.Tab(f"Manage {column}"):
                value_input = gr.Textbox(label=f"Add new {column} value")
                add_btn = gr.Button(f"Add {column}")
                remove_input = gr.Dropdown(choices=get_column_values(column), label=f"Remove {column} value")
                remove_btn = gr.Button(f"Remove {column}")
                value_table = gr.Dataframe(value=[[v] for v in get_column_values(column)], headers=[column], label=f"Current {column} values")

                # 事件绑定：添加新值
                add_btn.click(fn=add_value, inputs=[column, value_input], outputs=value_table)

                # 事件绑定：删除值
                remove_btn.click(fn=remove_value, inputs=[column, remove_input], outputs=value_table)

    return demo

# 启动 Gradio 应用
app = generate_dynamic_ui()
app.launch()

