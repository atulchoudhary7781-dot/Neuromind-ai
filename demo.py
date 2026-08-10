"""
NeuroMind AI — Demo Script
============================
Run this to see NeuroMind AI in action from the terminal.

Usage: python examples/demo.py
"""

# ════════════════════════════════════════════════════════════════════════════════
# CRITICAL: Path Setup (MUST be first - before any other imports)
# ════════════════════════════════════════════════════════════════════════════════
import os as _os, sys as _sys
_SCRIPT_DIR = _os.path.dirname(_os.path.abspath(__file__))
if _SCRIPT_DIR not in _sys.path:
    _sys.path.insert(0, _SCRIPT_DIR)

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.theme import Theme
from rich import print as rprint

# Custom theme
theme = Theme({
    "ai": "bold magenta",
    "user": "bold cyan",
    "success": "bold green",
    "error": "bold red",
    "info": "dim white",
})
console = Console(theme=theme)


def print_banner():
    """Print the NeuroMind AI banner."""
    console.print(Panel.fit(
        "[bold magenta]🧠 NeuroMind AI[/bold magenta] [dim]— Demo Mode[/dim]\n"
        "[dim]Multi-Modal Intelligence Platform v1.0.0[/dim]",
        border_style="magenta",
        padding=(1, 4),
    ))


def demo_chat():
    """Demo the chat functionality."""
    console.print("\n[bold cyan]══ Demo: AI Chat ══[/bold cyan]\n")

    from src.ai_core import NeuroMindAI
    ai = NeuroMindAI(mode="chat")

    questions = [
        "What is machine learning in simple terms?",
        "Give me 3 real-world applications of AI.",
    ]

    for q in questions:
        console.print(f"[user]👤 You:[/user] {q}")

        with Progress(
            SpinnerColumn(),
            TextColumn("[ai]🧠 NeuroMind AI is thinking...[/ai]"),
            transient=True,
        ) as progress:
            progress.add_task("", total=None)
            response = ai.chat(q)

        console.print(Panel(
            Markdown(response),
            title="[ai]🧠 NeuroMind AI[/ai]",
            border_style="magenta",
            padding=(0, 1),
        ))
        console.print()


def demo_data_analysis():
    """Demo with a sample CSV."""
    console.print("\n[bold cyan]══ Demo: Data Analysis ══[/bold cyan]\n")

    import csv
    import io
    from src.ai_core import NeuroMindAI
    from src.data_analyzer import DataAnalyzer

    # Create sample data
    sample_csv = """product,sales,revenue,region,quarter
Laptop,150,225000,North,Q1
Phone,320,96000,South,Q1
Tablet,85,42500,East,Q1
Laptop,180,270000,North,Q2
Phone,290,87000,South,Q2
Tablet,110,55000,West,Q2
Laptop,210,315000,East,Q3
Phone,400,120000,North,Q3
Tablet,95,47500,South,Q3"""

    console.print("[info]📊 Analyzing sample sales data...[/info]\n")

    ai = NeuroMindAI(mode="data_analyst")
    analyzer = DataAnalyzer(ai)
    df, stats = analyzer.load_csv(
        file_bytes=sample_csv.encode(),
        file_name="sales_demo.csv"
    )

    # Display stats table
    table = Table(title="📊 Dataset Overview", border_style="cyan")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Rows", f"{stats['shape']['rows']:,}")
    table.add_row("Columns", str(stats['shape']['cols']))
    table.add_row("Numeric Columns", ", ".join(stats['numeric_cols']))
    table.add_row("Categorical Columns", ", ".join(stats['categorical_cols']))
    table.add_row("Missing Values", "None ✅")

    console.print(table)
    console.print()

    # Get AI insights
    console.print("[info]🧠 Generating AI insights...[/info]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[ai]Analyzing data...[/ai]"),
        transient=True,
    ) as progress:
        progress.add_task("", total=None)
        insights = analyzer.get_ai_insights()

    console.print(Panel(
        Markdown(insights),
        title="[ai]🤖 AI Data Insights[/ai]",
        border_style="magenta",
    ))


def demo_code_assistant():
    """Demo the code assistant."""
    console.print("\n[bold cyan]══ Demo: Code Assistant ══[/bold cyan]\n")

    from src.ai_core import NeuroMindAI
    ai = NeuroMindAI(mode="code_assistant")

    prompt = "Write a Python function to find prime numbers up to N using the Sieve of Eratosthenes. Include docstring and example usage."

    console.print(f"[user]👤 Request:[/user] {prompt}\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[ai]💻 Writing code...[/ai]"),
        transient=True,
    ) as progress:
        progress.add_task("", total=None)
        code = ai.chat(prompt)

    console.print(Panel(
        Markdown(code),
        title="[ai]💻 Generated Code[/ai]",
        border_style="magenta",
    ))


def main():
    """Run the demo."""
    print_banner()

    console.print(
        "\n[bold]Welcome to NeuroMind AI Demo![/bold]\n"
        "[dim]This demo showcases the core capabilities.\n"
        "Make sure ANTHROPIC_API_KEY is set in your .env file.[/dim]\n"
    )

    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print(
            "[error]❌ ANTHROPIC_API_KEY not found![/error]\n"
            "[info]Please set it in .env or export it:\n"
            "  export ANTHROPIC_API_KEY=sk-ant-...[/info]"
        )
        sys.exit(1)

    try:
        demo_chat()
        demo_data_analysis()
        demo_code_assistant()

        console.print(Panel.fit(
            "[success]✅ Demo complete! All features working.[/success]\n\n"
            "[dim]To run the full web app:[/dim]\n"
            "[bold]streamlit run app.py[/bold]",
            border_style="green",
            padding=(1, 4),
        ))

    except Exception as e:
        console.print(f"\n[error]❌ Demo error: {e}[/error]")
        console.print("[info]Make sure you have a valid API key and all dependencies installed.[/info]")
        sys.exit(1)


if __name__ == "__main__":
    main()
