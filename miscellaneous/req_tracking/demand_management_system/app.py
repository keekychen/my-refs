import os
import gradio as gr
from demand_manager import DemandManager
from datetime import datetime

# Initialize the demand manager
manager = DemandManager()

def select_request(index):
    """Populate the selected request details into the input fields for modification."""
    index = int(index) - 1  # Adjust for 1-based index
    if index >= 0 and index < len(manager.data):
        req = manager.data.iloc[index]
        return (
            req["Request Name"], req["Description"], req["Origin Team"],
            req["Receiving Team"], req["Product"], req["Dependencies"].split(","),
            req["Submission Date"], req["Expected Completion Date"], req["Status"], req["Priority"]
        )
    return None, None, None, None, None, None, None, None, None, None

def add_request(req_name, desc, origin_team, rec_team, product, dependencies, sub_date, exp_date, status, priority):
    """Add or modify a request and return the updated request table."""
    updated_data = manager.add_request(req_name, desc, origin_team, rec_team, product, ','.join(dependencies), sub_date, exp_date, status, priority)
    return updated_data

def filter_requests(team):
    """Filter requests by team name using fuzzy matching."""
    filtered_data = manager.data[manager.data["Receiving Team"].str.contains(team, case=False, na=False)]
    return filtered_data

def export_requests():
    """Export the request data to a CSV file."""
    return manager.export_to_csv()

def add_department(dept_name):
    """Add a new department and return the updated department list and dropdowns."""
    manager.add_department(dept_name)
    departments = manager.get_departments()
    return manager.departments, gr.Dropdown.update(choices=departments), gr.Dropdown.update(choices=departments), gr.Dropdown.update(choices=departments)

def remove_department(dept_name):
    """Remove a department and return the updated department list and dropdowns."""
    manager.remove_department(dept_name)
    departments = manager.get_departments()
    return manager.departments, gr.Dropdown.update(choices=departments), gr.Dropdown.update(choices=departments), gr.Dropdown.update(choices=departments)

def add_product(product_name):
    """Add a new product and return the updated product list."""
    manager.add_product(product_name)
    products = manager.get_products()
    return manager.products, gr.Dropdown.update(choices=products)

def remove_product(product_name):
    """Remove a product and return the updated product list."""
    manager.remove_product(product_name)
    products = manager.get_products()
    return manager.products, gr.Dropdown.update(choices=products)

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
            # Multi-select dropdown for dependencies
            dependencies = gr.Dropdown(choices=manager.get_departments(), label="Dependencies", multiselect=True)
            # Use Textbox for date input, default format YYYY-MM-DD
            sub_date = gr.Textbox(label="Submission Date (YYYY-MM-DD)", value=str(datetime.now().date()))
            exp_date = gr.Textbox(label="Expected Completion Date (YYYY-MM-DD)")
        with gr.Row():
            status = gr.Dropdown(choices=["Pending", "In Progress", "Completed"], label="Status")
            priority = gr.Dropdown(choices=["Low", "Medium", "High", "Critical"], label="Priority")
        submit_btn = gr.Button("Submit Request")

        # Table to display all requests
        request_table = gr.DataFrame(value=manager.data, label="Existing Requests", headers="auto")
        
        # Dropdown to select record for modification
        record_index = gr.Number(label="Select Request Index (1-based)", value=1, precision=0)
        select_btn = gr.Button("Select Request")
        select_btn.click(select_request, inputs=record_index, outputs=[req_name, desc, origin_team, rec_team, product, dependencies, sub_date, exp_date, status, priority])
        
        # Filter requests by team with fuzzy matching
        team_filter = gr.Textbox(label="Filter by Receiving Team (optional)", placeholder="Enter team name")
        filter_btn = gr.Button("Filter Requests")
        filter_btn.click(filter_requests, inputs=team_filter, outputs=request_table)

        export_btn = gr.Button("Export to CSV")
        export_btn.click(fn=export_requests, outputs=gr.File(label="Download CSV"))

    with gr.Tab("Manage Departments"):
        dept_name = gr.Textbox(label="Department Name")
        add_dept_btn = gr.Button("Add Department")
        remove_dept_btn = gr.Button("Remove Department")
        department_table = gr.DataFrame(value=manager.departments, label="Current Departments", headers="auto")

        # Event handlers for department management
        add_dept_btn.click(fn=add_department, inputs=dept_name, outputs=[department_table, origin_team, rec_team, dependencies])
        remove_dept_btn.click(fn=remove_department, inputs=dept_name, outputs=[department_table, origin_team, rec_team, dependencies])

    with gr.Tab("Manage Products"):
        product_name = gr.Textbox(label="Product Name")
        add_prod_btn = gr.Button("Add Product")
        remove_prod_btn = gr.Button("Remove Product")
        product_table = gr.DataFrame(value=manager.products, label="Current Products", headers="auto")

        # Event handlers for product management
        add_prod_btn.click(fn=add_product, inputs=product_name, outputs=[product_table, product])
        remove_prod_btn.click(fn=remove_product, inputs=product_name, outputs=[product_table, product])

# Launch the Gradio app
demo.launch()
