"""
NeuroMind AI — Test Suite for AI Core Module
=============================================
Tests for the NeuroMindAI class.

Run: pytest tests/ -v
"""

import os
import pytest
from unittest.mock import MagicMock, patch


class TestNeuroMindAI:
    """Test cases for the core AI engine."""

    def test_init_without_api_key_raises(self):
        """Should raise ValueError if no API key is set."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("ANTHROPIC_API_KEY", None)
            with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
                # Re-import to avoid cached env
                import importlib
                import config
                importlib.reload(config)
                from src.ai_core import NeuroMindAI
                NeuroMindAI()

    def test_init_with_api_key(self):
        """Should initialize correctly with API key."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test123"}):
            with patch("anthropic.Anthropic"):
                from src.ai_core import NeuroMindAI
                ai = NeuroMindAI()
                assert ai.mode == "chat"
                assert ai.conversation_history == []

    def test_mode_selection(self):
        """Should set correct system prompt based on mode."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test123"}):
            with patch("anthropic.Anthropic"):
                from src.ai_core import NeuroMindAI
                from config import SYSTEM_PROMPTS

                for mode in ["chat", "document_qa", "data_analyst", "code_assistant"]:
                    ai = NeuroMindAI(mode=mode)
                    assert ai.system_prompt == SYSTEM_PROMPTS[mode], \
                        f"Wrong system prompt for mode: {mode}"

    def test_clear_history(self):
        """Should clear conversation history."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test123"}):
            with patch("anthropic.Anthropic"):
                from src.ai_core import NeuroMindAI
                ai = NeuroMindAI()
                ai.conversation_history = [
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi!"},
                ]
                ai.clear_history()
                assert ai.conversation_history == []

    def test_get_stats(self):
        """Should return correct stats."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test123"}):
            with patch("anthropic.Anthropic"):
                from src.ai_core import NeuroMindAI
                ai = NeuroMindAI(mode="chat")
                stats = ai.get_stats()
                assert "total_messages" in stats
                assert "model" in stats
                assert stats["mode"] == "chat"


class TestConversationMemory:
    """Test cases for conversation memory."""

    def test_add_and_retrieve(self):
        """Should add and retrieve messages correctly."""
        from src.memory import ConversationMemory
        memory = ConversationMemory()
        memory.add("user", "Hello!")
        memory.add("assistant", "Hi there!")

        msgs = memory.get_all()
        assert len(msgs) == 2
        assert msgs[0]["role"] == "user"
        assert msgs[1]["content"] == "Hi there!"

    def test_clear(self):
        """Should clear all messages."""
        from src.memory import ConversationMemory
        memory = ConversationMemory()
        memory.add("user", "test")
        memory.clear()
        assert len(memory) == 0

    def test_count(self):
        """Should count messages by role correctly."""
        from src.memory import ConversationMemory
        memory = ConversationMemory()
        memory.add("user", "Q1")
        memory.add("assistant", "A1")
        memory.add("user", "Q2")

        counts = memory.count()
        assert counts["total"] == 3
        assert counts["user"] == 2
        assert counts["assistant"] == 1

    def test_search(self):
        """Should find messages containing keyword."""
        from src.memory import ConversationMemory
        memory = ConversationMemory()
        memory.add("user", "Tell me about Python")
        memory.add("assistant", "Python is a programming language")
        memory.add("user", "What about Java?")

        results = memory.search("python")
        assert len(results) == 2  # Both contain "Python"

    def test_to_markdown_format(self):
        """Should export to valid markdown."""
        from src.memory import ConversationMemory
        memory = ConversationMemory(session_name="test_session")
        memory.add("user", "Hello")
        memory.add("assistant", "World")

        md = memory.to_markdown()
        assert "NeuroMind AI" in md
        assert "test_session" in md
        assert "Hello" in md
        assert "World" in md

    def test_to_json_format(self):
        """Should export valid JSON."""
        import json
        from src.memory import ConversationMemory
        memory = ConversationMemory()
        memory.add("user", "Test")

        json_str = memory.to_json()
        data = json.loads(json_str)
        assert "messages" in data
        assert data["message_count"] == 1


class TestUtils:
    """Test cases for utility functions."""

    def test_format_file_size(self):
        from src.utils import format_file_size
        assert format_file_size(500) == "500 B"
        assert "KB" in format_file_size(2048)
        assert "MB" in format_file_size(2 * 1024 * 1024)

    def test_truncate_text(self):
        from src.utils import truncate_text
        text = "A" * 300
        result = truncate_text(text, max_length=100)
        assert len(result) <= 100
        assert result.endswith("...")

    def test_truncate_short_text(self):
        from src.utils import truncate_text
        text = "Short text"
        assert truncate_text(text, max_length=100) == text

    def test_count_tokens_approx(self):
        from src.utils import count_tokens_approx
        text = "A" * 400  # 100 tokens approx
        assert count_tokens_approx(text) == 100

    def test_validate_api_key_valid(self):
        from src.utils import validate_api_key
        valid, msg = validate_api_key("sk-ant-api03-abcdefghijklmnopqrstuvwxyz1234567890")
        assert valid is True

    def test_validate_api_key_empty(self):
        from src.utils import validate_api_key
        valid, msg = validate_api_key("")
        assert valid is False

    def test_validate_api_key_wrong_prefix(self):
        from src.utils import validate_api_key
        valid, msg = validate_api_key("wrong-prefix-key-12345678901234567890")
        assert valid is False

    def test_detect_language_python(self):
        from src.utils import detect_language
        code = "def hello_world():\n    print('Hello')\nimport os"
        assert detect_language(code) == "python"

    def test_detect_language_javascript(self):
        from src.utils import detect_language
        code = "const greet = (name) => console.log(`Hello ${name}`);"
        assert detect_language(code) == "javascript"

    def test_format_number(self):
        from src.utils import format_number
        assert format_number(1000000) == "1,000,000"
        assert format_number(3.14159, decimals=2) == "3.14"

    def test_safe_divide(self):
        from src.utils import safe_divide
        assert safe_divide(10, 2) == 5.0
        assert safe_divide(10, 0) == 0.0
        assert safe_divide(10, 0, default=-1) == -1
