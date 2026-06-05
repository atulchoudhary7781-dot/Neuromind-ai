"""
NeuroMind AI — Package Setup
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = [
        line.strip()
        for line in f
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="neuromind-ai",
    version="1.0.0",
    author="NeuroMind AI Team",
    description="Multi-Modal AI Assistant Platform built with Claude API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/neuromind-ai",
    packages=find_packages(exclude=["tests*", "examples*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "neuromind-demo=examples.demo:main",
        ],
    },
    keywords="ai, llm, claude, anthropic, chatbot, nlp, machine-learning",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/neuromind-ai/issues",
        "Source": "https://github.com/yourusername/neuromind-ai",
    },
)
