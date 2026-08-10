"""
NeuroMind AI — Source Package
==============================
Core modules for the NeuroMind AI platform.

Modules:
    - ai_core: Core AI engine (NeuroMindAI class)
    - document_qa: Document Q&A module (DocumentQA class)
    - data_analyzer: Data analysis module (DataAnalyzer class)
    - memory: Conversation memory (ConversationMemory class)
    - utils: Utility functions and helpers
    - config: Configuration and settings

Example:
    >>> from src import NeuroMindAI, DataAnalyzer, ConversationMemory
    >>> ai = NeuroMindAI()
    >>> response = ai.chat("Hello!")
"""

# Import configuration first (no external dependencies)
from .config import (
    APP_CONFIG,
    MODEL_CONFIG,
    UI_CONFIG,
    SYSTEM_PROMPTS,
    VERSION,
    SUPPORTED_DOCUMENT_TYPES,
    SUPPORTED_IMAGE_TYPES,
    SUPPORTED_DATA_TYPES,
)

# Import commonly used utilities (no external dependencies)
from .utils import (
    format_file_size,
    truncate_text,
    count_tokens_approx,
    validate_api_key,
    generate_session_id,
)

# Import memory module (no external dependencies)
from .memory import ConversationMemory, Message

# Import core classes with graceful handling for missing dependencies
try:
    from .ai_core import NeuroMindAI
except ImportError as e:
    # Handle missing optional dependencies (e.g., anthropic)
    NeuroMindAI = None
    _ai_import_error = str(e)

try:
    from .document_qa import DocumentQA
except ImportError:
    DocumentQA = None

try:
    from .data_analyzer import DataAnalyzer
except ImportError:
    DataAnalyzer = None

__version__ = VERSION
__author__ = "NeuroMind AI Team"

__all__ = [
    # Core classes (may be None if dependencies missing)
    "NeuroMindAI",
    "DocumentQA",
    "DataAnalyzer",
    "ConversationMemory",
    "Message",
    # Configuration
    "APP_CONFIG",
    "MODEL_CONFIG",
    "UI_CONFIG",
    "SYSTEM_PROMPTS",
    "VERSION",
    "SUPPORTED_DOCUMENT_TYPES",
    "SUPPORTED_IMAGE_TYPES",
    "SUPPORTED_DATA_TYPES",
    # Utilities
    "format_file_size",
    "truncate_text",
    "count_tokens_approx",
    "validate_api_key",
    "generate_session_id",
]
