from peewee import SqliteDatabase, Model, AutoField, IntegerField, CharField, DateTimeField, ForeignKeyField, TextField
import datetime

# Initialize database
db = SqliteDatabase('attendance.db')

class BaseModel(Model):
    class Meta:
        database = db

class Device(BaseModel):
    id = AutoField()
    ip_address = CharField(max_length=15, help_text='IPv4 address of the device')
    port = IntegerField(default=4370)
    password = CharField(max_length=32, default='0')
    device_model = CharField(max_length=50)
    status = CharField(max_length=20, default="Offline")
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'devices'

class User(BaseModel):
    uid = IntegerField(primary_key=True)
    name = CharField(max_length=100)
    role = IntegerField(help_text='Privilege level on the device')
    password = CharField(max_length=128, null=True)
    group_id = IntegerField(null=True)
    user_id = CharField(max_length=50, unique=True, help_text='Application-specific user ID')
    card = CharField(max_length=50, null=True, help_text='ID card number if applicable')
    user_cloud_id = IntegerField(null=True, help_text='Link to user record in cloud')
    device = ForeignKeyField(Device, backref='users', null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'users'

class Attendance(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref='attendances')
    timestamp = DateTimeField()
    status = CharField(max_length=20, help_text='Attendance status code')
    punch = CharField(max_length=20, help_text='Punch type (e.g., IN, OUT)')
    uid = IntegerField(null=True, help_text='Device-specific user identifier at punch')
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'attendance_logs'

class Settings(BaseModel):
    id = AutoField()
    key = CharField(max_length=50, unique=True)
    value = TextField()  # Store JSON string

    class Meta:
        table_name = 'settings'

def init_db():
    db.connect()
    db.create_tables([Device, User, Attendance, Settings], safe=True)