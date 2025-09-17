import win32com.client as client
import datetime
import json

class OutlookCalendarReader:
    def __init__(self, calendar_name):
        self.outlook = client.Dispatch("Outlook.Application")
        self.namespace = self.outlook.GetNamespace("MAPI")
        self.calendar_name = calendar_name

    def get_appointments(self, start_date=None, end_date=None):
        if start_date is None:
            # 默认获取当前时间前后一个月的预约
            today = datetime.date.today()
            start_date = today - datetime.timedelta(days=30)
            end_date = today + datetime.timedelta(days=30)

        calendar = self.find_calendar(self.namespace.Folders[1], self.calendar_name)

        if calendar:
            appointments = []
            for appointment in calendar.Items:
                if start_date <= appointment.Start.date() <= end_date:
                    appointment_info = {
                        "Subject": appointment.Subject,
                        "Start": appointment.Start.strftime("%Y-%m-%d %H:%M:%S"),
                        "End": appointment.End.strftime("%Y-%m-%d %H:%M:%S"),
                        "Location": appointment.Location,
                        "Body": appointment.Body,
                    }
                    appointments.append(appointment_info)

            return appointments
        else:
            return []

    def find_calendar(self, folder, calendar_name):
        if folder.Name == calendar_name:
            return folder
        for subfolder in folder.Folders:
            result = self.find_calendar(subfolder, calendar_name)
            if result:
                return result
        return None

    def export_to_json(self, appointments, output_file):
        with open(output_file, "w") as f:
            json.dump(appointments, f, indent=4)

# 使用这个类的例子
calendar_reader = OutlookCalendarReader("Calendar Name")  # 替换为要读取的日历名称
appointments = calendar_reader.get_appointments()

# 输出预约信息到JSON文件
calendar_reader.export_to_json(appointments, "calendar_appointments.json")



