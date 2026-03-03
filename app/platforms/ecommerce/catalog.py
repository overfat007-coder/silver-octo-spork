"""Catalog and inventory primitives."""

class CatalogService:
    def __init__(self)->None:
        self.products:dict[str,dict]={}

    def upsert_product(self,sku:str,name:str,price:float,stock:int)->dict:
        p={"sku":sku,"name":name,"price":price,"stock":stock}
        self.products[sku]=p
        return p

    def reserve(self,sku:str,qty:int)->None:
        p=self.products[sku]
        if p['stock']<qty:
            raise ValueError('insufficient stock')
        p['stock']-=qty
