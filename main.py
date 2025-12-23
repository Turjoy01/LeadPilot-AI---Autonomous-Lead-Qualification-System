"""
Main entry point for LeadPilot AI
This file allows running: uvicorn main:app --reload

Make sure to run from the project root directory:
    uvicorn main:app --reload
"""
import sys
import os
from pathlib import Path

# Get the directory where this file is located (project root)
project_root = Path(__file__).parent.absolute()

# Add project root to Python path if not already there
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Now import the app
from backend.main import app

__all__ = ["app"]

