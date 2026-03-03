"""Gamification points and badges."""

class GamificationService:
    def __init__(self)->None:
        self.points:dict[str,int]={}

    def add_points(self,user_id:str,delta:int)->int:
        self.points[user_id]=self.points.get(user_id,0)+delta
        return self.points[user_id]

    def badge_for(self,user_id:str)->str:
        pts=self.points.get(user_id,0)
        return 'gold' if pts>=100 else 'silver' if pts>=50 else 'bronze'
