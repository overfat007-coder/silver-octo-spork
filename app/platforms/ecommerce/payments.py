"""Payment providers abstraction."""

def charge(order_id:str,amount:float,provider:str='stripe')->dict:
    if amount<=0:
        raise ValueError('amount must be positive')
    return {'order_id':order_id,'provider':provider,'amount':amount,'status':'captured'}
