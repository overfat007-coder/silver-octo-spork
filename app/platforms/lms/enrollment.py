"""Enrollment and progress tracking."""

class EnrollmentService:
    def __init__(self)->None:
        self.enrollments:dict[tuple[str,str],dict]={}

    def enroll(self,user_id:str,course_id:str)->dict:
        rec={"user_id":user_id,"course_id":course_id,"progress":0.0,"completed":False}
        self.enrollments[(user_id,course_id)]=rec
        return rec

    def set_progress(self,user_id:str,course_id:str,progress:float)->dict:
        rec=self.enrollments[(user_id,course_id)]
        rec['progress']=max(0.0,min(100.0,progress))
        rec['completed']=rec['progress']>=100.0
        return rec
