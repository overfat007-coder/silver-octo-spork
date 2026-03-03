"""Property registry service."""

class PropertyService:
    def __init__(self)->None:
        self.properties: dict[str,dict]={}

    def put(self,property_id:str,address:str,price:float)->dict:
        p={"property_id":property_id,"address":address,"price":price,"status":"listed"}
        self.properties[property_id]=p
        return p
