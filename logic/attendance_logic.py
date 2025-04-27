from db.database import Attendance, User
import pandas as pd


class AttendanceLogic:
    def __init__(self, page_size=100):
        self.page_size = page_size
        self.current_page = 1
        self.attendances = []
        self.total_count = 0
        self.load_page(1)

    def load_page(self, page):
        self.current_page = page
        offset = (page - 1) * self.page_size
        query = (Attendance.select(
            Attendance.id,
            Attendance.timestamp,
            User.name,
            Attendance.status,
            Attendance.punch,
            Attendance.uid,
            Attendance.user
        )
                 .join(User, on=(Attendance.user == User.uid))
                 .order_by(Attendance.timestamp.desc())
                 .offset(offset)
                 .limit(self.page_size))
        self.attendances = list(query)
        self.total_count = Attendance.select().count()

    def get_page(self):
        return self.attendances, self.current_page, (self.total_count + self.page_size - 1) // self.page_size

    def filter_attendance(self, search_text, date_filter=None):
        search_text = search_text.lower()
        query = (Attendance.select(
            Attendance.id,
            Attendance.timestamp,
            User.name,
            Attendance.status,
            Attendance.punch,
            Attendance.uid,
            Attendance.user
        )
                 .join(User, on=(Attendance.user == User.uid))
                 .order_by(Attendance.timestamp.desc()))

        if search_text:
            query = query.where(
                (User.name.contains(search_text)) |
                (Attendance.status.contains(search_text)) |
                (Attendance.punch.contains(search_text))
            )

        if date_filter:
            query = query.where(Attendance.timestamp >= date_filter[0], Attendance.timestamp <= date_filter[1])

        offset = (self.current_page - 1) * self.page_size
        filtered_attendances = list(query.offset(offset).limit(self.page_size))
        filtered_count = query.count()
        return filtered_attendances, self.current_page, (filtered_count + self.page_size - 1) // self.page_size

    def export_attendance(self, parent):
        try:
            attendances = (Attendance.select(
                Attendance.id,
                Attendance.timestamp,
                User.name,
                Attendance.status,
                Attendance.punch,
                Attendance.uid
            )
                           .join(User, on=(Attendance.user == User.uid))
                           .order_by(Attendance.timestamp.desc())
                           .dicts())
            df = pd.DataFrame(list(attendances))
            if not df.empty:
                df.to_excel("attendance_export.xlsx", index=False)
                print("Attendance exported to attendance_export.xlsx")
            else:
                print("No attendance data to export")
        except Exception as e:
            print(f"Error exporting attendance: {e}")
