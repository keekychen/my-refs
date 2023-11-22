import toml
import os

class TomlHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.read_toml()

    def read_toml(self):
        """Reads the TOML file."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                self.data = toml.load(file)
        else:
            raise FileNotFoundError(f"The file {self.file_path} does not exist")

    def create_update_entry(self, key, value):
        """Creates or updates an entry in the TOML data."""
        if not self.data:
            self.data = {}
        self.data[key] = value

    def read_entry(self, key):
        """Reads an entry from the TOML data."""
        return self.data.get(key)

    def delete_entry(self, key):
        """Deletes an entry from the TOML data."""
        if key in self.data:
            del self.data[key]

    def save_toml(self):
        """Saves the current data back to the TOML file."""
        with open(self.file_path, 'w') as file:
            toml.dump(self.data, file)

    def print_toml(self):
        """Prints the current TOML data."""
        print(toml.dumps(self.data))

