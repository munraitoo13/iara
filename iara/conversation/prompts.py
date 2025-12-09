from conversation.state import ConversationState

VALIDATION_PROMPTS = {
    ConversationState.GATHERING_DOB: (
        "The user provided their name as: {user_input}.\n"
        "Please confirm if this is a valid name.\n"
        "Respond ONLY with 'valid' or 'invalid' and provide a brief explanation.\n"
        "Examples:\n"
        "- 'Jhon Doe' -> valid\n"
        "- '12345' -> invalid, names cannot contain numbers.\n"
        "- 'None' -> invalid, name cannot be empty.\n"
        "- 'idk' -> invalid, please provide a valid name."
    ),
    ConversationState.GATHERING_ADDRESS: (
        "The user provided their date of birth as: {user_input}.\n"
        "Please confirm if this is a valid date of birth in MM/DD/YYYY format.\n"
        "Respond ONLY with 'valid' or 'invalid' and provide a brief explanation.\n"
        "Examples:\n"
        "- '01/15/1990' -> valid\n"
        "- '1990-01-15' -> invalid, please use MM/DD/YYYY format.\n"
        "- '15/01/1990' -> invalid, month must come first.\n"
        "- 'abcd' -> invalid, please provide a valid date."
    ),
    ConversationState.GATHERING_INSURANCE_PAYER: (
        "The user provided their address as: {user_input}.\n"
        "Please confirm if this is a valid address.\n"
        "Respond ONLY with 'valid' or 'invalid' and provide a brief explanation.\n"
        "Examples:\n"
        "- '123 Main St, Springfield, IL 62701' -> valid\n"
        "- 'Unknown' -> invalid, address cannot be empty.\n"
        "- '123' -> invalid, please provide a full address including street, city, state, and zip code."
    ),
    ConversationState.GATHERING_INSURANCE_ID: (
        "The user provided their insurance payer name as: {user_input}.\n"
        "Please confirm if this is a valid insurance payer name.\n"
        "Respond ONLY with 'valid' or 'invalid' and provide a brief explanation.\n"
        "Examples:\n"
        "- 'Blue Cross Blue Shield' -> valid\n"
        "- '12345' -> invalid, payer names cannot be just numbers.\n"
        "- 'None' -> invalid, please provide a valid payer name."
    ),
    ConversationState.GATHERING_COMPLAINT: (
        "The user provided their insurance ID as: {user_input}.\n"
        "Please confirm if this is a valid insurance ID.\n"
        "Respond ONLY with 'valid' or 'invalid' and provide a brief explanation.\n"
        "Examples:\n"
        "- 'A123456789' -> valid\n"
        "- '123' -> invalid, insurance IDs are typically longer.\n"
        "- 'abcd' -> invalid, please provide a valid insurance ID."
    ),
}

PROMPT_BY_STATE = {
    ConversationState.GATHERING_DOB: (
        "The user said their name is {user_input}.\n"
        "Now, ask for their date of birth."
        "Keep it brief (1-2 sentences)."
    ),
    ConversationState.GATHERING_ADDRESS: (
        "The user said their date of birth is {user_input}.\n"
        "Now, ask for their address (street, city, state, zip)."
        "Keep it brief (1-2 sentences)."
    ),
    ConversationState.GATHERING_INSURANCE_PAYER: (
        "The user said their address is {user_input}.\n"
        "Now, ask for their insurance payer name."
        "Keep it brief (1-2 sentences)."
    ),
    ConversationState.GATHERING_INSURANCE_ID: (
        "The user said their insurance payer name is {user_input}.\n"
        "Now, ask for their insurance ID."
        "Keep it brief (1-2 sentences)."
    ),
    ConversationState.GATHERING_COMPLAINT: (
        "The user said their insurance ID is {user_input}.\n"
        "Now, ask for their chief complaint or reason for visit."
        "Keep it brief (1-2 sentences)."
    ),
}

RETRY_MESSAGES = {
    ConversationState.GATHERING_DOB: "please, provide a valid name.",
    ConversationState.GATHERING_ADDRESS: "please, provide a valid date of birth in MM/DD/YYYY format.",
    ConversationState.GATHERING_INSURANCE_PAYER: "please, provide a valid address (street, city, state, and zip code).",
    ConversationState.GATHERING_INSURANCE_ID: "please, provide a valid insurance payer name.",
    ConversationState.GATHERING_COMPLAINT: "please, provide a valid insurance ID.",
}

SYSTEM_PROMPT = """
You are an AI-powered conversational chat agent for Assort Health. Your role is to collect patient appointment information in a friendly and conversational manner, similar to a live human representative.

Your goal is to collect the following information, one piece at a time:
1. Patient's full name
2. Patient's date of birth
3. Address (street, city, state, zip)
4. Payer name for insurance
5. Insurance ID
6. Chief complaint/reason for visit

Once you have collected all the information, you will be provided with a list of available appointments to present to the user. After the user selects an appointment, you will confirm all the details with them.

Please be conversational and handle various user inputs gracefully. If the user provides information you weren't asking for, acknowledge it and continue with the current step.
"""
