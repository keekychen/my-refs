import xml.etree.ElementTree as ET

class XMLHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tree = ET.parse(self.file_path)
        self.root = self.tree.getroot()

    def create_element(self, tag, attrib={}, text=None):
        """Creates a new element."""
        element = ET.Element(tag, attrib)
        if text:
            element.text = text
        return element

    def add_element(self, parent_tag, element):
        """Adds a new element to a parent element identified by parent_tag."""
        parent = self.root.find(parent_tag)
        if parent is not None:
            parent.append(element)
        else:
            raise ValueError(f"Parent tag '{parent_tag}' not found")

    def read_element(self, tag):
        """Finds and returns elements with a specific tag."""
        return self.root.findall(tag)

    def update_element(self, tag, attrib, new_value):
        """Updates an element's attribute or text."""
        elements = self.root.findall(tag)
        for elem in elements:
            if attrib in elem.attrib:
                elem.set(attrib, new_value)
            else:
                elem.text = new_value

    def delete_element(self, tag):
        """Deletes elements with a specific tag."""
        elements = self.root.findall(tag)
        for elem in elements:
            self.root.remove(elem)

    def save_xml(self):
        """Saves the current XML tree to the file."""
        self.tree.write(self.file_path)

    def print_xml(self):
        """Prints the XML structure."""
        ET.dump(self.root)
