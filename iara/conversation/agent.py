from iara.conversation.prompts import PROMPT_BY_STATE, RETRY_MESSAGES, VALIDATION_PROMPTS
from iara.conversation.state import ConversationStateData, TranscriptItem, ConversationState
from iara.services.gemini_service import GeminiService



class Agent:
    def __init__(self):
        """Initialize the Agent with necessary services and conversation state."""
        
        self.gemini_service = GeminiService()
        self.maps_service = None  # placeholder maps api
        self.state = ConversationStateData()

    def respond(self, user_input: str) -> str:
        """Generate a response based on the current conversation state and user input."""

        self.state.transcript.append(TranscriptItem(actor="user", message=user_input))
        response = self._respond_by_state(self.state.state)
        self.state.transcript.append(TranscriptItem(actor="agent", message=response))

        return response
    
    def _validate_response(self, state: ConversationState, user_input: str) -> tuple[bool, str]:
        """Validate user input based on the current conversation state."""

        if state not in VALIDATION_PROMPTS:
            return True, ""
        validation_response = self.gemini_service.generate_response(VALIDATION_PROMPTS[state].format(user_input=user_input))
        if validation_response.lower().startswith("valid"):
            return True, ""
        else:
            return False, validation_response
        
    def _retry_message(self, state: ConversationState, reason: str) -> str:
        base_msg = RETRY_MESSAGES.get(state, "I need valid information to proceed.")

        if reason:
            return f"I understand, but {base_msg}"
    
        return base_msg

    def _prompt_by_state(self, state: ConversationState, user_input: str) -> str:
        return PROMPT_BY_STATE.get(state).format(user_input=user_input)

    def _respond_by_state(self, state: ConversationState) -> str:
        user_input = self.state.transcript[-1].message

        match state:
            case ConversationState.GATHERING_NAME:
                response = "What is your name?"
                self.state.state = ConversationState.GATHERING_DOB
            case ConversationState.GATHERING_DOB:
                is_valid, reason = self._validate_response(state, user_input)
                if not is_valid:
                    return self._retry_message(state, reason)
                else:
                    self.state.patient_info.full_name = user_input
                    prompt = self._prompt_by_state(state, user_input)
                    response = self.gemini_service.generate_response(prompt)
                    self.state.state = ConversationState.GATHERING_ADDRESS
            case ConversationState.GATHERING_ADDRESS:
                is_valid, reason = self._validate_response(state, user_input)
                if not is_valid:
                    return self._retry_message(state, reason)
                else:
                    self.state.patient_info.date_of_birth = user_input
                    prompt = self._prompt_by_state(state, user_input)
                    response = self.gemini_service.generate_response(prompt)
                    self.state.state = ConversationState.GATHERING_INSURANCE_PAYER
            case ConversationState.GATHERING_INSURANCE_PAYER:
                is_valid, reason = self._validate_response(state, user_input)
                if not is_valid:
                    return self._retry_message(state, reason)
                else:
                    self.state.patient_info.address = user_input
                    prompt = self._prompt_by_state(state, user_input)
                    response = self.gemini_service.generate_response(prompt)
                    self.state.state = ConversationState.GATHERING_INSURANCE_ID
            case ConversationState.GATHERING_INSURANCE_ID:
                is_valid, reason = self._validate_response(state, user_input)
                if not is_valid:
                    return self._retry_message(state, reason)
                else:
                    self.state.patient_info.payer_name = user_input
                    prompt = self._prompt_by_state(state, user_input)
                    response = self.gemini_service.generate_response(prompt)
                    self.state.state = ConversationState.GATHERING_COMPLAINT
            case ConversationState.GATHERING_COMPLAINT:
                is_valid, reason = self._validate_response(state, user_input)
                if not is_valid:
                    return self._retry_message(state, reason)
                else:
                    self.state.patient_info.insurance_id = user_input
                    prompt = self._prompt_by_state(state, user_input)
                    response = self.gemini_service.generate_response(prompt)
                    self.state.state = ConversationState.CONFIRMATION
            case ConversationState.CONFIRMATION:
                is_valid, reason = self._validate_response(state, user_input)
                if not is_valid:
                    return self._retry_message(state, reason)
                else:
                    self.state.patient_info.chief_complaint = user_input
                    response = (
                        "Thank you for the information. Please confirm that all details are correct:\n"
                        f"Name: {self.state.patient_info.full_name}\n"
                        f"DOB: {self.state.patient_info.date_of_birth}\n"
                        f"Address: {self.state.patient_info.address}\n"
                        f"Insurance Payer: {self.state.patient_info.payer_name}\n"
                        f"Insurance ID: {self.state.patient_info.insurance_id}\n"
                        f"Chief Complaint: {self.state.patient_info.chief_complaint}\n"
                        "Is this information correct? (yes/no)"
                    )
                    self.state.state = ConversationState.END    
            case ConversationState.END:
                response = "Thank you! Your information has been recorded."
            case _:
                response = "I'm sorry, something went wrong."

        return response

