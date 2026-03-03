"""Campaign execution helpers."""

def launch_campaign(name:str,audience_size:int)->dict:
    return {"name":name,"audience_size":audience_size,"status":"running"}
