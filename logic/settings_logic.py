from utilities.state_manager import state_manager

class SettingsLogic:
    def __init__(self):
        pass  # Settings are now managed by state_manager

    def save_settings(self, data):
        state_manager.settings = data
        print("Settings saved:", state_manager.settings)

    def test_connection(self):
        # Simulate connection test
        return True