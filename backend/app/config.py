import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

class Settings:
    PROJECT_NAME: str = "CrimeVision AI Forensic Engine"
    API_V1_PREFIX: str = "/api/v1"
    
    # Base paths
    BACKEND_DIR: Path = Path(__file__).resolve().parent.parent
    PROJECT_ROOT: Path = BACKEND_DIR.parent
    
    # Data directories (compatible with Vercel serverless /tmp write restrictions)
    is_vercel: bool = bool(os.getenv("VERCEL"))
    if is_vercel:
        _tmp_base = Path("/tmp") / "crimevision"
        _tmp_base.mkdir(parents=True, exist_ok=True)
        DATABASE_PATH: Path = _tmp_base / "forensic_data.db"
        _bundled_db = BACKEND_DIR / "forensic_data.db"
        if _bundled_db.exists() and not DATABASE_PATH.exists():
            import shutil
            try:
                shutil.copyfile(_bundled_db, DATABASE_PATH)
            except Exception:
                pass
        UPLOAD_DIR: Path = _tmp_base / "uploads"
        REPORT_DIR: Path = _tmp_base / "reports"
    else:
        DATABASE_PATH: Path = BACKEND_DIR / "forensic_data.db"
        UPLOAD_DIR: Path = BACKEND_DIR / "uploads"
        REPORT_DIR: Path = BACKEND_DIR / "reports"
    SAMPLE_DATA_DIR: Path = PROJECT_ROOT / "sample_data"
    
    # Gemini AI Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()
    
    # Mock / Sandbox fallback mode
    FORCE_MOCK: bool = os.getenv("FORCE_MOCK", "false").lower() in ("true", "1", "yes")

    @property
    def is_gemini_active(self) -> bool:
        return bool(self.GEMINI_API_KEY) and not self.FORCE_MOCK and not self.GEMINI_API_KEY.startswith("mock")

settings = Settings()

# Ensure required directories exist
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.REPORT_DIR.mkdir(parents=True, exist_ok=True)
settings.SAMPLE_DATA_DIR.mkdir(parents=True, exist_ok=True)
