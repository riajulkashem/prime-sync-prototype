from db.database import Device

class DeviceLogic:
    def __init__(self, page_size=100):
        self.page_size = page_size
        self.current_page = 1
        self.devices = []
        self.total_count = 0
        self.load_page(1)

    def load_page(self, page):
        self.current_page = page
        offset = (page - 1) * self.page_size
        self.devices = list(Device.select(
            Device.id, Device.device_model, Device.ip_address, Device.port, Device.password
        ).offset(offset).limit(self.page_size))
        self.total_count = Device.select().count()

    def get_page(self):
        return self.devices, self.current_page, (self.total_count + self.page_size - 1) // self.page_size

    def add_device(self, data):
        Device.create(
            ip_address=data["IP Address"],
            port=int(data["Port"]),
            password=data["Password"],
            device_model=data["Device Model"],
        )
        self.load_page(self.current_page)

    def edit_device(self, device_id, data):
        device = Device.get(Device.id == device_id)
        device.ip_address = data["IP Address"]
        device.port = int(data["Port"])
        device.password = data["Password"]
        device.device_model = data["Device Model"]
        device.save()
        self.load_page(self.current_page)

    def delete_device(self, device_id):
        device = Device.get(Device.id == device_id)
        device.delete_instance()
        self.load_page(self.current_page)

    def filter_devices(self, search_text):
        search_text = search_text.lower()
        query = Device.select(
            Device.id, Device.device_model, Device.ip_address, Device.port, Device.password
        ).where(
            (Device.ip_address.contains(search_text)) | (Device.device_model.contains(search_text))
        )
        offset = (self.current_page - 1) * self.page_size
        filtered_devices = list(query.offset(offset).limit(self.page_size))
        filtered_count = query.count()
        return filtered_devices, self.current_page, (filtered_count + self.page_size - 1) // self.page_size