import os

# Define the directory structure and file contents
project_structure = {
    "demand_management_system": {
        "app.py": """import os
import gradio as gr
from demand_manager import DemandManager
from datetime import datetime

# Initialize the demand manager
manager = DemandManager()

def select_request(index):
    \"\"\"Populate the selected request details into the input fields for modification.\"\"\"
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
    \"\"\"Add or modify a request and return the updated request table.\"\"\"
    updated_data = manager.add_request(req_name, desc, origin_team, rec_team, product, ','.join(dependencies), sub_date, exp_date, status, priority)
    return updated_data

def filter_requests(team):
    \"\"\"Filter requests by team name using fuzzy matching.\"\"\"
    filtered_data = manager.data[manager.data["Receiving Team"].str.contains(team, case=False, na=False)]
    return filtered_data

def export_requests():
    \"\"\"Export the request data to a CSV file.\"\"\"
    return manager.export_to_csv()

def add_department(dept_name):
    \"\"\"Add a new department and return the updated department list and dropdowns.\"\"\"
    manager.add_department(dept_name)
    departments = manager.get_departments()
    return departments, departments, departments

def remove_department(dept_name):
    \"\"\"Remove a department and return the updated department list and dropdowns.\"\"\"
    manager.remove_department(dept_name)
    departments = manager.get_departments()
    return departments, departments, departments

def add_product(product_name):
    \"\"\"Add a new product and return the updated product list.\"\"\"
    manager.add_product(product_name)
    products = manager.get_products()
    return products

def remove_product(product_name):
    \"\"\"Remove a product and return the updated product list.\"\"\"
    manager.remove_product(product_name)
    products = manager.get_products()
    return products

# Gradio interface for managing departments and requests
with gr.Blocks() as demo:
    with gr.Tab("Manage Requests"):
        req_name = gr.Textbox(label="Request Name")
        desc = gr.Textbox(label="Description", lines=3)
        origin_team = gr.Dropdown(choices=manager.get_departments(), label="Origin Team")
        rec_team = gr.Dropdown(choices=manager.get_departments(), label="Receiving Team")
        product = gr.Dropdown(choices=manager.get_products(), label="Receiving Team's Product")
        dependencies = gr.Dropdown(choices=manager.get_departments(), label="Dependencies", multiselect=True)
        sub_date = gr.Date(label="Submission Date", value=str(datetime.now().date()))
        exp_date = gr.Date(label="Expected Completion Date")
        status = gr.Dropdown(choices=["Pending", "In Progress", "Completed"], label="Status")
        priority = gr.Dropdown(choices=["Low", "Medium", "High", "Critical"], label="Priority")
        submit_btn = gr.Button("Submit Request")

        request_table = gr.Dataframe(value=manager.data, label="Existing Requests")
        
        record_index = gr.Number(label="Select Request Index (1-based)", value=1, precision=0)
        select_btn = gr.Button("Select Request")
        select_btn.click(fn=select_request, inputs=record_index, outputs=[req_name, desc, origin_team, rec_team, product, dependencies, sub_date, exp_date, status, priority])
        
        team_filter = gr.Textbox(label="Filter by Receiving Team (optional)", placeholder="Enter team name")
        filter_btn = gr.Button("Filter Requests")
        filter_btn.click(fn=filter_requests, inputs=team_filter, outputs=request_table)

        export_btn = gr.Button("Export to CSV")
        export_btn.click(fn=export_requests, outputs=gr.File(label="Download CSV"))

    with gr.Tab("Manage Departments"):
        dept_name = gr.Textbox(label="Department Name")
        add_dept_btn = gr.Button("Add Department")
        remove_dept_btn = gr.Button("Remove Department")
        department_table = gr.Dataframe(value=manager.departments, label="Current Departments")

        add_dept_btn.click(fn=add_department, inputs=dept_name, outputs=[department_table, origin_team, rec_team, dependencies])
        remove_dept_btn.click(fn=remove_department, inputs=dept_name, outputs=[department_table, origin_team, rec_team, dependencies])

    with gr.Tab("Manage Products"):
        product_name = gr.Textbox(label="Product Name")
        add_prod_btn = gr.Button("Add Product")
        remove_prod_btn = gr.Button("Remove Product")
        product_table = gr.Dataframe(value=manager.products, label="Current Products")

        add_prod_btn.click(fn=add_product, inputs=product_name, outputs=product_table)
        remove_prod_btn.click(fn=remove_product, inputs=product_name, outputs=product_table)

# Launch the Gradio app
demo.launch()
""",
        "demand_manager.py": """import pandas as pd

class DemandManager:
    def __init__(self, data_file='data/requests.csv', dept_file='data/departments.csv', product_file='data/products.csv'):
        self.data_file = data_file
        self.dept_file = dept_file
        self.product_file = product_file
        self.columns = ["Request ID", "Request Name", "Description", "Origin Team", 
                        "Receiving Team", "Product", "Dependencies", "Submission Date", 
                        "Expected Completion Date", "Status", "Priority"]
        self.load_data()
        self.load_departments()
        self.load_products()

    def load_data(self):
        \"\"\"Load existing request data from the CSV file or initialize an empty DataFrame.\"\"\"
        try:
            self.data = pd.read_csv(self.data_file)
            if self.data.empty:
                self.data = pd.DataFrame(columns=self.columns)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            self.data = pd.DataFrame(columns=self.columns)

    def save_data(self):
        \"\"\"Save the current request data to the CSV file.\"\"\"
        self.data.to_csv(self.data_file, index=False)

    def add_request(self, req_name, desc, origin_team, rec_team, product, dependencies, sub_date, exp_date, status, priority):
        \"\"\"Add a new request to the data.\"\"\"
        req_id = len(self.data) + 1
        new_entry = pd.DataFrame([[req_id, req_name, desc, origin_team, rec_team, product, dependencies, 
                                   sub_date, exp_date, status, priority]], columns=self.columns)
        self.data = pd.concat([self.data, new_entry], ignore_index=True)
        self.save_data()
        return self.data

    def filter_requests(self, team=None):
        \"\"\"Filter requests by receiving team.\"\"\"
        if team:
            filtered_data = self.data[self.data["Receiving Team"] == team]
        else:
            filtered_data = self.data
        return filtered_data

    def export_to_csv(self, filename="exported_requests.csv"):
        \"\"\"Export the current data to a CSV file.\"\"\"
        self.data.to_csv(filename, index=False)
        return filename

    # Department management methods
    def load_departments(self):
        \"\"\"Load departments from the CSV file or initialize an empty list.\"\"\"
        try:
            self.departments = pd.read_csv(self.dept_file)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            self.departments = pd.DataFrame(columns=["Department"])

    def add_department(self, dept_name):
        \"\"\"Add a new department to the departments list.\"\"\"
        if dept_name not in self.departments['Department'].values:
            new_dept = pd.DataFrame([[dept_name]], columns=["Department"])
            self.departments = pd.concat([self.departments, new_dept], ignore_index=True)
            self.save_departments()

    def remove_department(self, dept_name):
        \"\"\"Remove a department from the list.\"\"\"
        self.departments = self.departments[self.departments['Department'] != dept_name]
        self.save_departments()

    def save_departments(self):
        \"\"\"Save the departments list to the CSV file.\"\"\"
        self.departments.to_csv(self.dept_file, index=False)

    def get_departments(self):
        \"\"\"Return the list of departments.\"\"\"
        return self.departments['Department'].tolist()

    # Product management methods
    def load_products(self):
        \"\"\"Load products from the CSV file or initialize an empty list.\"\"\"
        try:
            self.products = pd.read_csv(self.product_file)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            self.products = pd.DataFrame(columns=["Product"])

    def add_product(self, product_name):
        \"\"\"Add a new product to the products list.\"\"\"
        if product_name not in self.products['Product'].values:
            new_product = pd.DataFrame([[product_name]], columns=["Product"])
            self.products = pd.concat([self.products, new_product], ignore_index=True)
            self.save_products()

    def remove_product(self, product_name):
        \"\"\"Remove a product from the list.\"\"\"
        self.products = self.products[self.products['Product'] != product_name]
        self.save_products()

    def save_products(self):
        \"\"\"Save the products list to the CSV file.\"\"\"
        self.products.to_csv(self.product_file, index=False)

    def get_products(self):
        \"\"\"Return the list of products.\"\"\"
        return self.products['Product'].tolist()
""",
        "data": {
            "requests.csv": "",  # Empty CSV file for initialization
            "departments.csv": "",  # Empty CSV file for departments
            "products.csv": ""  # Empty CSV file for products
        },
        "requirements.txt": "gradio==5.0\npandas==2.1.1"
    }
}

def create_project_structure(structure, root=""):
    for name, content in structure.items():
        path = os.path.join(root, name)
        if isinstance(content, dict):
            # It's a directory, create it
            os.makedirs(path, exist_ok=True)
            # Recursively create subdirectories and files
            create_project_structure(content, root=path)
        else:
            # It's a file, create and write content
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    # Create the project structure in the current directory
    create_project_structure(project_structure)
    print("Project structure created successfully!")

