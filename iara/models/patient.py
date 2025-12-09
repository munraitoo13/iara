from typing import Optional

from pydantic import BaseModel

class PatientInfo(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    address: Optional[str] = None
    payer_name: Optional[str] = None
    insurance_id: Optional[str] = None
    chief_complaint: Optional[str] = None

class TranscriptItem(BaseModel):
    actor: str
    message: str
