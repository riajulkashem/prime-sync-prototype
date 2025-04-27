from PySide6.QtCore import QObject, Signal
from db.database import Settings, db
import json

class StateManager(QObject):
    settings_changed = Signal(dict)

    def __init__(self):
        super().__init__()
        self._settings = self.load_settings()
        self._current_user = None

    def load_settings(self):
        try:
            # Ensure the database connection is open
            if not db.is_closed():
                db.connect(reuse_if_open=True)

            # Check if the Settings table exists; if not, create it
            db.create_tables([Settings], safe=True)

            # Try to load settings from the database
            settings_record = Settings.select().where(Settings.key == "app_settings").first()
            if settings_record:
                return json.loads(settings_record.value)

            # If no settings exist, create default settings and save them
            default_settings = {
                "cloud_api_url": "https://api.primesync.com/v1",
                "username": "admin",
                "password": "••••••••",
                "auto_check_interval": 15,
                "enable_auto_sync": True,
                "periodic_sync_time": "12:00 PM",
                "enable_periodic_sync": True
            }
            Settings.create(key="app_settings", value=json.dumps(default_settings))
            return default_settings

        except Exception as e:
            print(f"Error loading settings from database: {e}")
            # Fallback to default settings if there's an error
            return {
                "cloud_api_url": "https://api.primesync.com/v1",
                "username": "admin",
                "password": "••••••••",
                "auto_check_interval": 15,
                "enable_auto_sync": True,
                "periodic_sync_time": "12:00 PM",
                "enable_periodic_sync": True
            }
        finally:
            if not db.is_closed():
                db.close()

    def save_settings(self):
        try:
            if not db.is_closed():
                db.connect(reuse_if_open=True)

            settings_record = Settings.select().where(Settings.key == "app_settings").first()
            if settings_record:
                settings_record.value = json.dumps(self._settings)
                settings_record.save()
            else:
                Settings.create(key="app_settings", value=json.dumps(self._settings))
        except Exception as e:
            print(f"Error saving settings to database: {e}")
        finally:
            if not db.is_closed():
                db.close()

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = value
        self.save_settings()
        self.settings_changed.emit(self._settings)

    @property
    def current_user(self):
        return self._current_user

    @current_user.setter
    def current_user(self, value):
        self._current_user = value

# Singleton instance
state_manager = StateManager()