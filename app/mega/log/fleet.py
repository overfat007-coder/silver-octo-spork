"""Fleet and vehicle capacity service."""

class FleetService:
    def __init__(self)->None:
        self.vehicles: dict[str,dict]={}

    def add_vehicle(self,vehicle_id:str,capacity_kg:float)->dict:
        v={"vehicle_id":vehicle_id,"capacity_kg":capacity_kg,"status":"ready"}
        self.vehicles[vehicle_id]=v
        return v
