"""
NeuroMind AI — Conversation Memory Module
==========================================
Manages conversation history with export capabilities.

Author: NeuroMind AI Team
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Message:
    """A single conversation message."""
    role: str           # 'user' or 'assistant'
    content: str        # Message text
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    module: str = "chat"   # Which NeuroMind module was used

    def to_dict(self) -> dict:
        return asdict(self)


class ConversationMemory:
    """
    Manages conversation history for NeuroMind AI sessions.

    Supports:
    - In-memory conversation tracking
    - Export to Markdown / JSON
    - Message filtering and search
    - Session statistics

    Example:
        >>> memory = ConversationMemory()
        >>> memory.add("user", "Hello!")
        >>> memory.add("assistant", "Hi there!")
        >>> print(memory.to_markdown())
    """

    def __init__(self, session_name: str = ""):
        self.session_name = session_name or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.messages: list[Message] = []
        self.created_at = datetime.now().isoformat()

    def add(self, role: str, content: str, module: str = "chat") -> None:
        """Add a message to the conversation history."""
        self.messages.append(Message(role=role, content=content, module=module))

    def get_all(self) -> list[dict]:
        """Get all messages as a list of dicts (for Claude API format)."""
        return [{"role": m.role, "content": m.content} for m in self.messages]

    def get_last_n(self, n: int) -> list[dict]:
        """Get the last N messages."""
        return [{"role": m.role, "content": m.content} for m in self.messages[-n:]]

    def clear(self) -> None:
        """Clear all messages."""
        self.messages = []

    def search(self, query: str) -> list[Message]:
        """Search messages containing a keyword."""
        query = query.lower()
        return [m for m in self.messages if query in m.content.lower()]

    def count(self) -> dict:
        """Return message count by role."""
        return {
            "total": len(self.messages),
            "user": sum(1 for m in self.messages if m.role == "user"),
            "assistant": sum(1 for m in self.messages if m.role == "assistant"),
        }

    def to_markdown(self) -> str:
        """Export conversation as a Markdown document."""
        lines = [
            f"# 🧠 NeuroMind AI — Conversation Export",
            f"**Session:** {self.session_name}",
            f"**Date:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            f"**Total Messages:** {len(self.messages)}",
            f"\n---\n",
        ]

        for msg in self.messages:
            timestamp = msg.timestamp[:19].replace("T", " ")
            if msg.role == "user":
                lines.append(f"### 👤 You  \n*{timestamp}*\n")
                lines.append(msg.content)
            else:
                lines.append(f"\n### 🤖 NeuroMind AI  \n*{timestamp}*\n")
                lines.append(msg.content)
            lines.append("\n---\n")

        return "\n".join(lines)

    def to_json(self) -> str:
        """Export conversation as JSON."""
        data = {
            "session_name": self.session_name,
            "created_at": self.created_at,
            "exported_at": datetime.now().isoformat(),
            "message_count": len(self.messages),
            "messages": [m.to_dict() for m in self.messages],
        }
        return json.dumps(data, indent=2, ensure_ascii=False)

    def save_to_file(self, path: str, format: str = "markdown") -> str:
        """Save conversation to a file."""
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format == "json":
            output_path.write_text(self.to_json(), encoding="utf-8")
        else:
            output_path.write_text(self.to_markdown(), encoding="utf-8")

        return str(output_path)

    def get_stats(self) -> dict:
        """Get detailed session statistics."""
        if not self.messages:
            return {"error": "No messages in session"}

        user_msgs = [m for m in self.messages if m.role == "user"]
        ai_msgs = [m for m in self.messages if m.role == "assistant"]

        return {
            "session_name": self.session_name,
            "total_messages": len(self.messages),
            "user_messages": len(user_msgs),
            "ai_messages": len(ai_msgs),
            "avg_user_length": int(sum(len(m.content) for m in user_msgs) / max(len(user_msgs), 1)),
            "avg_ai_length": int(sum(len(m.content) for m in ai_msgs) / max(len(ai_msgs), 1)),
            "session_start": self.created_at[:19].replace("T", " "),
            "modules_used": list(set(m.module for m in self.messages)),
        }

    def __len__(self) -> int:
        return len(self.messages)

    def __repr__(self) -> str:
        return f"ConversationMemory(session='{self.session_name}', messages={len(self.messages)})"
