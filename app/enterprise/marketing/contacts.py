"""Contact and segment management primitives."""

class ContactService:
    def __init__(self)->None:
        self.contacts: dict[str,dict] = {}

    def upsert(self,contact_id:str,email:str)->dict:
        c={"contact_id":contact_id,"email":email,"tags":[]}
        self.contacts[contact_id]=c
        return c
