"""Order creation and status transitions."""

class OrderService:
    def __init__(self)->None:
        self.orders:dict[str,dict]={}

    def create(self,order_id:str,user_id:str,items:dict[str,int],total:float)->dict:
        o={"order_id":order_id,"user_id":user_id,"items":items,"total":total,"status":"created"}
        self.orders[order_id]=o
        return o

    def set_status(self,order_id:str,status:str)->dict:
        self.orders[order_id]['status']=status
        return self.orders[order_id]
