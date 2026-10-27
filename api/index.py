import sys
import os
from pathlib import Path

# Ensure project root is in sys.path so 'backend.app.main' imports cleanly
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

backend_dir = root_dir / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Ensure writable directories in /tmp for Vercel Serverless Functions
tmp_base = Path("/tmp") / "crimevision"
try:
    tmp_base.mkdir(parents=True, exist_ok=True)
    (tmp_base / "uploads").mkdir(parents=True, exist_ok=True)
    (tmp_base / "reports").mkdir(parents=True, exist_ok=True)
except Exception:
    pass

# Import single source of truth FastAPI app
from backend.app.main import app, application, handler
