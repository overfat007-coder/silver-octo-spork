"""Video consultation session helper."""


def start_session(session_id:str, patient_id:str, doctor_id:str)->dict:
    return {"session_id":session_id,"patient_id":patient_id,"doctor_id":doctor_id,"state":"active"}
