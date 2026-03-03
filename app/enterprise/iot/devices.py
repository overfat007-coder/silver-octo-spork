"""Device registry and shadow state."""

class DeviceRegistry:
    def __init__(self)->None:
        self.devices: dict[str,dict] = {}

    def register(self,device_id:str,kind:str)->dict:
        d={"device_id":device_id,"kind":kind,"status":"active","shadow":{}}
        self.devices[device_id]=d
        return d

    def shadow_update(self,device_id:str,payload:dict)->dict:
        self.devices[device_id]["shadow"].update(payload)
        return self.devices[device_id]
