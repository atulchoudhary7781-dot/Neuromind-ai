"""
NeuroMind AI — Core AI Engine (Multi-Provider Support)
========================================================
Supports BOTH Anthropic Claude AND Groq APIs.

Providers:
- Anthropic: Uses anthropic SDK (sk-ant-* keys)
- Groq: Uses groq SDK (gsk_* keys) - FREE & FAST!

Author: NeuroMind AI Team
"""

import base64
import os
import time
from pathlib import Path
from typing import Generator, Optional

from .config import APP_CONFIG, MODEL_CONFIG, SYSTEM_PROMPTS


def _detect_provider(api_key: str) -> str:
    """Detect API provider from key format."""
    if api_key.startswith("gsk_"):
        return "groq"
    elif api_key.startswith("sk-ant-"):
        return "anthropic"
    else:
        # Default to anthropic for other formats
        return os.getenv("AI_PROVIDER", "anthropic")


class NeuroMindAI:
    """
    Core AI engine for NeuroMind AI - Multi-provider support!

    Supports:
    - Anthropic Claude (paid, powerful)
    - Groq (FREE, fast, Llama/Mixtral models)

    Example:
        >>> ai = NeuroMindAI()  # Auto-detects provider from key
        >>> response = ai.chat("Explain quantum computing")
        >>> print(response)
    """

    def __init__(self, mode: str = "chat", api_key: Optional[str] = None):
        """
        Initialize the AI engine.

        Args:
            mode: One of 'chat', 'document_qa', 'data_analyst',
                  'image_analyst', 'code_assistant'
            api_key: Optional API key (falls back to env/config)
        """
        self.api_key = api_key or APP_CONFIG.api_key or os.getenv("GROQ_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "❌ No API key found!\n"
                "Set GROQ_API_KEY or ANTHROPIC_API_KEY in:\n"
                "  - .env file\n"
                "  - Streamlit Cloud Secrets\n"
                "\nGet keys:\n"
                "  - Groq (FREE): https://console.groq.com/keys\n"
                "  - Anthropic: https://console.anthropic.com"
            )

        self.provider = _detect_provider(self.api_key)
        self.mode = mode
        self.system_prompt = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["chat"])
        self.conversation_history: list[dict] = []
        self._total_tokens_used: int = 0

        # Initialize appropriate client
        if self.provider == "groq":
            self._init_groq_client()
        else:
            self._init_anthropic_client()

    def _init_groq_client(self):
        """Initialize Groq client (FREE tier available!)."""
        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
            # Groq model mapping
            self.model = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
            self.max_tokens = int(os.getenv("MAX_TOKENS", "4096"))
            self.is_groq = True
            print(f"✅ Groq client initialized | Model: {self.model}")
        except ImportError:
            raise ImportError(
                "❌ Groq package not installed!\n"
                "Run: pip install groq\n"
                "Or use an Anthropic API key instead."
            )

    def _init_anthropic_client(self):
        """Initialize Anthropic client."""
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
            self.model = MODEL_CONFIG.name
            self.max_tokens = MODEL_CONFIG.max_tokens
            self.is_groq = False
            print(f"✅ Anthropic client initialized | Model: {self.model}")
        except ImportError:
            raise ImportError(
                "❌ Anthropic package not installed!\n"
                "Run: pip install anthropic\n"
                "Or use a Groq API key instead."
            )

    @property
    def provider_name(self) -> str:
        """Get human-readable provider name."""
        return "Groq (FREE)" if self.is_groq else "Anthropic"

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
            if self.is_groq:
                response = self._groq_chat()
            else:
                response = self._anthropic_chat()

            return response

        except Exception as e:
            error_msg = str(e).lower()
            if "auth" in error_msg or "invalid" in error_msg or "401" in error_msg:
                raise ValueError(f"❌ Invalid API key for {self.provider_name}. Please check your key.")
            elif "rate" in error_msg or "429" in error_msg:
                raise RuntimeError("⏳ Rate limit reached. Please wait a moment and try again.")
            else:
                raise RuntimeError(f"🔧 API error ({self.provider_name}): {str(e)}")

    def _anthropic_chat(self) -> str:
        """Chat using Anthropic API."""
        import anthropic
        
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

    def _groq_chat(self) -> str:
        """Chat using Groq API (OpenAI-compatible)."""
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[
                {"role": "system", "content": self.system_prompt},
                *self.conversation_history
            ]
        )

        assistant_message = response.choices[0].message.content
        self._total_tokens_used += response.usage.prompt_tokens + response.usage.completion_tokens

        # Save assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def chat_with_image(self, user_message: str, image_path: str) -> str:
        """
        Send a message with an image for visual analysis.
        
        Note: Image analysis works best with Anthropic/Vision models.
        Groq has limited vision support.
        """
        image_data, media_type = self._encode_image(image_path)

        if self.is_groq:
            # Groq vision (limited support)
            return self._groq_vision(user_message, image_data, media_type)
        else:
            return self._anthropic_vision(user_message, image_data, media_type)

    def _anthropic_vision(self, user_message: str, image_data: str, media_type: str) -> str:
        """Vision analysis using Anthropic."""
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

    def _groq_vision(self, user_message: str, image_data: str, media_type: str) -> str:
        """Vision analysis using Groq (if supported, otherwise text-only fallback)."""
        try:
            # Try vision-capable Groq model
            vision_model = os.getenv("GROQ_VISION_MODEL", "llama-3.2-11b-vision-preview")
            
            response = self.client.chat.completions.create(
                model=vision_model,
                max_tokens=self.max_tokens,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPTS["image_analyst"]},
                    {
                        "role": "user",
                        "content": [
                            {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{image_data}"}},
                            {"type": "text", "text": user_message}
                        ]
                    }
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            # Fallback: Describe without image
            return f"⚠️ {self.provider_name} has limited vision support.\n\n{self.quick_ask(user_message)}"

    def chat_with_image_bytes(self, user_message: str, image_bytes: bytes, media_type: str = "image/png") -> str:
        """Send a message with image bytes (from file upload)."""
        image_data = base64.standard_b64encode(image_bytes).decode("utf-8")
        return self.chat_with_image(user_message, image_data)  # Will encode properly

    def quick_ask(self, prompt: str, system: str = "") -> str:
        """
        One-shot question without conversation history.
        Useful for analysis tasks.
        """
        if self.is_groq:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[
                    {"role": "system", "content": system or self.system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        else:
            import anthropic
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
            "provider": self.provider_name,
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


# ── Convenience Factory Functions ────────────────────────────────────────────

def create_ai_engine(mode: str = "chat", api_key: Optional[str] = None) -> NeuroMindAI:
    """
    Factory function to create an AI engine with auto-provider detection.
    
    Args:
        mode: AI mode (chat, document_qa, etc.)
        api_key: Optional API key (auto-detects if not provided)
    
    Returns:
        Configured NeuroMindAI instance
    """
    return NeuroMindAI(mode=mode, api_key=api_key)


def create_groq_engine(mode: str = "chat") -> NeuroMindAI:
    """Create an AI engine specifically using Groq."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ GROQ_API_KEY not found in environment!")
    return NeuroMindAI(mode=mode, api_key=api_key)


def create_anthropic_engine(mode: str = "chat") -> NeuroMindAI:
    """Create an AI engine specifically using Anthropic."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("❌ ANTHROPIC_API_KEY not found in environment!")
    return NeuroMindAI(mode=mode, api_key=api_key)
