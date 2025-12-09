from iara.config import settings

from typing import List

from google import genai
from google.genai import types

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


class GeminiService:
    def __init__(self, api_key: str = settings.gemini_api_key):
        """Initialize the GeminiService with the provided API key."""
        self.client = genai.Client(api_key=api_key)
        self.config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=1.0,
        )
        self.chat = None
        self._start_new_chat()

    def _start_new_chat(self):
        """Start a new chat session with the Gemini model."""
        self.chat = self.client.chats.create(
            config=self.config, model="gemini-2.5-flash-lite"
        )

    def generate_response(self, prompt: str) -> str:
        """Generate a response from the Gemini model based on the given prompt."""
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def reset_chat(self):
        """Reset the current chat session."""
        self._start_new_chat()

    def get_history(self) -> List[str]:
        """Retrieve the chat history as a list of messages."""
        return self.chat.get_history() if self.chat else []
