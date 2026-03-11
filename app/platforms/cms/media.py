"""CMS media and CDN metadata handling."""

def build_media_record(media_id:str, filename:str, cdn_base:str|None=None)->dict:
    url=f"{cdn_base.rstrip('/')}/{filename}" if cdn_base else f"/media/{filename}"
    return {"media_id":media_id,"filename":filename,"url":url}
