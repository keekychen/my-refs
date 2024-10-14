import pandas as pd
from datetime import datetime

class DemandManager:
    def __init__(self, data_file='data/requests.csv'):
        self.data_file = data_file
        self.columns = ["Request ID", "Request Name", "Description", "Origin Team", 
                        "Receiving Team", "Product", "Dependencies", "Submission Date", 
                        "Expected Completion Date", "Status", "Priority"]
        self.load_data()

    def load_data(self):
        """Load existing request data from the CSV file."""
        try:
            self.data = pd.read_csv(self.data_file)
        except FileNotFoundError:
            # Initialize with an empty DataFrame if file does not exist
            self.data = pd.DataFrame(columns=self.columns)

    def save_data(self):
        """Save the current request data to the CSV file."""
        self.data.to_csv(self.data_file, index=False)

    def add_request(self, req_name, desc, origin_team, rec_team, product, dependencies, sub_date, exp_date, status, priority):
        """Add a new request to the data."""
        req_id = len(self.data) + 1
        new_entry = pd.DataFrame([[req_id, req_name, desc, origin_team, rec_team, product, dependencies, 
                                   sub_date, exp_date, status, priority]], columns=self.columns)
        self.data = pd.concat([self.data, new_entry], ignore_index=True)
        self.save_data()
        return self.data

    def filter_requests(self, team=None):
        """Filter requests by receiving team."""
        if team:
            filtered_data = self.data[self.data["Receiving Team"] == team]
        else:
            filtered_data = self.data
        return filtered_data

    def export_to_csv(self, filename="exported_requests.csv"):
        """Export the current data to a CSV file."""
        self.data.to_csv(filename, index=False)
        return filename
