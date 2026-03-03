"""Appointment scheduling service."""

class AppointmentService:
    def __init__(self)->None:
        self.items: dict[str,dict]={}

    def book(self,appointment_id:str,patient_id:str,doctor_id:str,slot:str)->dict:
        a={"appointment_id":appointment_id,"patient_id":patient_id,"doctor_id":doctor_id,"slot":slot,"status":"booked"}
        self.items[appointment_id]=a
        return a
