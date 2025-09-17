import win32com.client as client

class OutlookFolderTree:
    def __init__(self):
        self.outlook = client.Dispatch("Outlook.Application")
        self.namespace = self.outlook.GetNamespace("MAPI")
        self.root = {"name": "Outlook Folders", "children": []}

    def build_tree(self, folder, parent_node):
        folder_node = {"name": folder.Name, "children": []}
        parent_node["children"].append(folder_node)

        for subfolder in folder.Folders:
            self.build_tree(subfolder, folder_node)

    def display_tree(self):
        self.build_tree(self.namespace.Folders[1], self.root)  # 使用默认邮箱账号的根文件夹

        def display_node(node, indent=""):
            print(indent + node["name"])
            for child in node["children"]:
                display_node(child, indent + "  ")

        display_node(self.root)

# 使用这个类的例子
folder_tree = OutlookFolderTree()
folder_tree.display_tree()


