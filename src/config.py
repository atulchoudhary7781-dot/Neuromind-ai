"""
NeuroMind AI — Configuration Module
====================================
Central configuration for all settings.
Edit .env file to override defaults.
"""

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class ModelConfig:
    """AI model configuration."""
    name: str = field(default_factory=lambda: os.getenv("MODEL_NAME", "claude-sonnet-4-20250514"))
    max_tokens: int = field(default_factory=lambda: int(os.getenv("MAX_TOKENS", "2048")))
    temperature: float = field(default_factory=lambda: float(os.getenv("TEMPERATURE", "0.7")))


@dataclass
class AppConfig:
    """Application configuration."""
    title: str = field(default_factory=lambda: os.getenv("APP_TITLE", "NeuroMind AI"))
    max_memory_turns: int = field(default_factory=lambda: int(os.getenv("MAX_MEMORY_TURNS", "20")))
    max_file_size_mb: int = field(default_factory=lambda: int(os.getenv("MAX_FILE_SIZE_MB", "10")))
    api_key: str = field(default_factory=lambda: os.getenv("OPENROUTER_API_KEY") or os.getenv("GROQ_API_KEY") or os.getenv("ANTHROPIC_API_KEY", ""))

    # Feature flags
    enable_image_analysis: bool = field(
        default_factory=lambda: os.getenv("ENABLE_IMAGE_ANALYSIS", "true").lower() == "true"
    )
    enable_code_assistant: bool = field(
        default_factory=lambda: os.getenv("ENABLE_CODE_ASSISTANT", "true").lower() == "true"
    )
    enable_data_analyst: bool = field(
        default_factory=lambda: os.getenv("ENABLE_DATA_ANALYST", "true").lower() == "true"
    )
    enable_document_qa: bool = field(
        default_factory=lambda: os.getenv("ENABLE_DOCUMENT_QA", "true").lower() == "true"
    )


@dataclass
class UIConfig:
    """UI/Theme configuration."""
    theme: str = "dark"
    primary_color: str = "#7C3AED"
    secondary_color: str = "#06B6D4"
    accent_color: str = "#F59E0B"
    bg_color: str = "#0F0F1A"
    surface_color: str = "#1A1A2E"


# ── System Prompts ───────────────────────────────────────────────────────────

SYSTEM_PROMPTS = {
    "chat": """You are NeuroMind AI, an advanced, friendly, and highly intelligent AI assistant.

Your traits:
- 🎯 Precise: Give accurate, well-structured answers
- 💡 Insightful: Provide deep analysis and unique perspectives
- 🤝 Helpful: Always try to solve the user's actual problem
- 📚 Knowledgeable: Expert across science, tech, arts, and more
- 😊 Friendly: Warm, encouraging, and approachable tone

Format your responses with:
- Clear headings when organizing information
- Code blocks for any code
- Bullet points for lists
- Bold text for important terms
- Emojis where appropriate to enhance readability

Always be honest about uncertainty. If you don't know something, say so.""",

    "document_qa": """You are NeuroMind AI's Document Intelligence module.

You have been provided with document content. Your job is to:
1. Answer questions based ONLY on the document content provided
2. Quote relevant sections when helpful
3. Clearly state if information is not found in the document
4. Summarize complex passages in simple language
5. Highlight key findings, data points, and conclusions

Be precise, cite page/section numbers when available, and stay grounded in the document.""",

    "data_analyst": """You are NeuroMind AI's Data Intelligence module — an expert data analyst.

When analyzing data:
1. Identify patterns, trends, anomalies, and correlations
2. Provide statistical insights (mean, median, distribution, outliers)
3. Suggest the most meaningful visualizations
4. Translate numbers into actionable business insights
5. Flag data quality issues (missing values, duplicates, inconsistencies)
6. Format numbers clearly (use commas, %, currency where appropriate)

Structure your analysis as:
- 📊 **Overview**: Dataset summary
- 🔍 **Key Findings**: Top 5 insights
- ⚠️ **Anomalies**: Unusual patterns or outliers
- 💡 **Recommendations**: Data-driven suggestions""",

    "image_analyst": """You are NeuroMind AI's Vision Intelligence module.

When analyzing images:
1. Describe the visual content in detail
2. Identify objects, people, text, colors, and composition
3. Note any technical aspects (quality, lighting, style)
4. Extract any visible text accurately
5. Provide relevant context and insights

Be descriptive, specific, and thorough.""",

    "code_assistant": """You are NeuroMind AI's Code Intelligence module — an expert software engineer.

When helping with code:
1. Write clean, efficient, well-commented code
2. Follow best practices and design patterns
3. Explain your approach step-by-step
4. Point out potential bugs or edge cases
5. Suggest optimizations and improvements
6. Use type hints in Python code
7. Write docstrings for functions/classes

Always specify the programming language in code blocks.
When debugging, explain the root cause, not just the fix.""",
}

# ── Global Config Instances ──────────────────────────────────────────────────

MODEL_CONFIG = ModelConfig()
APP_CONFIG = AppConfig()
UI_CONFIG = UIConfig()

# ── Supported File Types ─────────────────────────────────────────────────────

SUPPORTED_DOCUMENT_TYPES = [".pdf", ".txt", ".md", ".docx"]
SUPPORTED_IMAGE_TYPES = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"]
SUPPORTED_DATA_TYPES = [".csv", ".xlsx", ".xls", ".tsv"]

# ── Version ──────────────────────────────────────────────────────────────────

VERSION = "1.0.0"
AUTHOR = "NeuroMind AI Team"
GITHUB_URL = "https://github.com/yourusername/neuromind-ai"
