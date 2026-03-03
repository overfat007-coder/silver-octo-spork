"""Patient profile and EMR base service."""

class PatientService:
    def __init__(self)->None:
        self.patients: dict[str,dict]={}

    def upsert(self,patient_id:str,name:str)->dict:
        p={"patient_id":patient_id,"name":name,"allergies":[]}
        self.patients[patient_id]=p
        return p
