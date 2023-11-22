import pandas as pd
import os

class SpreadsheetHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_extension = file_path.split('.')[-1].lower()
        self.data = None
        self.read_file()

    def read_file(self):
        """Reads the spreadsheet file."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"The file {self.file_path} does not exist")

        if self.file_extension in ['xlsx', 'xls']:
            self.data = pd.read_excel(self.file_path)
        elif self.file_extension == 'csv':
            self.data = pd.read_csv(self.file_path)
        else:
            raise ValueError("Unsupported file format")

    def create_update_row(self, row_index, row_data):
        """Creates or updates a row in the data."""
        self.data.loc[row_index] = row_data

    def read_row(self, row_index):
        """Reads a row from the data."""
        return self.data.loc[row_index]

    def delete_row(self, row_index):
        """Deletes a row from the data."""
        self.data.drop(row_index, inplace=True)

    def save_file(self):
        """Saves the current data back to the file."""
        if self.file_extension == 'xlsx':
            self.data.to_excel(self.file_path, index=False)
        elif self.file_extension == 'csv':
            self.data.to_csv(self.file_path, index=False)
        else:
            raise ValueError("Unsupported file format")

    def print_data(self):
        """Prints the current data."""
        print(self.data)

