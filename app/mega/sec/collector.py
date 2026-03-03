"""Security event collection service."""

class SecurityCollector:
    def __init__(self)->None:
        self.events: list[dict]=[]

    def ingest(self,source:str,event_type:str,severity:str)->dict:
        e={"source":source,"event_type":event_type,"severity":severity}
        self.events.append(e)
        return e
