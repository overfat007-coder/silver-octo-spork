"""Main LMS service facade."""
from app.platforms.lms.courses import CourseService
from app.platforms.lms.enrollment import EnrollmentService
from app.platforms.lms.gamification import GamificationService

class LmsService:
    def __init__(self)->None:
        self.courses=CourseService()
        self.enrollment=EnrollmentService()
        self.gamification=GamificationService()
