"""Main CMS service for content types, entries, workflow and versions."""
from app.platforms.cms.models import ContentType, ContentEntry
from app.platforms.cms.validation import validate_entry
from app.platforms.cms.versioning import snapshot
from app.platforms.cms.workflow import transit

class CmsService:
    def __init__(self)->None:
        self.types:dict[str,ContentType]={}
        self.entries:dict[str,ContentEntry]={}

    def register_type(self,name:str,fields:dict[str,str])->ContentType:
        ct=ContentType(name=name,fields=fields)
        self.types[name]=ct
        return ct

    def create_entry(self,entry_id:str,type_name:str,data:dict)->ContentEntry:
        ct=self.types[type_name]
        validate_entry(ct.fields,data)
        e=ContentEntry(entry_id=entry_id,type_name=type_name,data=data)
        e.history.append(snapshot(e.__dict__))
        self.entries[entry_id]=e
        return e

    def update_entry(self,entry_id:str,data:dict)->ContentEntry:
        e=self.entries[entry_id]
        e.version += 1
        e.data = data
        e.history.append(snapshot(e.__dict__))
        return e

    def set_status(self,entry_id:str,target:str)->ContentEntry:
        e=self.entries[entry_id]
        e.status=transit(e.status,target)
        e.version += 1
        e.history.append(snapshot(e.__dict__))
        return e
