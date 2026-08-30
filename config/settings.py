import os
from pathlib import Path
# ==========================================
# Base Directory & Path Resolution
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
VECTOR_DB_DIR = BASE_DIR / "vector_store"
# ==========================================
# Runtime Directory Assurance
# ==========================================
def ensure_directories():
    """Ensures that local data and vector storage directories exist prior to database initialization."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# Enterprise Design & Theme Tokens
# ==========================================
THEME = {
    "primary": "#2563eb",         # Deep Executive Blue (Institutional Trust)
    "success": "#10b981",         # Emerald Green (Verified Data & Completed Milestones)
    "background": "#f8fafc",      # Soft Slate Background
    "card_bg": "#ffffff",         # Crisp White Card Background
    "text_dark": "#0f172a",       # Primary Heading Text Color
    "text_muted": "#64748b"       # Secondary Subtitle / Label Text Color
}

# ==========================================
# Database Connection URL
# ==========================================
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    f"sqlite:///{DATA_DIR}/pragyan_intelligence.db"
)
