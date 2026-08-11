"""
NeuroMind AI — Document Q&A Module
=====================================
Process PDF, TXT, MD, DOCX files and answer questions about them.

Author: NeuroMind AI Team
"""

import re
from pathlib import Path
from typing import Optional


class DocumentQA:
    """
    Document intelligence engine for NeuroMind AI.

    Supports PDF, TXT, Markdown, and DOCX files.
    Extracts text and enables AI-powered Q&A.

    Example:
        >>> qa = DocumentQA(ai_engine)
        >>> content, pages = qa.load_document("research.pdf")
        >>> answer = qa.ask("What are the main findings?")
    """

    def __init__(self, ai_engine):
        """
        Initialize with a NeuroMindAI engine instance.

        Args:
            ai_engine: Instance of NeuroMindAI
        """
        self.ai = ai_engine
        self.document_text: str = ""
        self.document_name: str = ""
        self.page_count: int = 0
        self.word_count: int = 0
        self.char_count: int = 0

    def load_document(self, file_path: str = "", file_bytes: bytes = b"",
                      file_name: str = "") -> tuple[str, int]:
        """
        Load and extract text from a document.

        Args:
            file_path: Path to document file (optional)
            file_bytes: Raw file bytes from upload (optional)
            file_name: Original filename (for type detection)

        Returns:
            Tuple of (extracted_text, page_count)
        """
        # Determine source and extension
        if file_path:
            path = Path(file_path)
            ext = path.suffix.lower()
            self.document_name = path.name
            with open(file_path, "rb") as f:
                file_bytes = f.read()
        else:
            ext = Path(file_name).suffix.lower()
            self.document_name = file_name

        # Route to appropriate extractor
        if ext == ".pdf":
            text, pages = self._extract_pdf(file_bytes)
        elif ext in (".txt", ".md"):
            text = file_bytes.decode("utf-8", errors="ignore")
            pages = text.count("\n\n") + 1
        elif ext == ".docx":
            text, pages = self._extract_docx(file_bytes)
        else:
            raise ValueError(f"Unsupported file type: {ext}\nSupported: PDF, TXT, MD, DOCX")

        self.document_text = text
        self.page_count = pages
        self.word_count = len(text.split())
        self.char_count = len(text)

        return text, pages

    def ask(self, question: str) -> str:
        """
        Ask a question about the loaded document.

        Args:
            question: User's question about the document

        Returns:
            AI-generated answer grounded in the document
        """
        if not self.document_text:
            return "❌ No document loaded. Please upload a document first."

        # Create a context-rich prompt
        context = self._build_context()
        prompt = f"""Based on the following document content, please answer this question:

**Question:** {question}

**Document Content:**
{self._truncate_text(self.document_text, max_chars=15000)}

Please provide a detailed, accurate answer based only on the document content.
If the answer is not found in the document, clearly state that."""

        return self.ai.quick_ask(prompt, system=self._get_system_prompt())

    def summarize(self) -> str:
        """
        Generate a comprehensive document summary.

        Returns:
            AI-generated summary with key points
        """
        if not self.document_text:
            return "❌ No document loaded."

        prompt = f"""Please provide a comprehensive summary of this document:

**Document:** {self.document_name}
**Content:**
{self._truncate_text(self.document_text, max_chars=15000)}

Structure your summary as:
1. 📋 **Overview** (2-3 sentences)
2. 🔑 **Key Points** (bullet list of 5-8 main points)
3. 💡 **Key Takeaways** (most important insights)
4. 📊 **Data/Statistics** (if any numbers are mentioned)
5. 🎯 **Conclusion** (final assessment)"""

        return self.ai.quick_ask(prompt, system=self._get_system_prompt())

    def extract_key_info(self) -> str:
        """
        Extract structured information from the document.

        Returns:
            Structured key information
        """
        if not self.document_text:
            return "❌ No document loaded."

        prompt = f"""Extract the most important structured information from this document:

{self._truncate_text(self.document_text, max_chars=12000)}

Identify and list:
- 📌 **Main Topics/Themes**
- 👤 **People/Organizations Mentioned**
- 📅 **Dates/Timeline**
- 📊 **Numbers/Statistics**
- ✅ **Action Items/Recommendations**
- ❓ **Open Questions**"""

        return self.ai.quick_ask(prompt, system=self._get_system_prompt())

    def get_document_stats(self) -> dict:
        """Return statistics about the loaded document."""
        return {
            "name": self.document_name,
            "pages": self.page_count,
            "words": self.word_count,
            "characters": self.char_count,
            "estimated_read_time": f"{max(1, self.word_count // 200)} minutes",
        }

    def clear(self) -> None:
        """Clear the loaded document."""
        self.document_text = ""
        self.document_name = ""
        self.page_count = 0
        self.word_count = 0
        self.char_count = 0

    # ── Private Helpers ──────────────────────────────────────────────────────

    def _extract_pdf(self, file_bytes: bytes) -> tuple[str, int]:
        """Extract text from PDF using PyMuPDF."""
        try:
            import fitz  # PyMuPDF

            doc = fitz.open(stream=file_bytes, filetype="pdf")
            texts = []
            page_count = len(doc)  # Save BEFORE closing!
            
            for page_num, page in enumerate(doc, 1):
                page_text = page.get_text()
                if page_text.strip():
                    texts.append(f"[Page {page_num}]\n{page_text}")

            doc.close()
            return "\n\n".join(texts), page_count  # Use saved value

        except ImportError:
            raise ImportError(
                "PyMuPDF is required for PDF processing.\n"
                "Install: pip install PyMuPDF"
            )
        except Exception as e:
            raise RuntimeError(f"PDF extraction failed: {str(e)}")

    def _extract_docx(self, file_bytes: bytes) -> tuple[str, int]:
        """Extract text from DOCX files."""
        try:
            import io
            from docx import Document

            doc = Document(io.BytesIO(file_bytes))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            text = "\n\n".join(paragraphs)
            return text, max(1, len(paragraphs) // 30)  # Estimate pages

        except ImportError:
            raise ImportError(
                "python-docx is required for DOCX processing.\n"
                "Install: pip install python-docx"
            )

    def _truncate_text(self, text: str, max_chars: int = 15000) -> str:
        """Truncate text to fit within context limits."""
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + f"\n\n[... Document truncated. {len(text) - max_chars} characters not shown ...]"

    def _build_context(self) -> str:
        """Build context string with document metadata."""
        return (
            f"Document: {self.document_name} | "
            f"Pages: {self.page_count} | "
            f"Words: {self.word_count:,}"
        )

    def _get_system_prompt(self) -> str:
        from .config import SYSTEM_PROMPTS
        return SYSTEM_PROMPTS["document_qa"]

    def __repr__(self) -> str:
        if self.document_name:
            return f"DocumentQA(doc='{self.document_name}', words={self.word_count:,})"
        return "DocumentQA(no document loaded)"
