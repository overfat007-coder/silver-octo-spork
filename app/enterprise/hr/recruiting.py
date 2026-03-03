"""Recruiting pipeline primitives."""

class RecruitingService:
    def __init__(self)->None:
        self.candidates: dict[str,dict] = {}

    def add_candidate(self,candidate_id:str,name:str)->dict:
        c={"candidate_id":candidate_id,"name":name,"stage":"applied"}
        self.candidates[candidate_id]=c
        return c

    def move_stage(self,candidate_id:str,stage:str)->dict:
        self.candidates[candidate_id]["stage"]=stage
        return self.candidates[candidate_id]
