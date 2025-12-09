from iara.conversation.state import ConversationStateData, TranscriptItem, ConversationState

from iara.services.gemini_service import GeminiService


class Agent:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.maps_service = None  # Placeholder for MapsService initialization
        self.state = ConversationStateData()

    def respond(self, user_input: str) -> str:
        self.state.transcript.append(TranscriptItem(actor="user", message=user_input))
        response = self._respond_by_state(self.state.state)
        self.state.transcript.append(TranscriptItem(actor="agent", message=response))
        return response
    
    def _validate_response(self, state: ConversationState, user_input: str) -> tuple[bool, str]:
        """Validate user input based on the current conversation state."""

        validation_prompts = {
            ConversationState.GATHERING_DOB: (
                f"The user provided their name as: {user_input}.\n"
                "Please confirm if this is a valid name.\n"
                "Respond ONLY with 'valid' or 'invalid' and provide a brief explanation.\n"
                "Examples:\n"
                "- 'Jhon Doe' -> valid\n"
                "- '12345' -> invalid, names cannot contain numbers.\n"
                "- 'None' -> invalid, name cannot be empty.\n"
                "- 'idk' -> invalid, please provide a valid name."
            ),
            ConversationState.GATHERING_ADDRESS: (
                f"The user provided their date of birth as: {user_input}.\n"
                "Please confirm if this is a valid date of birth in MM/DD/YYYY format.\n"
                "Respond ONLY with 'valid' or 'invalid' and provide a brief explanation.\n"
                "Examples:\n"
                "- '01/15/1990' -> valid\n"
                "- '1990-01-15' -> invalid, please use MM/DD/YYYY format.\n"
                "- '15/01/1990' -> invalid, month must come first.\n"
                "- 'abcd' -> invalid, please provide a valid date."
            ),
            ConversationState.GATHERING_INSURANCE_PAYER: (
                f"The user provided their address as: {user_input}.\n"
                "Please confirm if this is a valid address.\n"
                "Respond ONLY with 'valid' or 'invalid' and provide a brief explanation.\n"
                "Examples:\n"
                "- '123 Main St, Springfield, IL 62701' -> valid\n"
                "- 'Unknown' -> invalid, address cannot be empty.\n"
                "- '123' -> invalid, please provide a full address including street, city, state, and zip code."
            ),
            ConversationState.GATHERING_INSURANCE_ID: (
                f"The user provided their insurance payer name as: {user_input}.\n"
                "Please confirm if this is a valid insurance payer name.\n"
                "Respond ONLY with 'valid' or 'invalid' and provide a brief explanation.\n"
                "Examples:\n"
                "- 'Blue Cross Blue Shield' -> valid\n"
                "- '12345' -> invalid, payer names cannot be just numbers.\n"
                "- 'None' -> invalid, please provide a valid payer name."
            ),
            ConversationState.GATHERING_COMPLAINT: (
                f"The user provided their insurance ID as: {user_input}.\n"
                "Please confirm if this is a valid insurance ID.\n"
                "Respond ONLY with 'valid' or 'invalid' and provide a brief explanation.\n"
                "Examples:\n"
                "- 'A123456789' -> valid\n"
                "- '123' -> invalid, insurance IDs are typically longer.\n"
                "- 'abcd' -> invalid, please provide a valid insurance ID."
            ),
        }

        if state not in validation_prompts:
            return True, ""
        
        validation_response = self.gemini_service.generate_response(validation_prompts[state])
        if validation_response.lower().startswith("valid"):
            return True, ""
        else:
            return False, validation_response
        
    def _retry_message(self, state: ConversationState, reason: str) -> str:
        base_messages = {
            ConversationState.GATHERING_DOB: "please, provide a valid name.",
            ConversationState.GATHERING_ADDRESS: "please, provide a valid date of birth in MM/DD/YYYY format.",
            ConversationState.GATHERING_INSURANCE_PAYER: "please, provide a valid address (street, city, state, and zip code).",
            ConversationState.GATHERING_INSURANCE_ID: "please, provide a valid insurance payer name.",
            ConversationState.GATHERING_COMPLAINT: "please, provide a valid insurance ID.",
        }

        base_msg = base_messages.get(state, "I need valid information to proceed.")

        if reason:
            return f"I understand, but {base_msg}"
        
        return base_msg

    def _prompt_by_state(self, state: ConversationState, user_input: str) -> str:
        prompts = {
            ConversationState.GATHERING_DOB: (
                f"The user said their name is {user_input}.\n"
                "Now, ask for their date of birth."
                "Keep it brief (1-2 sentences)."
            ),
            ConversationState.GATHERING_ADDRESS: (
                f"The user said their date of birth is {user_input}.\n"
                "Now, ask for their address (street, city, state, zip)."
                "Keep it brief (1-2 sentences)."
            ),
            ConversationState.GATHERING_INSURANCE_PAYER: (
                f"The user said their address is {user_input}.\n"
                "Now, ask for their insurance payer name."
                "Keep it brief (1-2 sentences)."
            ),
            ConversationState.GATHERING_INSURANCE_ID: (
                f"The user said their insurance payer name is {user_input}.\n"
                "Now, ask for their insurance ID."
                "Keep it brief (1-2 sentences)."
            ),
            ConversationState.GATHERING_COMPLAINT: (
                f"The user said their insurance ID is {user_input}.\n"
                "Now, ask for their chief complaint or reason for visit."
                "Keep it brief (1-2 sentences)."
            ),
        }

        return prompts.get(state, user_input)

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

