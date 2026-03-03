from app.enterprise.finance.accounts import Ledger
from app.enterprise.finance.transactions import double_entry


def test_finance_ledger() -> None:
    l=Ledger()
    l.post('1000',100)
    l.post('1000',-40)
    assert l.accounts['1000']==60
    assert double_entry(10,10)
