"""
Configuration and constants for the application
"""
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
UPLOADS_DIR = BASE_DIR / "uploads"
MD_DIR = UPLOADS_DIR / "md"
DOCX_DIR = UPLOADS_DIR / "docx"

# Ensure directories exist
MD_DIR.mkdir(parents=True, exist_ok=True)
DOCX_DIR.mkdir(parents=True, exist_ok=True)

# CORS settings
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080"
]
