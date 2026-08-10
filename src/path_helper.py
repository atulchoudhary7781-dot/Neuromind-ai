"""
NeuroMind AI — Path Helper Utility
===================================
Provides path configuration utilities for reliable imports.

IMPORTANT: Before using this module, you MUST ensure the project root 
is in sys.path. Add this at the TOP of your entry point scripts:

    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from src.path_helper import setup_path
    setup_path()

Or simply use the bootstrap function below in your scripts.
"""

import os
import sys
from pathlib import Path


def setup_path() -> str:
    """
    Ensure project root is in sys.path for reliable 'from src.xxx' imports.
    
    Returns:
        str: The absolute path to the project root directory
        
    Example:
        >>> from src.path_helper import setup_path
        >>> root = setup_path()
        >>> from src.config import APP_CONFIG  # Now works!
    """
    # Get the directory where THIS file is located
    current_file = Path(__file__).resolve()
    src_dir = current_file.parent  # src/
    project_root = src_dir.parent  # project_root/
    
    # Convert to string
    project_root_str = str(project_root)
    
    # Add to sys.path if not already there
    if project_root_str not in sys.path:
        # Insert at position 1 (after current directory) for priority
        sys.path.insert(1, project_root_str)
    
    return project_root_str


def get_project_root() -> str:
    """Get the project root directory without modifying sys.path."""
    return str(Path(__file__).resolve().parent.parent)


def get_src_dir() -> str:
    """Get the src/ directory path."""
    return str(Path(__file__).resolve().parent)


def bootstrap() -> str:
    """
    Bootstrap function for entry-point scripts.
    
    Call this at the VERY TOP of your main scripts (before any src imports):
    
        import os, sys
        from src.path_helper import bootstrap
        bootstrap()  # Auto-detects and configures paths
        
    This is a convenience wrapper around setup_path().
    """
    return setup_path()
