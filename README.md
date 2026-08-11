<div align="center">

```
███╗   ██╗███████╗██╗   ██╗██████╗  ██████╗ ███╗   ███╗██╗███╗   ██╗██████╗     █████╗ ██╗
████╗  ██║██╔════╝██║   ██║██╔══██╗██╔═══██╗████╗ ████║██║████╗  ██║██╔══██╗   ██╔══██╗██║
██╔██╗ ██║█████╗  ██║   ██║██████╔╝██║   ██║██╔████╔██║██║██╔██╗ ██║██║  ██║   ███████║██║
██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██║   ██║██║╚██╔╝██║██║██║╚██╗██║██║  ██║   ██╔══██║██║
██║ ╚████║███████╗╚██████╔╝██║  ██║╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██████╔╝   ██║  ██║██║
╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝    ╚═╝  ╚═╝╚═╝
```

# 🧠 NeuroMind AI — Multi-Modal Intelligence Platform

**Your all-in-one AI-powered research, analysis & assistant platform**

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Click_Here-success?style=for-the-badge&logo=streamlit&logoColor=white)](https://i9fm8n3pz2wn67bkro5y2q.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![OpenRouter](https://img.shields.io/badge/OpenRouter_API-Multi_Model-orange?style=for-the-badge)](https://openrouter.ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)

---

> **NeuroMind AI** is a production-grade, multi-modal AI assistant platform that combines conversational AI, document understanding, intelligent data analysis, image recognition, and code assistance — all in one beautiful interface.
>
> 🔗 **[Try it live now!](https://i9fm8n3pz2wn67bkro5y2q.streamlit.app/)** — No setup required!

</div>

---

## ✨ Features

| Feature | Description | Status |
|---------|-------------|--------|
| 🤖 **AI Chat** | Multi-turn conversations with memory & context | ✅ Ready |
| 📄 **Document Q&A** | Upload PDF/TXT → Ask questions instantly | ✅ Ready |
| 📊 **Data Analyst** | Upload CSV → Get AI-powered insights + charts | ✅ Ready |
| 🖼️ **Image Analysis** | Upload images → Get detailed AI descriptions | ✅ Ready |
| 💻 **Code Assistant** | Write, explain, debug, optimize code in any language | ✅ Ready |
| 🧠 **Conversation Memory** | Full session history with export capability | ✅ Ready |
| 🎨 **Beautiful UI** | Dark-themed, responsive Streamlit interface | ✅ Ready |
| 📤 **Export Results** | Download analysis, chat history as Markdown/JSON | ✅ Ready |

---

## 🌐 Live Demo

👉 **[**Try NeuroMind AI Now →**](https://i9fm8n3pz2wn67bkro5y2q.streamlit.app/)**

No installation required! Just click and start chatting with AI.

---

## 🖥️ App Preview

```
┌─────────────────────────────────────────────────────────┐
│  🧠 NeuroMind AI                          [Dark Theme]  │
├──────────────┬──────────────────────────────────────────┤
│              │                                          │
│  🤖 AI Chat  │   Hello! How can I help you today?      │
│  📄 Doc Q&A  │   ──────────────────────────────────   │
│  📊 Data     │   User: Explain quantum computing        │
│  🖼️ Images   │   AI: Quantum computing uses qubits...  │
│  💻 Code     │                                          │
│              │   [  Send Message  ]                     │
└──────────────┴──────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/neuromind-ai.git
cd neuromind-ai
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App (API Key Pre-configured!)
```bash
# The app comes with pre-configured API key!
# Just run:
streamlit run app.py
```

🎉 **Or use it online:** [https://i9fm8n3pz2wn67bkro5y2q.streamlit.app/](https://i9fm8n3pz2wn67bkro5y2q.streamlit.app/)

🎉 Open your browser at `http://localhost:8501`

---

## 🔑 API Configuration

**Good news!** The app comes with a **pre-configured API key** — no setup needed!

If you want to use your own key:
1. Get a free key from [OpenRouter](https://openrouter.ai/keys) (recommended!)
2. Or use [Groq](https://console.groq.com/keys) (free tier available)
3. Set it as environment variable `OPENROUTER_API_KEY`

---

## 📁 Project Structure

```
neuromind-ai/
│
├── 📄 app.py                    # Main Streamlit application
├── ⚙️  config.py                 # Configuration & settings
├── 📋 requirements.txt          # Python dependencies
├── 🔒 .env.example              # Environment variables template
├── 📖 README.md                 # You are here!
│
├── 📦 src/
│   ├── __init__.py
│   ├── ai_core.py               # Claude API integration & AI logic
│   ├── memory.py                # Conversation memory management
│   ├── document_qa.py           # PDF/TXT document processing & Q&A
│   ├── data_analyzer.py         # CSV data analysis with Pandas + AI
│   ├── image_analyzer.py        # Image processing & vision analysis
│   ├── code_assistant.py        # Code generation, explanation & debug
│   └── utils.py                 # Helper utilities
│
├── 🧪 tests/
│   ├── test_ai_core.py
│   ├── test_document_qa.py
│   └── test_data_analyzer.py
│
└── 💡 examples/
    ├── demo_chat.py
    ├── demo_data_analysis.py
    └── sample_data.csv
```

---

## 🛠️ Tech Stack

```python
tech_stack = {
    "AI Engine":        "OpenRouter API (Multi-model support)",
    "UI Framework":     "Streamlit 1.35+",
    "Data Processing":  "Pandas + NumPy",
    "Visualizations":   "Plotly Express",
    "PDF Processing":   "PyMuPDF (fitz)",
    "Image Processing": "Pillow (PIL)",
    "Memory Store":     "Python dataclasses + JSON",
    "Config":           "python-dotenv",
    "Styling":          "Custom CSS + Streamlit components",
}
```

---

## 📊 How Each Module Works

### 🤖 AI Chat Module
```python
# Multi-turn conversation with full context window
from src.ai_core import NeuroMindAI

ai = NeuroMindAI()
response = ai.chat("Explain neural networks simply")
print(response)  # → Clear, contextual explanation
```

### 📄 Document Q&A Module
```python
# Upload any PDF/TXT and ask questions
from src.document_qa import DocumentQA

qa = DocumentQA()
qa.load_document("research_paper.pdf")
answer = qa.ask("What are the main findings?")
```

### 📊 Data Analyst Module
```python
# Upload CSV, get instant AI insights + charts
from src.data_analyzer import DataAnalyzer

analyzer = DataAnalyzer()
analyzer.load_csv("sales_data.csv")
insights = analyzer.analyze()  # Returns AI-generated insights + plots
```

---

## 🌟 Advanced Usage

### Using System Prompts
```python
ai = NeuroMindAI(
    system_prompt="You are an expert Python developer. Always provide code examples."
)
```

### Exporting Conversation History
```python
# In the UI: sidebar → Export Chat → Download as JSON/Markdown
# Or programmatically:
ai.memory.export_to_markdown("my_conversation.md")
```

### Batch Document Analysis
```python
from src.document_qa import DocumentQA

qa = DocumentQA()
questions = ["Summary?", "Key findings?", "Recommendations?"]
for doc in ["doc1.pdf", "doc2.pdf"]:
    qa.load_document(doc)
    for q in questions:
        print(f"[{doc}] {q} → {qa.ask(q)}")
```

---

## ⚙️ Configuration

Edit `config.py` or set environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | Pre-configured ✅ |
| `MODEL_NAME` | AI model to use | `meta-llama/llama-3.1-8b-instruct` |
| `MAX_TOKENS` | Max response tokens | `4096` |
| `TEMPERATURE` | Response creativity (0-1) | `0.7` |
| `MAX_MEMORY_TURNS` | Conversation turns to remember | `20` |

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html

# Run specific module tests
pytest tests/test_ai_core.py -v
```

---

## 🤝 Contributing

Contributions are warmly welcome! Here's how:

1. **Fork** the repository
2. Create a **feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. Open a **Pull Request**

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📈 Roadmap

- [ ] 🔊 Voice input/output support (Whisper API)
- [ ] 🌐 Web scraping & real-time search integration
- [ ] 🧩 Plugin system for custom tools
- [ ] 📱 Mobile-responsive UI improvements
- [ ] 🐳 Docker containerization
- [x] ☁️ One-click Streamlit Cloud deployment ✅
- [ ] 🔗 LangChain integration
- [ ] 💾 PostgreSQL conversation persistence

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [OpenRouter](https://openrouter.ai/) for multi-model AI access
- [Streamlit](https://streamlit.io/) for the amazing app framework
- The open-source Python community 💙

---

<div align="center">

**Made with ❤️ and Python**

⭐ **Star this repo if you found it helpful!** ⭐

*If you use NeuroMind AI in your project, I'd love to hear about it!*

</div>
