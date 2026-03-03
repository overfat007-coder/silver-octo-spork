"""Main e-commerce service combining catalog/cart/order/payment."""
from app.platforms.ecommerce.catalog import CatalogService
from app.platforms.ecommerce.cart import CartService
from app.platforms.ecommerce.orders import OrderService
from app.platforms.ecommerce.payments import charge
from app.platforms.ecommerce.promotions import apply_percent

class EcommerceService:
    def __init__(self)->None:
        self.catalog=CatalogService()
        self.cart=CartService()
        self.orders=OrderService()

    def checkout(self,order_id:str,user_id:str,discount_percent:float=0.0)->dict:
        items=self.cart.carts.get(user_id,{})
        total=0.0
        for sku,qty in items.items():
            p=self.catalog.products[sku]
            self.catalog.reserve(sku,qty)
            total += p['price']*qty
        total=apply_percent(total,discount_percent)
        order=self.orders.create(order_id,user_id,items,total)
        payment=charge(order_id,total)
        return {'order':order,'payment':payment}
