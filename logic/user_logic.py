from db.database import User
import pandas as pd

class UserLogic:
    def __init__(self, page_size=100):
        self.page_size = page_size
        self.current_page = 1
        self.users = []
        self.total_count = 0
        self.load_page(1)

    def load_page(self, page):
        self.current_page = page
        offset = (page - 1) * self.page_size
        self.users = list(User.select(
            User.uid, User.name, User.role, User.password, User.group_id, User.user_id, User.card, User.user_cloud_id
        ).offset(offset).limit(self.page_size))
        self.total_count = User.select().count()

    def get_page(self):
        return self.users, self.current_page, (self.total_count + self.page_size - 1) // self.page_size

    def add_user(self, data):
        role_map = {"Admin": 1, "Manager": 2, "User": 3}
        User.create(
            uid=User.select().count() + 1,  # Simple UID generation
            name=data["Full Name"],
            role=role_map[data["Role"]],
            password=data["Password"] or None,
            group_id=int(data["Group ID"]) if data["Group ID"] else None,
            user_id=data["User ID"] or f"U{User.select().count() + 1:03d}",
            card=data["Card Number"] or None
        )
        self.load_page(self.current_page)

    def edit_user(self, uid, data):
        role_map = {"Admin": 1, "Manager": 2, "User": 3}
        user = User.get(User.uid == uid)
        user.name = data["Full Name"]
        user.role = role_map[data["Role"]]
        user.password = data["Password"] or None
        user.group_id = int(data["Group ID"]) if data["Group ID"] else None
        user.user_id = data["User ID"]
        user.card = data["Card Number"] or None
        user.save()
        self.load_page(self.current_page)

    def delete_user(self, uid):
        user = User.get(User.uid == uid)
        user.delete_instance()
        self.load_page(self.current_page)

    def filter_users(self, search_text, role_filter):
        search_text = search_text.lower()
        query = User.select(
            User.uid, User.name, User.role, User.password, User.group_id, User.user_id, User.card, User.user_cloud_id
        )

        if search_text:
            query = query.where(
                (User.name.contains(search_text)) |
                (User.user_id.contains(search_text))
            )

        if role_filter != "All Roles":
            role_map = {"Admin": 1, "Manager": 2, "User": 3}
            query = query.where(User.role == role_map[role_filter])

        offset = (self.current_page - 1) * self.page_size
        filtered_users = list(query.offset(offset).limit(self.page_size))
        filtered_count = query.count()
        return filtered_users, self.current_page, (filtered_count + self.page_size - 1) // self.page_size

    def import_users(self, parent):
        try:
            df = pd.read_excel("users_import.xlsx")
            for _, row in df.iterrows():
                role_map = {"Admin": 1, "Manager": 2, "User": 3}
                User.create(
                    uid=row["UID"],
                    name=row["Name"],
                    role=role_map[row["Role"]],
                    password=row["Password"] if pd.notna(row["Password"]) else None,
                    group_id=int(row["Group ID"]) if pd.notna(row["Group ID"]) else None,
                    user_id=row["User ID"],
                    card=row["Card"] if pd.notna(row["Card"]) else None,
                    user_cloud_id=int(row["Cloud ID"]) if pd.notna(row["Cloud ID"]) else None
                )
            self.load_page(self.current_page)
            print("Users imported successfully")
        except Exception as e:
            print(f"Error importing users: {e}")

    def export_users(self, parent):
        try:
            users = User.select().dicts()
            df = pd.DataFrame(list(users))
            if not df.empty:
                df.to_excel("users_export.xlsx", index=False)
                print("Users exported to users_export.xlsx")
            else:
                print("No users to export")
        except Exception as e:
            print(f"Error exporting users: {e}")