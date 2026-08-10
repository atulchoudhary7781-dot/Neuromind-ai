"""
NeuroMind AI — Utility Functions
==================================
Helper functions used across NeuroMind AI modules.

Author: NeuroMind AI Team
"""

import hashlib
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any


def format_file_size(size_bytes: int) -> str:
    """Convert bytes to human-readable size."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 ** 3:
        return f"{size_bytes / 1024 ** 2:.1f} MB"
    return f"{size_bytes / 1024 ** 3:.1f} GB"


def get_file_extension(filename: str) -> str:
    """Get lowercase file extension."""
    return Path(filename).suffix.lower()


def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """Truncate text with ellipsis if too long."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def clean_markdown(text: str) -> str:
    """Remove Markdown formatting from text."""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # bold
    text = re.sub(r"\*(.*?)\*", r"\1", text)        # italic
    text = re.sub(r"`(.*?)`", r"\1", text)          # code
    text = re.sub(r"#{1,6}\s", "", text)            # headers
    return text.strip()


def count_tokens_approx(text: str) -> int:
    """
    Approximate token count (rough estimate: ~4 chars per token).

    Args:
        text: Input text

    Returns:
        Estimated token count
    """
    return len(text) // 4


def detect_language(code: str) -> str:
    """
    Detect programming language from code snippet.

    Args:
        code: Code string to analyze

    Returns:
        Detected language name
    """
    patterns = {
        "python": [r"def\s+\w+\(", r"import\s+\w+", r"print\(", r"if __name__"],
        "javascript": [r"const\s+\w+", r"function\s+\w+", r"console\.log", r"=>"],
        "typescript": [r"interface\s+\w+", r":\s*string", r":\s*number", r"export\s+type"],
        "java": [r"public\s+class", r"System\.out\.println", r"void\s+main"],
        "c++": [r"#include\s*<", r"std::", r"cout\s*<<", r"int\s+main"],
        "rust": [r"fn\s+main", r"let\s+mut", r"println!", r"use\s+std::"],
        "go": [r"func\s+main", r"package\s+main", r"fmt\.Println"],
        "sql": [r"SELECT\s+", r"FROM\s+", r"WHERE\s+", r"INSERT\s+INTO"],
        "html": [r"<html", r"<div", r"<!DOCTYPE"],
        "css": [r"\{[\s\n]*[\w-]+\s*:", r"@media", r"\.[\w-]+\s*\{"],
        "bash": [r"#!/bin/bash", r"\$\{", r"echo\s+", r"if\s+\["],
    }

    code_lower = code[:500]

    for lang, pats in patterns.items():
        if any(re.search(pat, code_lower, re.IGNORECASE) for pat in pats):
            return lang

    return "text"


def generate_session_id() -> str:
    """Generate a unique session ID."""
    timestamp = str(time.time()).encode()
    return hashlib.md5(timestamp).hexdigest()[:8].upper()


def format_number(n: float, decimals: int = 2) -> str:
    """Format a number with commas and optional decimals."""
    if isinstance(n, int) or n == int(n):
        return f"{int(n):,}"
    return f"{n:,.{decimals}f}"


def get_greeting() -> str:
    """Return time-appropriate greeting."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 21:
        return "Good evening"
    return "Hello"


def validate_api_key(api_key: str) -> tuple[bool, str]:
    """
    Basic validation of Anthropic API key format.

    Args:
        api_key: API key string to validate

    Returns:
        Tuple of (is_valid, message)
    """
    if not api_key:
        return False, "API key is empty"
    if not api_key.startswith("sk-ant-"):
        return False, "API key should start with 'sk-ant-'"
    if len(api_key) < 40:
        return False, "API key seems too short"
    return True, "API key format looks valid"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safe division that returns default on ZeroDivisionError."""
    try:
        return numerator / denominator
    except (ZeroDivisionError, TypeError):
        return default


class Timer:
    """Simple context manager for timing code blocks."""

    def __init__(self, name: str = ""):
        self.name = name
        self.elapsed: float = 0

    def __enter__(self):
        self._start = time.time()
        return self

    def __exit__(self, *args):
        self.elapsed = time.time() - self._start

    def __str__(self):
        label = f"{self.name}: " if self.name else ""
        return f"{label}{self.elapsed:.3f}s"
