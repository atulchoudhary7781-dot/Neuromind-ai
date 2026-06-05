"""
NeuroMind AI — Core AI Engine
==============================
Handles all interactions with the Anthropic Claude API.
Supports multi-turn conversations, image analysis, and streaming.

Author: NeuroMind AI Team
"""

import base64
import time
from pathlib import Path
from typing import Generator

import anthropic

from config import APP_CONFIG, MODEL_CONFIG, SYSTEM_PROMPTS


class NeuroMindAI:
    """
    Core AI engine for NeuroMind AI.

    Wraps the Anthropic Claude API with conversation memory,
    multi-modal support, and clean error handling.

    Example:
        >>> ai = NeuroMindAI()
        >>> response = ai.chat("Explain quantum computing")
        >>> print(response)
    """

    def __init__(self, mode: str = "chat"):
        """
        Initialize the AI engine.

        Args:
            mode: One of 'chat', 'document_qa', 'data_analyst',
                  'image_analyst', 'code_assistant'
        """
        if not APP_CONFIG.api_key:
            raise ValueError(
                "❌ ANTHROPIC_API_KEY not found!\n"
                "Please set it in your .env file.\n"
                "Get your key at: https://console.anthropic.com"
            )

        self.client = anthropic.Anthropic(api_key=APP_CONFIG.api_key)
        self.model = MODEL_CONFIG.name
        self.max_tokens = MODEL_CONFIG.max_tokens
        self.mode = mode
        self.system_prompt = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["chat"])
        self.conversation_history: list[dict] = []
        self._total_tokens_used: int = 0

    # ── Public Interface ─────────────────────────────────────────────────────

    def chat(self, user_message: str, context: str = "") -> str:
        """
        Send a message and get a response.

        Args:
            user_message: The user's input message
            context: Optional additional context (e.g., document content)

        Returns:
            The AI's response as a string
        """
        full_message = f"{context}\n\n{user_message}" if context else user_message

        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": full_message
        })

        # Trim history if too long
        self._trim_history()

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=self.system_prompt,
                messages=self.conversation_history
            )

            assistant_message = response.content[0].text
            self._total_tokens_used += response.usage.input_tokens + response.usage.output_tokens

            # Save assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except anthropic.AuthenticationError:
            raise ValueError("❌ Invalid API key. Please check your ANTHROPIC_API_KEY.")
        except anthropic.RateLimitError:
            raise RuntimeError("⏳ Rate limit reached. Please wait a moment and try again.")
        except anthropic.APIError as e:
            raise RuntimeError(f"🔧 API error: {str(e)}")

    def chat_with_image(self, user_message: str, image_path: str) -> str:
        """
        Send a message with an image for visual analysis.

        Args:
            user_message: The user's question about the image
            image_path: Path to the image file

        Returns:
            AI's analysis of the image
        """
        image_data, media_type = self._encode_image(image_path)

        message_content = [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": image_data,
                },
            },
            {
                "type": "text",
                "text": user_message
            }
        ]

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=SYSTEM_PROMPTS["image_analyst"],
                messages=[{"role": "user", "content": message_content}]
            )

            return response.content[0].text

        except Exception as e:
            raise RuntimeError(f"Image analysis failed: {str(e)}")

    def chat_with_image_bytes(self, user_message: str, image_bytes: bytes, media_type: str = "image/png") -> str:
        """
        Send a message with image bytes (from file upload).

        Args:
            user_message: The question about the image
            image_bytes: Raw image bytes
            media_type: MIME type of the image

        Returns:
            AI's analysis
        """
        image_data = base64.standard_b64encode(image_bytes).decode("utf-8")

        message_content = [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": image_data,
                },
            },
            {"type": "text", "text": user_message}
        ]

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=SYSTEM_PROMPTS["image_analyst"],
            messages=[{"role": "user", "content": message_content}]
        )

        return response.content[0].text

    def quick_ask(self, prompt: str, system: str = "") -> str:
        """
        One-shot question without conversation history.
        Useful for analysis tasks.

        Args:
            prompt: The prompt to send
            system: Optional system prompt override

        Returns:
            AI response string
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system or self.system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def clear_history(self) -> None:
        """Reset conversation history."""
        self.conversation_history = []

    def get_history(self) -> list[dict]:
        """Get the full conversation history."""
        return self.conversation_history.copy()

    def get_stats(self) -> dict:
        """Get usage statistics."""
        return {
            "total_messages": len(self.conversation_history),
            "total_tokens_used": self._total_tokens_used,
            "model": self.model,
            "mode": self.mode,
        }

    def set_mode(self, mode: str) -> None:
        """Switch AI mode and update system prompt."""
        self.mode = mode
        self.system_prompt = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["chat"])

    # ── Private Helpers ──────────────────────────────────────────────────────

    def _trim_history(self) -> None:
        """Keep conversation history within token limits."""
        max_turns = APP_CONFIG.max_memory_turns * 2  # Each turn = user + assistant
        if len(self.conversation_history) > max_turns:
            # Keep the most recent turns
            self.conversation_history = self.conversation_history[-max_turns:]

    def _encode_image(self, image_path: str) -> tuple[str, str]:
        """Encode an image file to base64."""
        path = Path(image_path)
        suffix = path.suffix.lower()

        media_type_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }

        media_type = media_type_map.get(suffix, "image/png")

        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode("utf-8")

        return image_data, media_type
