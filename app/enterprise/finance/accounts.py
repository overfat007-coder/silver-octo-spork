"""Chart of accounts and balances."""

class Ledger:
    def __init__(self)->None:
        self.accounts: dict[str,float] = {}

    def open_account(self,code:str)->None:
        self.accounts.setdefault(code,0.0)

    def post(self,code:str,amount:float)->float:
        self.open_account(code)
        self.accounts[code]+=amount
        return self.accounts[code]
