from app.enterprise.marketing.analytics import conversion_rate
from app.enterprise.marketing.contacts import ContactService


def test_marketing_contacts() -> None:
    svc=ContactService()
    svc.upsert('u1','u@example.com')
    assert svc.contacts['u1']['email']=='u@example.com'
    assert conversion_rate(5,20)==25.0
