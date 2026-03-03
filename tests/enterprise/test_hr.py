from app.enterprise.hr.recruiting import RecruitingService
from app.enterprise.hr.analytics import turnover_rate


def test_hr_recruiting() -> None:
    svc=RecruitingService()
    svc.add_candidate('c1','Ann')
    svc.move_stage('c1','interview')
    assert svc.candidates['c1']['stage']=='interview'
    assert turnover_rate(2,20)==10.0
