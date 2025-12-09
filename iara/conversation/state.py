from enum import Enum, auto
from typing import Optional, List

from pydantic import BaseModel, Field

class ConversationState(Enum):
    GATHERING_NAME = auto()
    GATHERING_DOB = auto()
    GATHERING_ADDRESS = auto()
    GATHERING_INSURANCE_PAYER = auto()
    GATHERING_INSURANCE_ID = auto()
    GATHERING_COMPLAINT = auto()
    CONFIRMATION = auto()
    END = auto()

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

class ConversationStateData(BaseModel):
    state: ConversationState = ConversationState.GATHERING_NAME
    patient_info: PatientInfo = Field(default_factory=PatientInfo)
    transcript: List[TranscriptItem] = Field(default_factory=list)
