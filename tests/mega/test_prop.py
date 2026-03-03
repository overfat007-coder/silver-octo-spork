from app.mega.prop.market import price_per_sqm
from app.mega.prop.rent import rent_yield


def test_prop_metrics() -> None:
    assert price_per_sqm(1_000_000,50)==20000.0
    assert rent_yield(50_000,10_000_000)==6.0
