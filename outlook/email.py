import win32com.client as client

class OutlookEmailReader:
    def __init__(self, folder_name):
        self.outlook = client.Dispatch("Outlook.Application")
        self.namespace = self.outlook.GetNamespace("MAPI")
        self.folder_name = folder_name
        self.folder = None

    def find_folder(self, folder, folder_name):
        if folder.Name == folder_name:
            return folder
        for subfolder in folder.Folders:
            result = self.find_folder(subfolder, folder_name)
            if result:
                return result
        return None

    def get_emails(self, folder=None):
        if folder is None:
            folder = self.find_folder(self.namespace.Folders[1], self.folder_name)  # 使用默认邮箱账号的根文件夹

        emails = []
        for email in folder.Items:
            email_info = {
                "Subject": email.Subject,
                "Sender": email.SenderName,
                "Body": email.Body,
                "Attachments": [],
            }

            # 提取附件信息
            for attachment in email.Attachments:
                email_info["Attachments"].append({
                    "Name": attachment.FileName,
                    "Size": attachment.Size,
                })

            emails.append(email_info)

        return emails

# 使用这个类的例子
email_reader = OutlookEmailReader("Inbox")  # 指定要读取的文件夹名称
emails = email_reader.get_emails()

# 打印邮件信息示例
for i, email in enumerate(emails, start=1):
    print(f"Email {i}:")
    print(f"Subject: {email['Subject']}")
    print(f"Sender: {email['Sender']}")
    print(f"Body: {email['Body']}")
    print("Attachments:")
    for attachment in email['Attachments']:
        print(f"  - Name: {attachment['Name']}, Size: {attachment['Size']} bytes")
    print()




import win32com.client as client

class OutlookEmail:
    def __init__(self, recipient, subject, body):
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.attachments = []
        self.cc = None
        self.bcc = None
        self.outlook = client.Dispatch("Outlook.Application")

    def add_attachment(self, attachment_path):
        self.attachments.append(attachment_path)

    def set_cc(self, cc):
        self.cc = cc

    def set_bcc(self, bcc):
        self.bcc = bcc

    def send(self):
        message = self.outlook.CreateItem(0)
        message.To = self.recipient
        message.Subject = self.subject
        message.Body = self.body

        # 添加附件
        for attachment_path in self.attachments:
            message.Attachments.Add(attachment_path)

        # 设置抄送和密送
        if self.cc:
            message.CC = self.cc
        if self.bcc:
            message.BCC = self.bcc

        message.Send()

# 使用这个类的例子
email = OutlookEmail("recipient@example.com", "Test Subject", "This is a test email.")
email.add_attachment("path/to/attachment1.pdf")
email.add_attachment("path/to/attachment2.jpg")
email.set_cc("cc@example.com")
email.set_bcc("bcc@example.com")
email.send()


