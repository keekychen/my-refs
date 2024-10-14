import os

# Define the directory structure and file contents
project_structure = {
    "demand_management_system": {
        "app.py": """import gradio as gr
from demand_manager import DemandManager
from datetime import datetime

# Initialize the demand manager
manager = DemandManager()

def add_request(req_name, desc, origin_team, rec_team, product, dependencies, sub_date, exp_date, status, priority):
    \"\"\"Add a new request and return the updated request table.\"\"\"
    sub_date = sub_date.strftime("%Y-%m-%d")
    exp_date = exp_date.strftime("%Y-%m-%d")
    updated_data = manager.add_request(req_name, desc, origin_team, rec_team, product, dependencies, sub_date, exp_date, status, priority)
    return updated_data

def filter_requests(team):
    \"\"\"Filter requests by team and return the filtered table.\"\"\"
    return manager.filter_requests(team)

def export_requests():
    \"\"\"Export the request data to a CSV file.\"\"\"
    return manager.export_to_csv()

# Gradio interface for submitting and managing requests
with gr.Blocks() as demo:
    with gr.Row():
        req_name = gr.Textbox(label="Request Name")
        desc = gr.Textbox(label="Description", lines=3)
    with gr.Row():
        origin_team = gr.Textbox(label="Origin Team")
        rec_team = gr.Textbox(label="Receiving Team")
        product = gr.Textbox(label="Receiving Team's Product")
    with gr.Row():
        dependencies = gr.Textbox(label="Dependencies (comma-separated)")
        sub_date = gr.Date(label="Submission Date", value=datetime.now())
        exp_date = gr.Date(label="Expected Completion Date")
    with gr.Row():
        status = gr.Dropdown(choices=["Pending", "In Progress", "Completed"], label="Status")
        priority = gr.Dropdown(choices=["Low", "Medium", "High", "Critical"], label="Priority")
    submit_btn = gr.Button("Submit Request")

    # Table to display all requests
    request_table = gr.DataFrame(manager.data, label="Existing Requests")
    
    # Filter requests by team
    team_filter = gr.Textbox(label="Filter by Receiving Team (optional)", placeholder="Enter team name")
    filter_btn = gr.Button("Filter Requests")
    export_btn = gr.Button("Export to CSV")

    # Event handlers for Gradio UI
    submit_btn.click(fn=add_request, 
                     inputs=[req_name, desc, origin_team, rec_team, product, dependencies, sub_date, exp_date, status, priority], 
                     outputs=request_table)
    
    filter_btn.click(fn=filter_requests, inputs=team_filter, outputs=request_table)
    
    export_btn.click(fn=export_requests, outputs=gr.File(label="Download CSV"))

# Launch the Gradio app
demo.launch()
""",
        "demand_manager.py": """import pandas as pd
from datetime import datetime

class DemandManager:
    def __init__(self, data_file='data/requests.csv'):
        self.data_file = data_file
        self.columns = ["Request ID", "Request Name", "Description", "Origin Team", 
                        "Receiving Team", "Product", "Dependencies", "Submission Date", 
                        "Expected Completion Date", "Status", "Priority"]
        self.load_data()

    def load_data(self):
        \"\"\"Load existing request data from the CSV file.\"\"\"
        try:
            self.data = pd.read_csv(self.data_file)
        except FileNotFoundError:
            # Initialize with an empty DataFrame if file does not exist
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
""",
        "data": {
            "requests.csv": ""
        },
        "requirements.txt": "gradio==3.16.2\npandas==2.1.1"
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

