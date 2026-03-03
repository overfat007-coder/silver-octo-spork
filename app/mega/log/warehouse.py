"""Warehouse stock operations."""

class WarehouseService:
    def __init__(self)->None:
        self.stock: dict[str,int]={}

    def receive(self,sku:str,qty:int)->int:
        self.stock[sku]=self.stock.get(sku,0)+qty
        return self.stock[sku]
