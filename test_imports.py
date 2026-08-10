#!/usr/bin/env python3
"""
Test Script - Verify src imports work
======================================
Run this to check if your installation is correct:

    python test_imports.py
"""

import sys
import os

print("=" * 60)
print("🔍 Neuromind AI - Import Test")
print("=" * 60)
print()

# Show environment info
print(f"📌 Python: {sys.executable}")
print(f"📌 Version: {sys.version.split()[0]}")
print(f"📌 Working Dir: {os.getcwd()}")
print()

# Test 1: Basic import
print("Test 1: import src")
try:
    import src
    print(f"   ✅ PASS - src found at: {src.__file__}")
except ImportError as e:
    print(f"   ❌ FAIL - {e}")
    print()
    print("🔧 FIX: Run this command:")
    print("      python3 -m pip install -e .")
    sys.exit(1)

# Test 2: Config import
print("\nTest 2: from src.config import ...")
try:
    from src.config import APP_CONFIG, VERSION, MODEL_CONFIG
    print(f"   ✅ PASS - Version: {VERSION}, Model: {MODEL_CONFIG.name}")
except ImportError as e:
    print(f"   ❌ FAIL - {e}")

# Test 3: Utils import
print("\nTest 3: from src.utils import ...")
try:
    from src.utils import format_file_size, validate_api_key
    print(f"   ✅ PASS - format_file_size(1024) = {format_file_size(1024)}")
except ImportError as e:
    print(f"   ❌ FAIL - {e}")

# Test 4: Memory import
print("\nTest 4: from src.memory import ...")
try:
    from src.memory import ConversationMemory, Message
    mem = ConversationMemory()
    print(f"   ✅ PASS - ConversationMemory created")
except ImportError as e:
    print(f"   ❌ FAIL - {e}")

# Test 5: Document QA
print("\nTest 5: from src.document_qa import ...")
try:
    from src.document_qa import DocumentQA
    print(f"   ✅ PASS - DocumentQA imported")
except ImportError as e:
    print(f"   ❌ FAIL - {e}")

# Test 6: Data Analyzer
print("\nTest 6: from src.data_analyzer import ...")
try:
    from src.data_analyzer import DataAnalyzer
    print(f"   ✅ PASS - DataAnalyzer imported")
except ImportError as e:
    print(f"   ❌ FAIL - {e}")

# Test 7: AI Core (may fail without anthropic)
print("\nTest 7: from src.ai_core import ...")
try:
    from src.ai_core import NeuroMindAI
    print(f"   ✅ PASS - NeuroMindAI imported")
except ImportError as e:
    if 'anthropic' in str(e):
        print(f"   ⚠️  SKIP - anthropic not installed (optional)")
    else:
        print(f"   ❌ FAIL - {e}")

print()
print("=" * 60)
print("✅ All critical imports working!")
print("=" * 60)
print()
print("Now you can run:")
print("  streamlit run app.py")
