from app.platforms.lms.service import LmsService
from app.platforms.lms.quizzes import grade


def test_lms_enrollment_and_progress() -> None:
    svc=LmsService()
    svc.courses.create('c1','Python','teacher')
    svc.enrollment.enroll('u1','c1')
    rec=svc.enrollment.set_progress('u1','c1',100)
    assert rec['completed'] is True


def test_quiz_grade() -> None:
    result=grade(['a','b'],['a','x'])
    assert result['percent']==50.0
