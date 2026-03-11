"""Document lifecycle and metadata service."""

class DmsService:
    def __init__(self)->None:
        self.docs: dict[str,dict]={}

    def create(self,doc_id:str,title:str,doc_type:str)->dict:
        d={"doc_id":doc_id,"title":title,"type":doc_type,"version":1,"status":"draft"}
        self.docs[doc_id]=d
        return d

    def bump_version(self,doc_id:str)->dict:
        self.docs[doc_id]["version"] += 1
        return self.docs[doc_id]
