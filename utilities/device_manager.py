from zk import ZK, const
from db.database import Device, User, Attendance
import datetime
from utilities.logger import logger

class DeviceManager:
    def __init__(self, device):
        self.device = device
        self.zk = None

    def connect(self):
        """Connect to the device using pyzk."""
        try:
            self.zk = ZK(self.device.ip_address, port=self.device.port, password=int(self.device.password), timeout=5)
            conn = self.zk.connect()
            if conn:
                logger.info(f"Connected to device {self.device.ip_address}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to connect to device {self.device.ip_address}: {e}")
            return False

    def disconnect(self):
        """Disconnect from the device."""
        if self.zk:
            try:
                self.zk.disconnect()
                logger.info(f"Disconnected from device {self.device.ip_address}")
            except Exception as e:
                logger.error(f"Error disconnecting from device {self.device.ip_address}: {e}")
            finally:
                self.zk = None

    def pull_attendance(self):
        """Pull attendance data from the device and store it in the local database."""
        if not self.connect():
            return False, "Failed to connect to device"

        try:
            attendances = self.zk.get_attendance()
            if not attendances:
                return True, "No new attendance data found"

            for att in attendances:
                user = User.get_or_none(User.uid == att.user_id)
                if not user:
                    logger.warning(f"User with UID {att.user_id} not found in database")
                    continue

                # Check for duplicate attendance records
                existing = Attendance.get_or_none(
                    (Attendance.uid == att.user_id) &
                    (Attendance.timestamp == att.timestamp) &
                    (Attendance.status == att.status)
                )
                if existing:
                    continue

                Attendance.create(
                    user=user,
                    timestamp=att.timestamp,
                    status="Check-In" if att.punch == const.CHECK_IN else "Check-Out",
                    punch="IN" if att.punch == const.CHECK_IN else "OUT",
                    uid=att.user_id,
                    created_at=datetime.datetime.now()
                )
            logger.info(f"Pulled {len(attendances)} attendance records from device {self.device.ip_address}")
            return True, f"Pulled {len(attendances)} attendance records"
        except Exception as e:
            logger.error(f"Error pulling attendance from device {self.device.ip_address}: {e}")
            return False, f"Error pulling attendance: {e}"
        finally:
            self.disconnect()

    def pull_users(self):
        """Pull users from the device and store them in the local database."""
        if not self.connect():
            return False, "Failed to connect to device"

        try:
            users = self.zk.get_users()
            if not users:
                return True, "No users found on device"

            for user in users:
                # Check if user already exists in the database
                existing_user = User.get_or_none(User.uid == user.user_id)
                if existing_user:
                    # Update existing user
                    existing_user.name = user.name or existing_user.name
                    existing_user.role = user.privilege
                    existing_user.password = user.password or existing_user.password
                    existing_user.card = user.card or existing_user.card
                    existing_user.device = self.device
                    existing_user.updated_at = datetime.datetime.now()
                    existing_user.save()
                else:
                    # Create new user
                    User.create(
                        uid=user.user_id,
                        name=user.name or f"User_{user.user_id}",
                        role=user.privilege,
                        password=user.password,
                        group_id=None,
                        user_id=f"U{user.user_id:03d}",
                        card=user.card,
                        user_cloud_id=None,
                        device=self.device,
                        created_at=datetime.datetime.now(),
                        updated_at=datetime.datetime.now()
                    )
            logger.info(f"Pulled {len(users)} users from device {self.device.ip_address}")
            return True, f"Pulled {len(users)} users"
        except Exception as e:
            logger.error(f"Error pulling users from device {self.device.ip_address}: {e}")
            return False, f"Error pulling users: {e}"
        finally:
            self.disconnect()

    def push_users(self):
        """Push users from the local database to the device."""
        if not self.connect():
            return False, "Failed to connect to device"

        try:
            users = User.select().where(User.device == self.device)
            if not users:
                return True, "No users to push"

            for user in users:
                # Check if user already exists on the device
                device_users = self.zk.get_users()
                if any(device_user.user_id == user.uid for device_user in device_users):
                    # Update existing user on device
                    self.zk.set_user(
                        user_id=user.uid,
                        name=user.name,
                        privilege=user.role,
                        password=user.password or "",
                        card=user.card or ""
                    )
                else:
                    # Add new user to device
                    self.zk.set_user(
                        user_id=user.uid,
                        name=user.name,
                        privilege=user.role,
                        password=user.password or "",
                        card=user.card or ""
                    )
            logger.info(f"Pushed {len(users)} users to device {self.device.ip_address}")
            return True, f"Pushed {len(users)} users"
        except Exception as e:
            logger.error(f"Error pushing users to device {self.device.ip_address}: {e}")
            return False, f"Error pushing users: {e}"
        finally:
            self.disconnect()