# 🤝 Contributing to NeuroMind AI

Thank you for your interest in contributing! Here's how to get started.

## 🚀 Quick Start

1. **Fork** the repo → Click "Fork" on GitHub
2. **Clone** your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/neuromind-ai.git
   cd neuromind-ai
   ```
3. **Set up dev environment**:
   ```bash
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env  # Add your API key
   ```

## 🛠️ Development Workflow

```bash
# Create a feature branch
git checkout -b feature/your-amazing-feature

# Make changes, then test
pytest tests/ -v

# Commit with a descriptive message
git commit -m "feat: add voice input support"

# Push and open a Pull Request
git push origin feature/your-amazing-feature
```

## 📋 Contribution Guidelines

- Follow **PEP 8** Python style
- Write **docstrings** for all public functions
- Add **tests** for new features
- Keep commits focused and descriptive
- Update `README.md` if needed

## 🐛 Reporting Bugs

Open an issue with:
- Python version & OS
- Steps to reproduce
- Expected vs actual behavior
- Error message / traceback

## 💡 Suggesting Features

Open an issue labeled `enhancement` with:
- Use case description
- Proposed implementation approach

## 📜 Code of Conduct

Be kind, respectful, and constructive. We're all here to build something great together! 🚀
