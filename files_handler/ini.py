import configparser
import os

class IniConfig:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = configparser.ConfigParser()

    def read_ini(self):
        """Reads an INI file."""
        if os.path.exists(self.file_path):
            self.config.read(self.file_path)
        else:
            raise FileNotFoundError(f"The file {self.file_path} does not exist")

    def get(self, section, option):
        """Gets the value of the given section and option."""
        return self.config.get(section, option)

    def set(self, section, option, value):
        """Sets the value in the given section and option."""
        if section not in self.config.sections():
            self.config.add_section(section)
        self.config.set(section, option, value)

    def save_ini(self):
        """Saves the current configuration to the INI file."""
        with open(self.file_path, 'w') as configfile:
            self.config.write(configfile)

    def print_ini(self):
        """Prints the entire configuration."""
        for section in self.config.sections():
            print(f"[{section}]")
            for option in self.config.options(section):
                print(f"{option} = {self.config.get(section, option)}")
            print()
