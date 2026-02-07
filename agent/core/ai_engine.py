"""AI Agent Core Engine"""
import os
import json
import requests
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Message:
    """Message data structure"""
    role: str  # "user" or "assistant"
    content: str


class AIEngine:
    """Core AI Engine for handling API calls"""

    def __init__(self):
        self.api_base_url = os.getenv("API_BASE_URL", "https://yunwu.ai")
        self.api_key = os.getenv("API_KEY")
        self.model = os.getenv("API_MODEL", "gpt-4")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4096"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))

        if not self.api_key:
            raise ValueError("API_KEY not found in environment variables")

        self.conversation_history: List[Message] = []

    def add_message(self, role: str, content: str) -> None:
        """Add message to conversation history"""
        self.conversation_history.append(Message(role=role, content=content))

    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []

    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history in API format"""
        return [
            {"role": msg.role, "content": msg.content}
            for msg in self.conversation_history
        ]

    def call_api(self, user_message: str, system_prompt: Optional[str] = None) -> str:
        """Call AI API and get response"""
        self.add_message("user", user_message)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        messages = self.get_history()

        # Add system prompt if provided
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }

        try:
            response = requests.post(
                f"{self.api_base_url}/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            result = response.json()
            assistant_message = result["choices"][0]["message"]["content"]
            self.add_message("assistant", assistant_message)

            return assistant_message

        except requests.exceptions.RequestException as e:
            error_msg = f"API Error: {str(e)}"
            self.add_message("assistant", error_msg)
            return error_msg

    def process_with_tools(self, user_message: str, available_tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process message with tool availability information"""
        tools_descriptions = "\n".join([
            f"- {tool['name']}: {tool['description']}\n  Parameters: {tool['params']}"
            for tool in available_tools
        ])

        system_prompt = f"""You are an AI assistant with access to system tools. You can execute commands and perform actions.

Available tools:
{tools_descriptions}

When you need to use a tool, respond ONLY with a JSON object in this exact format:
{{"tool": "tool_name", "params": {{"param1": "value1", "param2": "value2"}}}}

If the user asks a question that doesn't require tools, respond normally.
If you need to use multiple tools, respond with one tool call at a time."""

        response = self.call_api(user_message, system_prompt)

        # Try to parse as JSON action
        try:
            if response.strip().startswith("{"):
                action = json.loads(response)
                if "tool" in action:
                    return {"type": "tool_call", "data": action}
        except json.JSONDecodeError:
            pass

        return {"type": "response", "data": response}
