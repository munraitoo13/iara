from iara.config import settings
from iara.conversation.prompts import SYSTEM_PROMPT

from typing import List

from google import genai
from google.genai import types

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
