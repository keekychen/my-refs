import pandas as pd

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
        """Load existing request data from the CSV file or initialize an empty DataFrame."""
        try:
            self.data = pd.read_csv(self.data_file)
            if self.data.empty:
                self.data = pd.DataFrame(columns=self.columns)
        except (FileNotFoundError, pd.errors.EmptyDataError):
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

    # Department management methods
    def load_departments(self):
        """Load departments from the CSV file or initialize an empty list."""
        try:
            self.departments = pd.read_csv(self.dept_file)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            self.departments = pd.DataFrame(columns=["Department"])

    def add_department(self, dept_name):
        """Add a new department to the departments list."""
        if dept_name not in self.departments['Department'].values:
            new_dept = pd.DataFrame([[dept_name]], columns=["Department"])
            self.departments = pd.concat([self.departments, new_dept], ignore_index=True)
            self.save_departments()

    def remove_department(self, dept_name):
        """Remove a department from the list."""
        self.departments = self.departments[self.departments['Department'] != dept_name]
        self.save_departments()

    def save_departments(self):
        """Save the departments list to the CSV file."""
        self.departments.to_csv(self.dept_file, index=False)

    def get_departments(self):
        """Return the list of departments."""
        return self.departments['Department'].tolist()

    # Product management methods
    def load_products(self):
        """Load products from the CSV file or initialize an empty list."""
        try:
            self.products = pd.read_csv(self.product_file)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            self.products = pd.DataFrame(columns=["Product"])

    def add_product(self, product_name):
        """Add a new product to the products list."""
        if product_name not in self.products['Product'].values:
            new_product = pd.DataFrame([[product_name]], columns=["Product"])
            self.products = pd.concat([self.products, new_product], ignore_index=True)
            self.save_products()

    def remove_product(self, product_name):
        """Remove a product from the list."""
        self.products = self.products[self.products['Product'] != product_name]
        self.save_products()

    def save_products(self):
        """Save the products list to the CSV file."""
        self.products.to_csv(self.product_file, index=False)

    def get_products(self):
        """Return the list of products."""
        return self.products['Product'].tolist()
