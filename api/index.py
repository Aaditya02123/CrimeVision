import sys
import os
from pathlib import Path

# Add backend directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
backend_dir = root_dir / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Ensure required writable directories exist in serverless /tmp
tmp_base = Path("/tmp") / "crimevision"
try:
    tmp_base.mkdir(parents=True, exist_ok=True)
    (tmp_base / "uploads").mkdir(parents=True, exist_ok=True)
    (tmp_base / "reports").mkdir(parents=True, exist_ok=True)
except Exception:
    pass

from app.main import app, application, handler
