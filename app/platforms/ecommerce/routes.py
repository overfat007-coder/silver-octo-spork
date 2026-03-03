"""FastAPI routes for e-commerce foundation."""
from fastapi import APIRouter, HTTPException
from app.platforms.ecommerce.service import EcommerceService

router=APIRouter(prefix='/platform/ecom',tags=['platform-ecom'])
svc=EcommerceService()

@router.post('/products/{sku}')
def put_product(sku:str,payload:dict)->dict:
    return svc.catalog.upsert_product(sku,payload['name'],float(payload['price']),int(payload.get('stock',0)))

@router.post('/cart/{user_id}/{sku}/{qty}')
def add_cart(user_id:str,sku:str,qty:int)->dict:
    return svc.cart.add(user_id,sku,qty)

@router.post('/checkout/{order_id}/{user_id}')
def checkout(order_id:str,user_id:str,payload:dict|None=None)->dict:
    payload=payload or {}
    try:
        return svc.checkout(order_id,user_id,float(payload.get('discount_percent',0.0)))
    except (KeyError,ValueError) as exc:
        raise HTTPException(status_code=400,detail=str(exc)) from exc
