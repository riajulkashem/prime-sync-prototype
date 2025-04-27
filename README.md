# PrimeSync - Attendance Management System

## Project Description
**PrimeSync** is a desktop application built with PySide6 (Qt for Python) to manage attendance tracking across multiple devices. It integrates with biometric devices using the `pyzk` library to pull and push user and attendance data, syncs with a cloud server, and provides a user-friendly interface for managing devices, users, and attendance records. The application is designed for organizations to streamline attendance tracking, offering features like user management, device synchronization, and cloud integration.

PrimeSync was developed as a prototype to demonstrate a full-stack attendance solution, focusing on usability, error handling, and extensibility. It includes a modular architecture, proper logging, and user feedback mechanisms to ensure a robust user experience.

## Features
- **Device Management**: Add, view, and manage biometric devices for attendance tracking.
- **User Management**: Create, update, delete, and import/export users, with automatic synchronization to devices.
- **Attendance Tracking**: Pull attendance data from devices and post it to a cloud server.
- **Dashboard Overview**: View statistics for devices, users, and attendance records.
- **Synchronization**:
  - **Pull Device**: Retrieve attendance data from devices to the local database.
  - **Post Cloud**: Push attendance data to a cloud server (abstract implementation).
  - **Push Users**: Sync users from the local database to devices.
  - **Pull Users**: Retrieve users from devices to the local database.
- **User Feedback**:
  - Processing dialog with animation during long-running operations.
  - Error notifications for failed operations (e.g., device connection issues, cloud sync failures).
- **Logging**: Comprehensive logging for debugging and monitoring.
- **Developer Credits**: A popup dialog showcasing the developer’s profile and social media links.

## Installation

### Prerequisites
- Python 3.13 or higher
- PySide6 (`pip install PySide6`)
- peewee (`pip install peewee`)
- pyzk (`pip install zklib`)
- requests (`pip install requests`)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/riajulkashem/primesync.git
   cd primesync
   ```

2. **Set Up a Virtual Environment** (Optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   If `requirements.txt` is not available, install the prerequisites manually:
   ```bash
   pip install PySide6 peewee zklib requests
   ```

4. **Prepare Icons**:
   - Ensure the `icons/` directory contains all necessary icons (e.g., `dashboard.png`, `cloud-upload.png`, `riajulkashem.png` for the developer profile).
   - If icons are missing, replace them with your own or update the paths in the code.

5. **Run the Application**:
   ```bash
   python prototype/main.py
   ```

## Usage Guide

### Launching the App
Run `main.py` to start the application. The main window displays a sidebar with navigation options and a content area.

### Navigation
- **Dashboard**: View an overview of devices, users, and attendance records. Use the "Post Cloud" and "Pull Device" buttons to sync attendance data.
- **Devices**: Manage biometric devices (e.g., add new devices).
- **Users**: Manage users, including adding, editing, deleting, and syncing users to devices.
- **Attendance**: View attendance records pulled from devices.
- **Settings**: Configure application settings (e.g., cloud API URL).
- **Developer**: View developer credits with a profile image and social media links.
- **Quit**: Exit the application.

### Key Operations
- **Adding a User**:
  1. Navigate to the "Users" screen.
  2. Click "Add User" and fill in the form.
  3. Submit the form to add the user to the database and sync to devices.
- **Syncing Users**:
  - Use "Pull Users" to retrieve users from devices.
  - Use "Push Users" to send users to devices.
  - User changes (create, update, delete, import) automatically trigger a sync to devices.
- **Syncing Attendance**:
  - On the Dashboard, click "Pull Device" to retrieve attendance data from all devices.
  - Click "Post Cloud" to send attendance data to the cloud (configure the API endpoint in settings).
- **Error Handling**:
  - If an operation fails (e.g., device offline, cloud sync error), an error popup will display the details.

## File Structure
```
primesync/
├── prototype/
│   ├── main.py                # Entry point of the application
│   ├── db/
│   │   └── database.py        # Database models and initialization (SQLite)
│   ├── logic/
│   │   ├── settings_logic.py  # Logic for settings screen
│   │   └── user_logic.py      # Logic for user management
│   ├── ui/
│   │   ├── attendance_ui.py   # Attendance screen UI
│   │   ├── dashboard_ui.py    # Dashboard screen UI
│   │   ├── device_ui.py       # Device screen UI
│   │   ├── settings_ui.py     # Settings screen UI
│   │   ├── user_ui.py         # User screen UI
│   │   ├── developer_credits.py # Developer credits popup
│   │   ├── error_dialog.py    # Error notification dialog
│   │   ├── processing_dialog.py # Processing animation dialog
│   │   └── components/
│   │       ├── form_dialog.py # Reusable form dialog for adding/editing
│   │       └── table_widget.py # Paginated table widget
│   └── utilities/
│       ├── device_manager.py  # Utility class for device operations (pyzk)
│       ├── logger.py         # Logging utility
│       └── state_manager.py  # State management for settings
├── icons/                     # Directory for icons (e.g., dashboard.png, riajulkashem.png)
└── README.md                  # Project documentation
```

## Developer Credits
**Riajul Kashem**  
*Software Engineer & Full-Stack Developer*  
- GitHub: [github.com/riajulkashem](https://github.com/riajulkashem)  
- LinkedIn: [linkedin.com/in/riajulkashem](https://linkedin.com/in/riajulkashem)
- Twitter: [twitter.com/riajulkashem](https://twitter.com/riajulkashem)

## Future Improvements
- Implement threading for non-blocking sync operations.
- Add a success notification dialog for completed operations.
- Integrate with a real cloud API for attendance posting.
- Add support for multiple device types and protocols.
- Enhance the UI with more advanced styling and animations.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details (if applicable).

---

**Note**: Update the repository URL, social media links, and license information as needed.