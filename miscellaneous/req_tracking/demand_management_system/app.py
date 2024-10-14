import gradio as gr
from demand_manager import DemandManager
from datetime import datetime

# Initialize the demand manager
manager = DemandManager()

def add_request(req_name, desc, origin_team, rec_team, product, dependencies, sub_date, exp_date, status, priority):
    """Add a new request and return the updated request table."""
    sub_date = sub_date.strftime("%Y-%m-%d")
    exp_date = exp_date.strftime("%Y-%m-%d")
    updated_data = manager.add_request(req_name, desc, origin_team, rec_team, product, dependencies, sub_date, exp_date, status, priority)
    return updated_data

def filter_requests(team):
    """Filter requests by team and return the filtered table."""
    return manager.filter_requests(team)

def export_requests():
    """Export the request data to a CSV file."""
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
