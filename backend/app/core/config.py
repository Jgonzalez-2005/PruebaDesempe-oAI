import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

class Settings(BaseModel):
    PROJECT_NAME: str = "LinguaColombia AI Customer Support"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Document directories
    BASE_DIR: Path = ROOT_DIR
    DOCS_DIR: Path = ROOT_DIR / "data" / "documents"
    
    # LLM Settings (OpenAI & Google Gemini)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    # Selected Provider: "openai", "gemini", or "auto"
    DEFAULT_PROVIDER: str = os.getenv("DEFAULT_PROVIDER", "auto")
    
    # RAG Settings
    CHUNK_SIZE: int = 400
    CHUNK_OVERLAP: int = 80
    TOP_K_CHUNKS: int = 4
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.08"))
    
    # Cache Settings
    CACHE_ENABLED: bool = True
    CACHE_MAX_ITEMS: int = 500
    CACHE_TTL_SECONDS: int = 3600

settings = Settings()
