from iara.models.patient import PatientInfo, TranscriptItem

from enum import Enum, auto
from typing import List

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

class ConversationStateData(BaseModel):
    state: ConversationState = ConversationState.GATHERING_NAME
    patient_info: PatientInfo = Field(default_factory=PatientInfo)
    transcript: List[TranscriptItem] = Field(default_factory=list)
