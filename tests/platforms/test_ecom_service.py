from app.platforms.ecommerce.service import EcommerceService


def test_ecom_checkout_flow() -> None:
    svc=EcommerceService()
    svc.catalog.upsert_product('sku1','Phone',100.0,5)
    svc.cart.add('u1','sku1',2)
    out=svc.checkout('o1','u1',10)
    assert out['order']['total']==180.0
    assert out['payment']['status']=='captured'
