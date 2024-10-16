import os
import gradio as gr
from demand_manager import DemandManager
from datetime import datetime

# Ensure the current working directory exists
try:
    os.getcwd()  # Check if current directory is accessible
except FileNotFoundError:
    print("Current working directory does not exist.")

# Initialize the demand manager
manager = DemandManager()

def add_request(req_name, desc, origin_team, rec_team, product, dependencies, sub_date, exp_date, status, priority):
    """Add a new request and return the updated request table."""
    updated_data = manager.add_request(req_name, desc, origin_team, rec_team, product, ','.join(dependencies), sub_date, exp_date, status, priority)
    # Convert the DataFrame to list format for Gradio Dataframe component
    return updated_data.values.tolist()

def filter_requests(team):
    """Filter requests by team and return the filtered table."""
    filtered_data = manager.filter_requests(team)
    return filtered_data.values.tolist()

def export_requests():
    """Export the request data to a CSV file."""
    return manager.export_to_csv()

def add_department(dept_name):
    """Add a new department and return the updated department list and dropdowns."""
    manager.add_department(dept_name)
    departments = manager.get_departments()
    return [[dept] for dept in departments], departments, departments, departments

def remove_department(dept_name):
    """Remove a department and return the updated department list and dropdowns."""
    manager.remove_department(dept_name)
    departments = manager.get_departments()
    return [[dept] for dept in departments], departments, departments, departments

def add_product(product_name):
    """Add a new product and return the updated product list."""
    manager.add_product(product_name)
    products = manager.get_products()
    return [[product] for product in products], products

def remove_product(product_name):
    """Remove a product and return the updated product list."""
    manager.remove_product(product_name)
    products = manager.get_products()
    return [[product] for product in products], products

# Gradio interface for managing departments and requests
with gr.Blocks() as demo:
    with gr.Tab("Manage Requests"):
        with gr.Row():
            req_name = gr.Textbox(label="Request Name")
            desc = gr.Textbox(label="Description", lines=3)
        with gr.Row():
            origin_team = gr.Dropdown(choices=manager.get_departments(), label="Origin Team")
            rec_team = gr.Dropdown(choices=manager.get_departments(), label="Receiving Team")
            product = gr.Dropdown(choices=manager.get_products(), label="Receiving Team's Product")
        with gr.Row():
            dependencies = gr.Dropdown(choices=manager.get_departments(), label="Dependencies", multiselect=True)
            sub_date = gr.Textbox(label="Submission Date (YYYY-MM-DD)", value=str(datetime.now().date()))
            exp_date = gr.Textbox(label="Expected Completion Date (YYYY-MM-DD)")
        with gr.Row():
            status = gr.Dropdown(choices=["Pending", "In Progress", "Completed"], label="Status")
            priority = gr.Dropdown(choices=["Low", "Medium", "High", "Critical"], label="Priority")
        submit_btn = gr.Button("Submit Request")

        request_table = gr.Dataframe(value=manager.data.values.tolist(), headers=manager.data.columns.tolist(), label="Existing Requests")

        team_filter = gr.Textbox(label="Filter by Receiving Team (optional)", placeholder="Enter team name")
        filter_btn = gr.Button("Filter Requests")
        export_btn = gr.Button("Export to CSV")

        submit_btn.click(fn=add_request,
                         inputs=[req_name, desc, origin_team, rec_team, product, dependencies, sub_date, exp_date, status, priority],
                         outputs=request_table)

        filter_btn.click(fn=filter_requests, inputs=team_filter, outputs=request_table)

        export_btn.click(fn=export_requests, outputs=gr.File(label="Download CSV"))

    with gr.Tab("Manage Departments"):
        dept_name = gr.Textbox(label="Department Name")
        add_dept_btn = gr.Button("Add Department")
        remove_dept_btn = gr.Button("Remove Department")
        department_table = gr.Dataframe(value=[[dept] for dept in manager.get_departments()], headers=["Department"], label="Current Departments")

        add_dept_btn.click(fn=add_department, inputs=dept_name, outputs=[department_table, origin_team, rec_team, dependencies])
        remove_dept_btn.click(fn=remove_department, inputs=dept_name, outputs=[department_table, origin_team, rec_team, dependencies])

    with gr.Tab("Manage Products"):
        product_name = gr.Textbox(label="Product Name")
        add_prod_btn = gr.Button("Add Product")
        remove_prod_btn = gr.Button("Remove Product")
        product_table = gr.Dataframe(value=[[prod] for prod in manager.get_products()], headers=["Product"], label="Current Products")

        add_prod_btn.click(fn=add_product, inputs=product_name, outputs=[product_table, product])
        remove_prod_btn.click(fn=remove_product, inputs=product_name, outputs=[product_table, product])

# Launch the Gradio app with sharing enabled
demo.launch(share=True)
