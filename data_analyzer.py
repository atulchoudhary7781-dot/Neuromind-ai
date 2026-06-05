"""
NeuroMind AI — Data Analyst Module
=====================================
AI-powered CSV/Excel data analysis with automatic visualizations.

Author: NeuroMind AI Team
"""

import io
import json
from typing import Optional

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class DataAnalyzer:
    """
    Intelligent data analysis engine for NeuroMind AI.

    Loads CSV/Excel files, generates statistics, creates
    beautiful visualizations, and provides AI-powered insights.

    Example:
        >>> analyzer = DataAnalyzer(ai_engine)
        >>> df, summary = analyzer.load_csv("sales.csv")
        >>> insights = analyzer.get_ai_insights()
        >>> fig = analyzer.plot_distribution("revenue")
    """

    def __init__(self, ai_engine):
        """
        Initialize with a NeuroMindAI engine instance.

        Args:
            ai_engine: Instance of NeuroMindAI
        """
        self.ai = ai_engine
        self.df: Optional[pd.DataFrame] = None
        self.file_name: str = ""
        self._color_palette = px.colors.qualitative.Vivid

    def load_csv(self, file_path: str = "", file_bytes: bytes = b"",
                 file_name: str = "") -> tuple[pd.DataFrame, dict]:
        """
        Load data from CSV or Excel file.

        Args:
            file_path: Path to data file (optional)
            file_bytes: Raw file bytes (optional)
            file_name: Original filename

        Returns:
            Tuple of (DataFrame, summary_stats_dict)
        """
        self.file_name = file_name or file_path

        if file_path:
            ext = file_path.rsplit(".", 1)[-1].lower()
            if ext == "csv":
                self.df = pd.read_csv(file_path)
            elif ext in ("xlsx", "xls"):
                self.df = pd.read_excel(file_path)
            elif ext == "tsv":
                self.df = pd.read_csv(file_path, sep="\t")
        else:
            ext = file_name.rsplit(".", 1)[-1].lower() if file_name else "csv"
            data_io = io.BytesIO(file_bytes)
            if ext == "csv":
                self.df = pd.read_csv(data_io)
            elif ext in ("xlsx", "xls"):
                self.df = pd.read_excel(data_io)
            elif ext == "tsv":
                self.df = pd.read_csv(data_io, sep="\t")

        # Clean column names
        self.df.columns = self.df.columns.str.strip()

        return self.df, self.get_summary_stats()

    def get_summary_stats(self) -> dict:
        """
        Generate comprehensive summary statistics.

        Returns:
            Dictionary with shape, dtypes, missing values, stats
        """
        if self.df is None:
            return {}

        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = self.df.select_dtypes(include=["object", "category"]).columns.tolist()

        return {
            "shape": {"rows": self.df.shape[0], "cols": self.df.shape[1]},
            "columns": self.df.columns.tolist(),
            "dtypes": self.df.dtypes.astype(str).to_dict(),
            "numeric_cols": numeric_cols,
            "categorical_cols": categorical_cols,
            "missing_values": self.df.isnull().sum().to_dict(),
            "missing_pct": (self.df.isnull().sum() / len(self.df) * 100).round(2).to_dict(),
            "duplicates": int(self.df.duplicated().sum()),
            "memory_mb": round(self.df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
            "numeric_stats": self.df[numeric_cols].describe().round(3).to_dict() if numeric_cols else {},
        }

    def get_ai_insights(self) -> str:
        """
        Use AI to generate deep insights about the dataset.

        Returns:
            AI-generated insights as formatted text
        """
        if self.df is None:
            return "❌ No data loaded."

        stats = self.get_summary_stats()
        sample_data = self.df.head(5).to_string()

        prompt = f"""I have a dataset with the following characteristics. Please provide expert data analysis insights.

**Dataset:** {self.file_name}
**Shape:** {stats['shape']['rows']:,} rows × {stats['shape']['cols']} columns

**Columns:** {', '.join(stats['columns'])}

**Data Types:**
{json.dumps(stats['dtypes'], indent=2)}

**Missing Values:**
{json.dumps({k: f"{v} ({stats['missing_pct'][k]:.1f}%)" for k, v in stats['missing_values'].items() if v > 0}, indent=2) or "None detected ✅"}

**Duplicated Rows:** {stats['duplicates']:,}

**Sample Data (first 5 rows):**
{sample_data}

**Statistical Summary:**
{json.dumps({k: {s: round(v, 2) for s, v in vs.items()} for k, vs in stats.get('numeric_stats', {}).items()}, indent=2)}

Please provide:
1. 📊 **Dataset Overview** - What kind of data is this?
2. 🔍 **Key Observations** - Top 5 most important findings
3. ⚠️ **Data Quality Issues** - Problems to fix before analysis
4. 📈 **Trends & Patterns** - Visible patterns in the data
5. 💡 **Recommended Analysis** - What analyses would be most valuable?
6. 🎯 **Actionable Insights** - What decisions could this data inform?"""

        return self.ai.quick_ask(prompt, system=self._get_system_prompt())

    def ask_about_data(self, question: str) -> str:
        """
        Ask a natural language question about the data.

        Args:
            question: Question about the dataset

        Returns:
            AI-generated answer
        """
        if self.df is None:
            return "❌ No data loaded."

        # Get relevant stats based on question
        stats = self.get_summary_stats()
        sample = self.df.head(10).to_string()

        # Try to compute relevant stats
        computed_stats = self._compute_relevant_stats(question)

        prompt = f"""Dataset: {self.file_name} ({stats['shape']['rows']:,} rows, {stats['shape']['cols']} cols)
Columns: {', '.join(stats['columns'])}

Sample Data:
{sample}

{f"Computed Statistics: {computed_stats}" if computed_stats else ""}

User Question: {question}

Please answer this question about the dataset. Use numbers and specific column names.
If the question requires computation you can't do, explain what the result would look like and how to compute it."""

        return self.ai.quick_ask(prompt, system=self._get_system_prompt())

    # ── Visualization Methods ────────────────────────────────────────────────

    def plot_overview_dashboard(self) -> go.Figure:
        """
        Create a complete dashboard overview of the dataset.

        Returns:
            Plotly figure with multiple subplots
        """
        if self.df is None:
            raise ValueError("No data loaded.")

        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()[:4]
        cat_cols = self.df.select_dtypes(include=["object"]).columns.tolist()[:2]

        plots_needed = len(numeric_cols) + len(cat_cols)
        rows = max(1, (plots_needed + 1) // 2)
        cols = 2

        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=[f"Distribution: {c}" for c in numeric_cols] +
                           [f"Top Values: {c}" for c in cat_cols],
            vertical_spacing=0.12,
            horizontal_spacing=0.08,
        )

        colors = self._color_palette

        # Add numeric distributions (histograms)
        for i, col in enumerate(numeric_cols):
            row = (i // 2) + 1
            col_pos = (i % 2) + 1
            fig.add_trace(
                go.Histogram(
                    x=self.df[col].dropna(),
                    name=col,
                    marker_color=colors[i % len(colors)],
                    showlegend=False,
                    nbinsx=20,
                ),
                row=row, col=col_pos
            )

        # Add categorical bar charts
        for j, col in enumerate(cat_cols):
            idx = len(numeric_cols) + j
            row = (idx // 2) + 1
            col_pos = (idx % 2) + 1
            top_vals = self.df[col].value_counts().head(8)
            fig.add_trace(
                go.Bar(
                    x=top_vals.index.tolist(),
                    y=top_vals.values.tolist(),
                    name=col,
                    marker_color=colors[(j + 4) % len(colors)],
                    showlegend=False,
                ),
                row=row, col=col_pos
            )

        fig.update_layout(
            title=f"📊 Dataset Dashboard: {self.file_name}",
            height=400 * rows,
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(26,26,46,0.8)",
            font=dict(color="white", family="monospace"),
            title_font_size=18,
        )

        return fig

    def plot_correlation_heatmap(self) -> go.Figure:
        """Generate a correlation heatmap for numeric columns."""
        numeric_df = self.df.select_dtypes(include=[np.number])

        if numeric_df.shape[1] < 2:
            raise ValueError("Need at least 2 numeric columns for correlation analysis.")

        corr = numeric_df.corr().round(3)

        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns.tolist(),
            y=corr.columns.tolist(),
            colorscale="RdBu",
            zmid=0,
            text=corr.values.round(2),
            texttemplate="%{text}",
            showscale=True,
        ))

        fig.update_layout(
            title="🔗 Correlation Heatmap",
            template="plotly_dark",
            height=500,
            paper_bgcolor="rgba(26,26,46,0.8)",
            font=dict(color="white"),
        )

        return fig

    def plot_missing_values(self) -> go.Figure:
        """Visualize missing value distribution across columns."""
        missing = self.df.isnull().sum()
        missing = missing[missing > 0]

        if missing.empty:
            # Show "no missing values" chart
            fig = go.Figure()
            fig.add_annotation(
                text="✅ No Missing Values!",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=24, color="#10B981")
            )
            fig.update_layout(template="plotly_dark", height=200)
            return fig

        pct = (missing / len(self.df) * 100).round(2)

        fig = go.Figure(go.Bar(
            x=missing.index.tolist(),
            y=pct.values.tolist(),
            marker_color=["#EF4444" if p > 20 else "#F59E0B" if p > 5 else "#10B981"
                         for p in pct.values],
            text=[f"{p:.1f}%" for p in pct.values],
            textposition="outside",
        ))

        fig.update_layout(
            title="⚠️ Missing Values by Column (%)",
            yaxis_title="Missing %",
            template="plotly_dark",
            height=400,
            paper_bgcolor="rgba(26,26,46,0.8)",
            font=dict(color="white"),
        )

        return fig

    def plot_distribution(self, column: str) -> go.Figure:
        """Plot distribution of a specific numeric column."""
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found.")

        series = self.df[column].dropna()

        fig = make_subplots(rows=1, cols=2,
                            subplot_titles=["Histogram", "Box Plot"])

        fig.add_trace(
            go.Histogram(x=series, marker_color="#7C3AED", name="Distribution"),
            row=1, col=1
        )

        fig.add_trace(
            go.Box(y=series, marker_color="#06B6D4", name="Box Plot",
                   boxpoints="outliers"),
            row=1, col=2
        )

        fig.update_layout(
            title=f"📈 Distribution Analysis: {column}",
            template="plotly_dark",
            height=400,
            paper_bgcolor="rgba(26,26,46,0.8)",
            font=dict(color="white"),
            showlegend=False,
        )

        return fig

    # ── Private Helpers ──────────────────────────────────────────────────────

    def _compute_relevant_stats(self, question: str) -> str:
        """Try to compute stats relevant to the question."""
        if self.df is None:
            return ""

        try:
            question_lower = question.lower()
            results = []

            numeric_cols = self.df.select_dtypes(include=[np.number]).columns

            if any(word in question_lower for word in ["average", "mean", "avg"]):
                means = self.df[numeric_cols].mean().round(2).to_dict()
                results.append(f"Means: {means}")

            if any(word in question_lower for word in ["max", "maximum", "highest", "largest"]):
                maxes = self.df[numeric_cols].max().to_dict()
                results.append(f"Maximums: {maxes}")

            if any(word in question_lower for word in ["min", "minimum", "lowest", "smallest"]):
                mins = self.df[numeric_cols].min().to_dict()
                results.append(f"Minimums: {mins}")

            if "count" in question_lower or "how many" in question_lower:
                results.append(f"Total rows: {len(self.df):,}")

            return " | ".join(results)
        except Exception:
            return ""

    def _get_system_prompt(self) -> str:
        from config import SYSTEM_PROMPTS
        return SYSTEM_PROMPTS["data_analyst"]
