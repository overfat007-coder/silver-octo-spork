"""Routes for telemedicine foundation."""
from fastapi import APIRouter
from app.mega.med.patient import PatientService
from app.mega.med.appointment import AppointmentService

router=APIRouter(prefix="/mega/med",tags=["mega-med"])
patients=PatientService()
appointments=AppointmentService()

@router.post("/patients/{patient_id}")
def upsert_patient(patient_id:str,payload:dict)->dict:
    return patients.upsert(patient_id,payload.get("name",patient_id))

@router.post("/appointments/{appointment_id}")
def book_appointment(appointment_id:str,payload:dict)->dict:
    return appointments.book(appointment_id,payload["patient_id"],payload["doctor_id"],payload["slot"])
