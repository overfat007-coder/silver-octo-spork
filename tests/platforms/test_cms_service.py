from app.platforms.cms.service import CmsService


def test_cms_create_update_workflow() -> None:
    svc=CmsService()
    svc.register_type('article',{'title':'text'})
    e=svc.create_entry('e1','article',{'title':'Hello'})
    assert e.version==1
    svc.update_entry('e1',{'title':'Hello2'})
    assert svc.entries['e1'].version==2
    svc.set_status('e1','review')
    assert svc.entries['e1'].status=='review'
