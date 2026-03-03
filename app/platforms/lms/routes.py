"""FastAPI routes for LMS foundation."""
from fastapi import APIRouter
from app.platforms.lms.service import LmsService
from app.platforms.lms.quizzes import grade
from app.platforms.lms.certificates import generate_certificate

router=APIRouter(prefix='/platform/lms',tags=['platform-lms'])
svc=LmsService()

@router.post('/courses/{course_id}')
def create_course(course_id:str,payload:dict)->dict:
    return svc.courses.create(course_id,payload['title'],payload.get('instructor','unknown'))

@router.post('/enroll/{user_id}/{course_id}')
def enroll(user_id:str,course_id:str)->dict:
    return svc.enrollment.enroll(user_id,course_id)

@router.post('/quiz/grade')
def grade_quiz(payload:dict)->dict:
    return grade(payload.get('correct',[]),payload.get('answers',[]))

@router.get('/certificate/{user_id}/{course_id}')
def cert(user_id:str,course_id:str)->dict:
    return generate_certificate(user_id,course_id)
