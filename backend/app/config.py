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
    @property
    def is_vercel(self) -> bool:
        return bool(os.getenv("VERCEL")) or os.getenv("AWS_LAMBDA_FUNCTION_NAME") is not None

    @property
    def DATABASE_PATH(self) -> Path:
        if self.is_vercel:
            return Path("/tmp") / "crimevision" / "forensic_data.db"
        DATABASE_PATH: Path = self.BACKEND_DIR / "forensic_data.db"
        return DATABASE_PATH

    @property
    def UPLOAD_DIR(self) -> Path:
        if self.is_vercel:
            return Path("/tmp") / "crimevision" / "uploads"
        UPLOAD_DIR: Path = self.BACKEND_DIR / "uploads"
        return UPLOAD_DIR

    @property
    def REPORT_DIR(self) -> Path:
        if self.is_vercel:
            return Path("/tmp") / "crimevision" / "reports"
        REPORT_DIR: Path = self.BACKEND_DIR / "reports"
        return REPORT_DIR

    def ensure_storage_directories(self):
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        self.REPORT_DIR.mkdir(parents=True, exist_ok=True)
        if self.is_vercel:
            target_db = self.DATABASE_PATH
            target_db.parent.mkdir(parents=True, exist_ok=True)
            bundled_db = self.BACKEND_DIR / "forensic_data.db"
            if bundled_db.exists() and not target_db.exists():
                import shutil
                try:
                    shutil.copyfile(bundled_db, target_db)
                except Exception:
                    pass

    SAMPLE_DATA_DIR: Path = PROJECT_ROOT / "sample_data"
    
    # Gemini AI Configuration
    @property
    def GEMINI_API_KEY(self) -> str:
        return os.getenv("GEMINI_API_KEY", "").strip()

    @property
    def GEMINI_MODEL(self) -> str:
        return os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()

    @property
    def FORCE_MOCK(self) -> bool:
        return os.getenv("FORCE_MOCK", "false").lower() in ("true", "1", "yes")
    
    @property
    def is_gemini_active(self) -> bool:
        key = self.GEMINI_API_KEY
        return bool(key) and not self.FORCE_MOCK and not key.startswith("mock")

settings = Settings()

settings.ensure_storage_directories()
settings.SAMPLE_DATA_DIR.mkdir(parents=True, exist_ok=True)
