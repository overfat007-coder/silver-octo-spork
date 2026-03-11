from app.enterprise.project.core import ProjectService
from app.enterprise.project.agile import velocity


def test_project_and_agile() -> None:
    svc=ProjectService()
    svc.create('p1','Proj')
    svc.add_task('p1','t1')
    assert len(svc.projects['p1']['tasks'])==1
    assert velocity([3,5])==4.0
