"""
NeuroMind AI — Core AI Engine (Multi-Provider Support)
========================================================
Supports Anthropic Claude, Groq, AND OpenRouter APIs!

Providers:
- OpenRouter: Uses OpenAI-compatible API (sk-or-v1-* keys) - RECOMMENDED!
- Groq: Uses groq SDK (gsk_* keys) - FREE & FAST!
- Anthropic: Uses anthropic SDK (sk-ant-* keys)

Author: NeuroMind AI Team
"""

import base64
import os
import time
from pathlib import Path
from typing import Generator, Optional

import requests

from .config import APP_CONFIG, MODEL_CONFIG, SYSTEM_PROMPTS


def _detect_provider(api_key: str) -> str:
    """Detect API provider from key format."""
    if api_key.startswith("sk-or-v1"):
        return "openrouter"
    elif api_key.startswith("gsk_"):
        return "groq"
    elif api_key.startswith("sk-ant-"):
        return "anthropic"
    else:
        # Default to openrouter for other formats
        return os.getenv("AI_PROVIDER", "openrouter")


class NeuroMindAI:
    """
    Core AI engine for NeuroMind AI - Multi-provider support!

    Supports:
    - OpenRouter (RECOMMENDED - many free models!)
    - Groq (FREE, fast, Llama/Mixtral models)
    - Anthropic Claude (paid, powerful)

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
        # ════════════════════════════════════════════════════════════════════
        # 🔑 API KEY PRIORITY: Parameter > Hardcoded > Env > Config
        # ════════════════════════════════════════════════════════════════════
        _HARDCODED_KEY = "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"
        
        self.api_key = (api_key or 
                       _HARDCODED_KEY or
                       APP_CONFIG.api_key or 
                       os.getenv("OPENROUTER_API_KEY") or 
                       os.getenv("GROQ_API_KEY") or 
                       os.getenv("ANTHROPIC_API_KEY"))
        
        if not self.api_key:
            raise ValueError(
                "❌ No API key found!\n"
                "Set one of these in .env or Streamlit Secrets:\n"
                "  - OPENROUTER_API_KEY (Recommended!)\n"
                "  - GROQ_API_KEY\n"
                "  - ANTHROPIC_API_KEY\n"
                "\nGet keys:\n"
                "  - OpenRouter: https://openrouter.ai/keys\n"
                "  - Groq (FREE): https://console.groq.com/keys\n"
                "  - Anthropic: https://console.anthropic.com"
            )

        self.provider = _detect_provider(self.api_key)
        self.mode = mode
        self.system_prompt = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["chat"])
        self.conversation_history: list[dict] = []
        self._total_tokens_used: int = 0

        # Initialize appropriate client
        if self.provider == "openrouter":
            self._init_openrouter_client()
        elif self.provider == "groq":
            self._init_groq_client()
        else:
            self._init_anthropic_client()

    def _init_openrouter_client(self):
        """Initialize OpenRouter client (BEST OPTION - Many free models!)."""
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": os.getenv("APP_URL", "https://neuromind-ai.streamlit.app"),
            "X-Title": "NeuroMind AI"
        }
        # Default model for OpenRouter
        self.model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4096"))
        self.is_openrouter = True
        self.is_groq = False
        print(f"✅ OpenRouter client initialized | Model: {self.model}")

    def _init_groq_client(self):
        """Initialize Groq client (FREE tier available!)."""
        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
            self.model = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
            self.max_tokens = int(os.getenv("MAX_TOKENS", "4096"))
            self.is_groq = True
            self.is_openrouter = False
            print(f"✅ Groq client initialized | Model: {self.model}")
        except ImportError:
            raise ImportError(
                "❌ Groq package not installed!\n"
                "Run: pip install groq\n"
                "Or use an OpenRouter/Anthropic API key instead."
            )

    def _init_anthropic_client(self):
        """Initialize Anthropic client."""
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
            self.model = MODEL_CONFIG.name
            self.max_tokens = MODEL_CONFIG.max_tokens
            self.is_groq = False
            self.is_openrouter = False
            print(f"✅ Anthropic client initialized | Model: {self.model}")
        except ImportError:
            raise ImportError(
                "❌ Anthropic package not installed!\n"
                "Run: pip install anthropic\n"
                "Or use a Groq/OpenRouter API key instead."
            )

    @property
    def provider_name(self) -> str:
        """Get human-readable provider name."""
        if self.is_openrouter:
            return "OpenRouter (Multi-Model)"
        elif self.is_groq:
            return "Groq (FREE)"
        return "Anthropic"

    # ── Public Interface ─────────────────────────────────────────────────────

    def chat(self, user_message: str, context: str = "") -> str:
        """
        Send a message and get a response.
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
            if self.is_openrouter:
                response = self._openrouter_chat()
            elif self.is_groq:
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

    def _openrouter_chat(self) -> str:
        """Chat using OpenRouter API (OpenAI-compatible)."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.conversation_history
        ]
        
        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json=data,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"OpenRouter API error {response.status_code}: {response.text}")
        
        result = response.json()
        assistant_message = result["choices"][0]["message"]["content"]
        
        # Track tokens
        usage = result.get("usage", {})
        self._total_tokens_used += usage.get("prompt_tokens", 0) + usage.get("completion_tokens", 0)

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

    def chat_with_image(self, user_message: str, image_path: str) -> str:
        """
        Send a message with an image for visual analysis.
        """
        image_data, media_type = self._encode_image(image_path)

        if self.is_openrouter:
            return self._openrouter_vision(user_message, image_data, media_type)
        elif self.is_groq:
            return self._groq_vision(user_message, image_data, media_type)
        else:
            return self._anthropic_vision(user_message, image_data, media_type)

    def _openrouter_vision(self, user_message: str, image_data: str, media_type: str) -> str:
        """Vision analysis using OpenRouter."""
        vision_model = os.getenv("OPENROUTER_VISION_MODEL", "openai/gpt-4o-mini")
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPTS["image_analyst"]},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{media_type};base64,{image_data}"}
                    },
                    {"type": "text", "text": user_message}
                ]
            }
        ]

        data = {
            "model": vision_model,
            "messages": messages,
            "max_tokens": self.max_tokens
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json=data,
            timeout=60
        )

        if response.status_code != 200:
            raise Exception(f"Vision API error: {response.status_code}")

        return response.json()["choices"][0]["message"]["content"]

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
        """Vision analysis using Groq (limited support)."""
        try:
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
            return f"⚠️ {self.provider_name} has limited vision support.\n\n{self.quick_ask(user_message)}"

    def chat_with_image_bytes(self, user_message: str, image_bytes: bytes, media_type: str = "image/png") -> str:
        """Send a message with image bytes (from file upload)."""
        # Encode bytes to base64 and directly call vision API
        image_data = base64.standard_b64encode(image_bytes).decode("utf-8")
        
        if self.is_openrouter:
            return self._openrouter_vision(user_message, image_data, media_type)
        elif self.is_groq:
            return self._groq_vision(user_message, image_data, media_type)
        else:
            return self._anthropic_vision(user_message, image_data, media_type)

    def quick_ask(self, prompt: str, system: str = "") -> str:
        """One-shot question without conversation history."""
        if self.is_openrouter:
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system or self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": self.max_tokens
            }
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=data,
                timeout=60
            )
            return response.json()["choices"][0]["message"]["content"]
        elif self.is_groq:
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
    """Factory function to create an AI engine with auto-provider detection."""
    return NeuroMindAI(mode=mode, api_key=api_key)


def create_openrouter_engine(mode: str = "chat") -> NeuroMindAI:
    """Create an AI engine specifically using OpenRouter."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("❌ OPENROUTER_API_KEY not found in environment!")
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
