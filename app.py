"""
NeuroMind AI — Main Streamlit Application
==========================================
Beautiful multi-modal AI assistant with dark theme.

Run: streamlit run app.py
"""

# ════════════════════════════════════════════════════════════════════════════════
# CRITICAL: Path Setup (MUST be first - before any other imports)
# This ensures 'from src.xxx import yyy' works regardless of execution location
# ════════════════════════════════════════════════════════════════════════════════
import os, sys
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

import io
import json
from datetime import datetime
from pathlib import Path

import streamlit as st
from PIL import Image

# ── Page Config (must be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="NeuroMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/yourusername/neuromind-ai",
        "Report a bug": "https://github.com/yourusername/neuromind-ai/issues",
        "About": "# NeuroMind AI\nYour multi-modal AI assistant platform.",
    }
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* === GLOBAL STYLES === */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-dark: #0F0F1A;
    --surface: #1A1A2E;
    --surface-2: #16213E;
    --primary: #7C3AED;
    --primary-light: #A855F7;
    --secondary: #06B6D4;
    --accent: #F59E0B;
    --success: #10B981;
    --error: #EF4444;
    --text: #E2E8F0;
    --text-muted: #94A3B8;
    --border: #2D3748;
}

.stApp {
    background: linear-gradient(135deg, #0F0F1A 0%, #1A1A2E 50%, #16213E 100%);
    font-family: 'Inter', sans-serif;
}

/* === SIDEBAR === */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D0D1F 0%, #1A0A2E 100%) !important;
    border-right: 1px solid #2D3748;
}

[data-testid="stSidebar"] .stButton button {
    width: 100%;
    background: transparent;
    border: 1px solid #2D3748;
    color: #E2E8F0;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    transition: all 0.2s ease;
    text-align: left;
    margin-bottom: 4px;
}

[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(124, 58, 237, 0.2);
    border-color: #7C3AED;
    color: #A855F7;
    transform: translateX(4px);
}

