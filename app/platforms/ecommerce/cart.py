"""Cart operations."""

class CartService:
    def __init__(self)->None:
        self.carts:dict[str,dict[str,int]]={}

    def add(self,user_id:str,sku:str,qty:int)->dict:
        cart=self.carts.setdefault(user_id,{})
        cart[sku]=cart.get(sku,0)+qty
        return cart
