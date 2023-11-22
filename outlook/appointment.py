import win32com.client as client

class OutlookAppointment:
    def __init__(self, subject, start, end, location=None, body=None):
        self.subject = subject
        self.start = start
        self.end = end
        self.location = location
        self.body = body
        self.outlook = client.Dispatch("Outlook.Application")

        # 初始化其他属性
        self.attendees = []  # 存储邀请参与者的列表
        self.show_as_free = False  # 显示为忙碌
        self.reminder_none = True  # 提醒设置为无
        self.response_no_request = True  # 响应选项为不请求响应

    def add_attendee(self, attendee_email):
        self.attendees.append(attendee_email)

    def set_show_as_free(self, value=True):
        self.show_as_free = value

    def set_reminder_none(self, value=True):
        self.reminder_none = value

    def set_response_no_request(self, value=True):
        self.response_no_request = value

    def send(self):
        appointment = self.outlook.CreateItem(1)  # 1 表示创建一个预约对象

        # 设置预约属性
        appointment.Subject = self.subject
        appointment.Start = self.start
        appointment.End = self.end
        if self.location:
            appointment.Location = self.location
        if self.body:
            appointment.Body = self.body

        # 添加邀请参与者
        for attendee in self.attendees:
            appointment.Recipients.Add(attendee)

        # 设置显示为忙碌
        if self.show_as_free:
            appointment.BusyStatus = 2  # 2 表示忙碌

        # 设置提醒为无
        if self.reminder_none:
            appointment.ReminderSet = False

        # 设置响应选项为不请求响应
        if self.response_no_request:
            appointment.ResponseRequested = False

        # 发送预约
        appointment.Save()
        appointment.Send()

# 使用这个类的例子
appointment = OutlookAppointment(
    subject="Meeting with Client",
    start="2023-11-30 09:00",
    end="2023-11-30 10:00",
    location="Office",
    body="Discuss project updates."
)
appointment.add_attendee("attendee1@example.com")
appointment.add_attendee("attendee2@example.com")
appointment.set_show_as_free(True)
appointment.set_reminder_none(True)
appointment.set_response_no_request(True)
appointment.send()