/* === CHAT MESSAGES === */
.user-message {
    background: linear-gradient(135deg, #1E1B4B, #2D1B69);
    border: 1px solid #4C1D95;
    border-radius: 16px 16px 4px 16px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    margin-left: 10%;
    color: #E2E8F0;
    font-size: 0.95rem;
    line-height: 1.6;
    box-shadow: 0 4px 20px rgba(124, 58, 237, 0.15);
}

.ai-message {
    background: linear-gradient(135deg, #0F2027, #203A43);
    border: 1px solid #164E63;
    border-radius: 16px 16px 16px 4px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    margin-right: 10%;
    color: #E2E8F0;
    font-size: 0.95rem;
    line-height: 1.6;
    box-shadow: 0 4px 20px rgba(6, 182, 212, 0.1);
}

.message-meta {
    font-size: 0.72rem;
    color: #64748B;
    margin-bottom: 0.3rem;
    font-family: 'JetBrains Mono', monospace;
}

/* === HEADER === */
.neuromind-header {
    background: linear-gradient(135deg, #0D0D1F, #1A0A2E);
    border: 1px solid #2D3748;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.neuromind-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at center, rgba(124, 58, 237, 0.08) 0%, transparent 70%);
    pointer-events: none;
}

.neuromind-title {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #A855F7, #06B6D4, #F59E0B);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    letter-spacing: -0.5px;
}

.neuromind-subtitle {
    color: #64748B;
    font-size: 0.9rem;
    margin-top: 0.3rem;
    font-family: 'JetBrains Mono', monospace;
}

/* === FEATURE CARDS === */
.feature-card {
    background: linear-gradient(135deg, #1A1A2E, #16213E);
    border: 1px solid #2D3748;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
}

.feature-card:hover {
    border-color: #7C3AED;
    box-shadow: 0 0 20px rgba(124, 58, 237, 0.2);
    transform: translateY(-2px);
}

/* === STAT BOXES === */
.stat-box {
    background: linear-gradient(135deg, #1A1A2E, #1E1B4B);
    border: 1px solid #2D3748;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}

.stat-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #A855F7;
    font-family: 'JetBrains Mono', monospace;
}

.stat-label {
    font-size: 0.75rem;
    color: #64748B;
    margin-top: 0.2rem;
}

/* === STREAMLIT OVERRIDES === */
.stTextInput input, .stTextArea textarea {
    background: #1A1A2E !important;
    border: 1px solid #2D3748 !important;
    color: #E2E8F0 !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #7C3AED, #5B21B6) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #A855F7, #7C3AED) !important;
    box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4) !important;
    transform: translateY(-1px) !important;
}

.stSelectbox select, [data-testid="stSelectbox"] div {
    background: #1A1A2E !important;
    color: #E2E8F0 !important;
    border-color: #2D3748 !important;
}

.stFileUploader {
    border: 2px dashed #2D3748 !important;
    border-radius: 12px !important;
    background: #1A1A2E !important;
}

.stFileUploader:hover {
    border-color: #7C3AED !important;
}

/* === TABS === */
.stTabs [data-baseweb="tab-list"] {
    background: #1A1A2E;
    border-radius: 10px;
    padding: 4px;
}

.stTabs [data-baseweb="tab"] {
    color: #64748B !important;
    font-family: 'Inter', sans-serif;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7C3AED, #5B21B6) !important;
    color: white !important;
    border-radius: 8px !important;
}

/* === SCROLLBAR === */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0F0F1A; }
::-webkit-scrollbar-thumb { background: #2D3748; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #7C3AED; }

/* === MISC === */
hr { border-color: #1E293B !important; }
.stMarkdown code {
    background: #1E1B4B !important;
    color: #A855F7 !important;
    padding: 2px 6px;
    border-radius: 4px;
}

.upload-tip {
    background: rgba(6, 182, 212, 0.08);
    border: 1px solid rgba(6, 182, 212, 0.2);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    color: #94A3B8;
    font-size: 0.85rem;
    margin-bottom: 1rem;
}

.success-badge {
    display: inline-block;
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #10B981;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.8rem;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# ── DEFAULT API KEY (Pre-configured - Users don't need to enter!) ────────
# Priority: OpenRouter > Groq > Anthropic
_DEFAULT_KEY = os.getenv("OPENROUTER_API_KEY") or os.getenv("GROQ_API_KEY") or os.getenv("ANTHROPIC_API_KEY", "")

def get_api_key():
    """Get API key - always returns a key (default or user-set)."""
    if st.session_state.get("api_key"):
        return st.session_state.api_key
    return _DEFAULT_KEY

# ── Initialize Session State ─────────────────────────────────────────────────
def init_session_state():
    # Auto-get API key (no user input needed!)
    _auto_key = get_api_key()
    
    defaults = {
        "messages": [],
        "api_key": _auto_key,  # Auto-set!
        "current_module": "🤖 AI Chat",
        "document_content": "",
        "document_name": "",
        "data_df": None,
        "data_file_name": "",
        "total_tokens": 0,
        "session_start": datetime.now().strftime("%H:%M"),
        "ai_engine": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val
    
    # Ensure API key is always set
    if not st.session_state.api_key and _auto_key:
        st.session_state.api_key = _auto_key


init_session_state()


# ── Helper Functions ─────────────────────────────────────────────────────────
def get_ai_engine(mode: str = "chat"):
    """Initialize or return cached AI engine."""
    if not st.session_state.api_key:
        return None
    try:
        from src.ai_core import NeuroMindAI
        engine = NeuroMindAI(mode=mode, api_key=st.session_state.api_key)
        # Store provider info in session
        st.session_state.ai_provider = engine.provider_name
        st.session_state.ai_model = engine.model
        return engine
    except Exception as e:
        st.error(f"Failed to initialize AI: {e}")
        return None


def display_message(role: str, content: str, timestamp: str = ""):
    """Render a chat message with custom styling."""
    time_str = timestamp or datetime.now().strftime("%H:%M")
    if role == "user":
        st.markdown(f"""
        <div class="user-message">
            <div class="message-meta">👤 You · {time_str}</div>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="ai-message">
            <div class="message-meta">🧠 NeuroMind AI · {time_str}</div>
            {content}
        </div>
        """, unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 0.5rem;">
        <div style="font-size: 2.5rem;">🧠</div>
        <div style="font-size: 1.1rem; font-weight: 700; color: #A855F7; letter-spacing: 1px;">NeuroMind AI</div>
        <div style="font-size: 0.7rem; color: #475569; font-family: 'JetBrains Mono', monospace;">v1.0.0</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Module Selection
    st.markdown("**🗂️ Modules**")
    modules = [
        ("🤖", "AI Chat", "Multi-turn conversation"),
        ("📄", "Document Q&A", "PDF, TXT, DOCX"),
        ("📊", "Data Analyst", "CSV, Excel"),
        ("🖼️", "Image Analysis", "Visual intelligence"),
        ("💻", "Code Assistant", "All languages"),
    ]

    for icon, name, desc in modules:
        label = f"{icon} {name}"
        if st.button(f"{icon} {name}  \n`{desc}`", key=f"mod_{name}", use_container_width=True):
            st.session_state.current_module = label

    st.divider()

    # API Key
    st.markdown("**🔑 API Key**")
    api_key_input = st.text_input(
        "Anthropic API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="sk-ant-...",
        help="Get your key at console.anthropic.com",
        label_visibility="collapsed",
    )
    if api_key_input:
        st.session_state.api_key = api_key_input
        os.environ["ANTHROPIC_API_KEY"] = api_key_input
        st.markdown('<span class="success-badge">✓ Key Set</span>', unsafe_allow_html=True)

    st.divider()

    # Session Stats
    st.markdown("**📈 Session Stats**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{len(st.session_state.messages)}</div>
            <div class="stat-label">Messages</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{st.session_state.session_start}</div>
            <div class="stat-label">Started</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Export & Clear
    if st.session_state.messages:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Export", use_container_width=True):
                chat_export = "\n\n".join([
                    f"**{m['role'].upper()}:** {m['content']}"
                    for m in st.session_state.messages
                ])
                st.download_button(
                    "⬇️ Download",
                    chat_export,
                    file_name=f"neuromind_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
        with col2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

    st.markdown("""
    <div style="text-align:center; margin-top:1rem;">
        <a href="https://github.com/yourusername/neuromind-ai"
           style="color: #475569; font-size: 0.75rem; text-decoration: none;">
            ⭐ Star on GitHub
        </a>
    </div>
    """, unsafe_allow_html=True)


# ── Main Content Area ─────────────────────────────────────────────────────────
def render_header(module: str):
    """Render page header for current module."""
    module_info = {
        "🤖 AI Chat": ("🤖", "AI Chat", "Multi-turn conversations with full memory & context"),
        "📄 Document Q&A": ("📄", "Document Q&A", "Upload any document and ask questions about it"),
        "📊 Data Analyst": ("📊", "Data Analyst", "AI-powered data analysis with auto-visualizations"),
        "🖼️ Image Analysis": ("🖼️", "Image Analysis", "Upload images for detailed AI-powered analysis"),
        "💻 Code Assistant": ("💻", "Code Assistant", "Write, explain, debug & optimize code"),
    }
    icon, name, desc = module_info.get(module, ("🧠", "NeuroMind AI", "Your AI assistant"))

    st.markdown(f"""
    <div class="neuromind-header">
        <div class="neuromind-title">{icon} {name}</div>
        <div class="neuromind-subtitle">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="neuromind-header">
    <div class="neuromind-title">🧠 NeuroMind AI</div>
    <div class="neuromind-subtitle">Multi-Modal Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar: API Key Status (Non-blocking!) ─────────────────────────────────
with st.sidebar:
    st.markdown("---")
    
    # Show API Status (always visible, never blocks!)
    _key = st.session_state.get("api_key", "")
    if _key:
        # Detect and show provider
        if _key.startswith("sk-or-v1"):
            st.markdown("### 🌐 OpenRouter")
            st.caption("🤖 Multi-Model Access!")
            st.success("✅ **Connected & Ready!**")
        elif _key.startswith("gsk_"):
            st.markdown("### 🟢 Groq (FREE)")
            st.caption("🤖 Llama 3.1 - Fast & Free!")
            st.success("✅ **Connected!**")
        elif _key.startswith("sk-ant-"):
            st.markdown("### 🔵 Anthropic")
            st.caption("🤖 Claude - Premium AI")
            st.success("✅ **Connected!**")
        else:
            st.markdown("### ⚪ AI Provider")
            st.success("✅ **Connected**")
        
        st.caption(f"Key: ••••{_key[-4:] if len(_key) > 4 else '****'}")
        
        if st.session_state.get("ai_model"):
            st.badge(f"Model: {st.session_state.ai_model}")
    
    # Optional: Change key (collapsed by default)
    with st.expander("⚙️ Change API Key (Optional)"):
        st.caption("**Supported Providers:**")
        st.caption("🌐 `sk-or-v1-*` → **OpenRouter** (Recommended!)")
        st.caption("🟢 `gsk_*` → **Groq** (FREE)")
        st.caption("🔵 `sk-ant-*` → **Anthropic** (Paid)")
        
        _new_key = st.text_input(
            "New API Key",
            type="password",
            placeholder="Paste new key...",
        )
        
        _col1, _col2 = st.columns(2)
        with _col1:
            if st.button("✅ Update Key", use_container_width=True, key="update_key_btn"):
                if _new_key:
                    st.session_state.api_key = _new_key
                    # Set appropriate env var
                    if _new_key.startswith("sk-or-v1"):
                        os.environ["OPENROUTER_API_KEY"] = _new_key
                    elif _new_key.startswith("gsk_"):
                        os.environ["GROQ_API_KEY"] = _new_key
                    else:
                        os.environ["ANTHROPIC_API_KEY"] = _new_key
                    st.success("✅ Key updated!")
                    st.rerun()
                else:
                    st.info("Enter a key first")
        
        with _col2:
            if st.button("🔄 Reset", use_container_width=True, key="reset_key_btn"):
                st.session_state.api_key = get_api_key()
                st.rerun()
    
    st.markdown("---")
    st.caption("💡 Get API Keys:")
    st.caption("🌐 [OpenRouter](https://openrouter.ai/keys) (Best!)")
    st.caption("🟢 [Groq](https://console.groq.com/keys) (Free)")

# NOTE: No more blocking! User goes directly to chat even without key
# (AI features just won't work until key is set)


# ── MODULES ──────────────────────────────────────────────────────────────────
current = st.session_state.current_module
render_header(current)


# ════════════════════════════════════════════════════════════════════════════
# MODULE 1: AI CHAT
# ════════════════════════════════════════════════════════════════════════════
if current == "🤖 AI Chat":

    chat_container = st.container()
    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
            <div style="text-align:center; padding: 3rem 0; color: #475569;">
                <div style="font-size: 4rem;">💬</div>
                <div style="font-size: 1.1rem; margin-top: 1rem;">Start a conversation!</div>
                <div style="font-size: 0.85rem; margin-top: 0.5rem;">
                    Ask me anything — science, coding, writing, analysis, math...
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"],
                                     avatar="👤" if msg["role"] == "user" else "🧠"):
                    st.markdown(msg["content"])

    if prompt := st.chat_input("Ask NeuroMind AI anything...", key="chat_input"):
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("Thinking..."):
                try:
                    from src.ai_core import NeuroMindAI
                    ai = NeuroMindAI(mode="chat")

                    for msg in st.session_state.messages[:-1]:
                        ai.conversation_history.append(msg)

                    response = ai.chat(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

                except Exception as e:
                    err_msg = f"❌ Error: {str(e)}"
                    st.error(err_msg)


# ════════════════════════════════════════════════════════════════════════════
# MODULE 2: DOCUMENT Q&A
# ════════════════════════════════════════════════════════════════════════════
elif current == "📄 Document Q&A":

    col1, col2 = st.columns([1, 1.5], gap="large")

    with col1:
        st.markdown("**📁 Upload Document**")
        st.markdown('<div class="upload-tip">💡 Supports PDF, TXT, MD, DOCX files</div>',
                    unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Drop your file here",
            type=["pdf", "txt", "md", "docx"],
            label_visibility="collapsed",
        )

        if uploaded:
            with st.spinner(f"📖 Reading {uploaded.name}..."):
                try:
                    from src.ai_core import NeuroMindAI
                    from src.document_qa import DocumentQA

                    ai = NeuroMindAI(mode="document_qa")
                    qa = DocumentQA(ai)
                    text, pages = qa.load_document(
                        file_bytes=uploaded.read(),
                        file_name=uploaded.name
                    )
                    st.session_state.document_content = text
                    st.session_state.document_name = uploaded.name
                    st.session_state.doc_qa = qa

                    stats = qa.get_document_stats()
                    st.success(f"✅ {uploaded.name} loaded!")
                    st.markdown(f"""
                    | Metric | Value |
                    |--------|-------|
                    | 📄 Pages | {stats['pages']} |
                    | 📝 Words | {stats['words']:,} |
                    | ⏱️ Read Time | {stats['estimated_read_time']} |
                    """)

                except Exception as e:
                    st.error(f"❌ Failed to load: {e}")

        if st.session_state.document_content:
            st.divider()
            st.markdown("**📌 Quick Actions**")
            if st.button("📋 Summarize Document", use_container_width=True):
                with st.spinner("Summarizing..."):
                    summary = st.session_state.doc_qa.summarize()
                    st.session_state.messages.append({"role": "assistant", "content": summary})

            if st.button("🔍 Extract Key Info", use_container_width=True):
                with st.spinner("Extracting..."):
                    info = st.session_state.doc_qa.extract_key_info()
                    st.session_state.messages.append({"role": "assistant", "content": info})

    with col2:
        st.markdown("**💬 Ask About the Document**")

        for msg in st.session_state.messages[-10:]:
            with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "📄"):
                st.markdown(msg["content"])

        if not st.session_state.document_content:
            st.info("👈 Upload a document first to start asking questions")
        else:
            if question := st.chat_input("Ask about the document...", key="doc_input"):
                with st.chat_message("user", avatar="👤"):
                    st.markdown(question)
                st.session_state.messages.append({"role": "user", "content": question})

                with st.chat_message("assistant", avatar="📄"):
                    with st.spinner("Analyzing document..."):
                        answer = st.session_state.doc_qa.ask(question)
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})


# ════════════════════════════════════════════════════════════════════════════
# MODULE 3: DATA ANALYST
# ════════════════════════════════════════════════════════════════════════════
elif current == "📊 Data Analyst":

    upload_col, chat_col = st.columns([1, 1.5], gap="large")

    with upload_col:
        st.markdown("**📁 Upload Data File**")
        st.markdown('<div class="upload-tip">💡 Supports CSV, Excel (.xlsx, .xls), TSV</div>',
                    unsafe_allow_html=True)

        data_file = st.file_uploader(
            "Drop data file",
            type=["csv", "xlsx", "xls", "tsv"],
            label_visibility="collapsed",
        )

        if data_file:
            with st.spinner("📊 Loading data..."):
                try:
                    from src.ai_core import NeuroMindAI
                    from src.data_analyzer import DataAnalyzer
                    import pandas as pd

                    ai = NeuroMindAI(mode="data_analyst")
                    analyzer = DataAnalyzer(ai)
                    df, stats = analyzer.load_csv(
                        file_bytes=data_file.read(),
                        file_name=data_file.name
                    )
                    st.session_state.data_df = df
                    st.session_state.data_file_name = data_file.name
                    st.session_state.data_analyzer = analyzer

                    st.success(f"✅ {data_file.name} loaded!")
                    st.markdown(f"""
                    | Metric | Value |
                    |--------|-------|
                    | 📊 Rows | {stats['shape']['rows']:,} |
                    | 📋 Columns | {stats['shape']['cols']} |
                    | ⚠️ Missing | {sum(v > 0 for v in stats['missing_values'].values())} cols |
                    | 🔁 Duplicates | {stats['duplicates']:,} |
                    """)

                except Exception as e:
                    st.error(f"❌ Load failed: {e}")

        if st.session_state.data_df is not None:
            st.divider()
            st.markdown("**📈 Visualizations**")

            viz_options = [
                "📊 Overview Dashboard",
                "🔗 Correlation Heatmap",
                "⚠️ Missing Values",
            ]
            selected_viz = st.selectbox("Choose chart", viz_options, label_visibility="collapsed")

            if st.button("🎨 Generate Chart", use_container_width=True):
                with st.spinner("Creating visualization..."):
                    try:
                        analyzer = st.session_state.data_analyzer
                        if "Dashboard" in selected_viz:
                            fig = analyzer.plot_overview_dashboard()
                        elif "Correlation" in selected_viz:
                            fig = analyzer.plot_correlation_heatmap()
                        else:
                            fig = analyzer.plot_missing_values()
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Chart error: {e}")

    with chat_col:
        st.markdown("**💬 Ask About Your Data**")

        if st.session_state.data_df is not None:
            with st.expander("👀 Data Preview (first 5 rows)"):
                st.dataframe(st.session_state.data_df.head(), use_container_width=True)

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🧠 AI Insights", use_container_width=True):
                    with st.spinner("Analyzing..."):
                        insights = st.session_state.data_analyzer.get_ai_insights()
                        st.session_state.messages.append({"role": "assistant", "content": insights})
                        st.rerun()

        for msg in st.session_state.messages[-8:]:
            with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "📊"):
                st.markdown(msg["content"])

        if st.session_state.data_df is None:
            st.info("👈 Upload a data file to start analysis")
        else:
            if question := st.chat_input("Ask about your data...", key="data_input"):
                with st.chat_message("user", avatar="👤"):
                    st.markdown(question)
                st.session_state.messages.append({"role": "user", "content": question})

                with st.chat_message("assistant", avatar="📊"):
                    with st.spinner("Analyzing..."):
                        answer = st.session_state.data_analyzer.ask_about_data(question)
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})


# ════════════════════════════════════════════════════════════════════════════
# MODULE 4: IMAGE ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
elif current == "🖼️ Image Analysis":

    left, right = st.columns([1, 1.5], gap="large")

    with left:
        st.markdown("**📁 Upload Image**")
        st.markdown('<div class="upload-tip">💡 Supports JPG, PNG, WEBP, GIF, BMP</div>',
                    unsafe_allow_html=True)

        img_file = st.file_uploader(
            "Upload image",
            type=["jpg", "jpeg", "png", "webp", "gif", "bmp"],
            label_visibility="collapsed",
        )

        if img_file:
            img = Image.open(img_file)
            st.image(img, caption=img_file.name, use_column_width=True)
            st.markdown(f"""
            | Property | Value |
            |----------|-------|
            | 📐 Size | {img.size[0]} × {img.size[1]} px |
            | 🎨 Mode | {img.mode} |
            | 📄 Format | {img.format or img_file.type} |
            """)
            st.session_state.current_image = img_file

    with right:
        st.markdown("**🤖 Image Intelligence**")

        if "current_image" not in st.session_state:
            st.info("👈 Upload an image to analyze")
        else:
            cols = st.columns(2)
            quick_prompts = [
                ("🔍 Describe", "Provide a detailed description of everything in this image."),
                ("📝 Extract Text", "Extract and list all text visible in this image."),
                ("🏷️ Identify Objects", "List all objects, items, and elements you can identify."),
                ("🎨 Analyze Style", "Analyze the visual style, composition, colors, and artistic elements."),
            ]

            for i, (label, prompt) in enumerate(quick_prompts):
                with cols[i % 2]:
                    if st.button(label, use_container_width=True, key=f"img_btn_{i}"):
                        with st.spinner("Analyzing image..."):
                            try:
                                from src.ai_core import NeuroMindAI
                                ai = NeuroMindAI(mode="image_analyst")
                                img_bytes = st.session_state.current_image.getvalue()
                                media_type = f"image/{st.session_state.current_image.type.split('/')[-1]}"
                                response = ai.chat_with_image_bytes(prompt, img_bytes, media_type)
                                st.session_state.messages.append({"role": "user", "content": label})
                                st.session_state.messages.append({"role": "assistant", "content": response})
                                st.rerun()
                            except Exception as e:
                                st.error(f"Analysis failed: {e}")

            st.divider()

            for msg in st.session_state.messages[-6:]:
                with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🖼️"):
                    st.markdown(msg["content"])

            if custom := st.chat_input("Ask about the image...", key="img_input"):
                with st.chat_message("user", avatar="👤"):
                    st.markdown(custom)
                st.session_state.messages.append({"role": "user", "content": custom})

                with st.chat_message("assistant", avatar="🖼️"):
                    with st.spinner("Analyzing..."):
                        from src.ai_core import NeuroMindAI
                        ai = NeuroMindAI(mode="image_analyst")
                        img_bytes = st.session_state.current_image.getvalue()
                        response = ai.chat_with_image_bytes(custom, img_bytes)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})


# ════════════════════════════════════════════════════════════════════════════
# MODULE 5: CODE ASSISTANT
# ════════════════════════════════════════════════════════════════════════════
elif current == "💻 Code Assistant":

    st.markdown('<div class="upload-tip">💡 I can write, explain, debug, and optimize code in any language</div>',
                unsafe_allow_html=True)

    action_cols = st.columns(5)
    quick_actions = [
        ("✍️ Write Code", "Write"),
        ("🔍 Explain Code", "Explain"),
        ("🐛 Debug Code", "Debug"),
        ("⚡ Optimize Code", "Optimize"),
        ("🧪 Write Tests", "Tests"),
    ]

    selected_action = "Write"
    for i, (label, action) in enumerate(quick_actions):
        with action_cols[i]:
            if st.button(label, use_container_width=True, key=f"code_action_{i}"):
                st.session_state.code_action = action
                selected_action = action

    action = st.session_state.get("code_action", "Write")

    col1, col2 = st.columns([1, 3])
    with col1:
        language = st.selectbox(
            "Language",
            ["Python", "JavaScript", "TypeScript", "Java", "C++", "Rust", "Go",
             "SQL", "HTML/CSS", "Bash", "R", "Kotlin", "Swift", "Other"],
        )

    with col2:
        placeholder_map = {
            "Write": f"Describe what you want me to code in {language}...",
            "Explain": "Paste your code here and I'll explain it step by step...",
            "Debug": "Paste your buggy code + error message here...",
            "Optimize": "Paste code to optimize for performance/readability...",
            "Tests": "Paste the function/class you want tests written for...",
        }
        code_input = st.text_area(
            "Your request or code",
            height=180,
            placeholder=placeholder_map.get(action, "Enter your code or request..."),
            label_visibility="collapsed",
        )

    if st.button(f"🚀 {action} with AI", type="primary", use_container_width=True):
        if code_input.strip():
            prompt_map = {
                "Write": f"Write {language} code for: {code_input}",
                "Explain": f"Explain this {language} code step by step:\n\n```{language.lower()}\n{code_input}\n```",
                "Debug": f"Debug this {language} code and fix all issues:\n\n```{language.lower()}\n{code_input}\n```",
                "Optimize": f"Optimize this {language} code for performance and readability:\n\n```{language.lower()}\n{code_input}\n```",
                "Tests": f"Write comprehensive unit tests for this {language} code:\n\n```{language.lower()}\n{code_input}\n```",
            }

            full_prompt = prompt_map.get(action, code_input)

            with st.chat_message("user", avatar="👤"):
                st.markdown(f"**[{action} Code — {language}]** {code_input[:100]}...")
            st.session_state.messages.append({"role": "user", "content": full_prompt})

            with st.chat_message("assistant", avatar="💻"):
                with st.spinner(f"🧠 {action}ing {language} code..."):
                    try:
                        from src.ai_core import NeuroMindAI
                        ai = NeuroMindAI(mode="code_assistant")
                        response = ai.chat(full_prompt)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.warning("Please enter code or a description first.")

    st.divider()
    st.markdown("**💬 Conversation History**")
    for msg in st.session_state.messages[-8:]:
        with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "💻"):
            st.markdown(msg["content"])

    if code_follow := st.chat_input("Follow-up question about the code...", key="code_follow"):
        with st.chat_message("user", avatar="👤"):
            st.markdown(code_follow)
        st.session_state.messages.append({"role": "user", "content": code_follow})

        with st.chat_message("assistant", avatar="💻"):
            with st.spinner("Coding..."):
                from src.ai_core import NeuroMindAI
                ai = NeuroMindAI(mode="code_assistant")
                for msg in st.session_state.messages[:-1]:
                    ai.conversation_history.append(msg)
                response = ai.chat(code_follow)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
