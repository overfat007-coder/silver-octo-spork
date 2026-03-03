"""Course management primitives."""

class CourseService:
    def __init__(self)->None:
        self.courses:dict[str,dict]={}

    def create(self,course_id:str,title:str,instructor:str)->dict:
        c={"course_id":course_id,"title":title,"instructor":instructor,"lessons":[]}
        self.courses[course_id]=c
        return c

    def add_lesson(self,course_id:str,lesson_id:str,title:str)->dict:
        lesson={"lesson_id":lesson_id,"title":title}
        self.courses[course_id]['lessons'].append(lesson)
        return lesson
