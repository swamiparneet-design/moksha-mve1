"""
Configuration Manager for MOKSHA MVE-1
Handles all environment variables and settings
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Main configuration class"""
    
    # Base directories
    BASE_DIR = Path(__file__).parent
    STORAGE_PATH = Path(os.getenv("STORAGE_PATH", "./storage"))
    CACHE_PATH = Path(os.getenv("CACHE_PATH", "./cache"))
    TEMP_PATH = Path(os.getenv("TEMP_PATH", "./temp"))
    OUTPUT_PATH = Path(os.getenv("OUTPUT_PATH", "./outputs"))
    
    # Create directories if they don't exist
    for path in [STORAGE_PATH, CACHE_PATH, TEMP_PATH, OUTPUT_PATH]:
        path.mkdir(parents=True, exist_ok=True)
    
    # Cache subdirectories
    (CACHE_PATH / "scripts").mkdir(exist_ok=True)
    (CACHE_PATH / "voices").mkdir(exist_ok=True)
    (CACHE_PATH / "broll").mkdir(exist_ok=True)
    (CACHE_PATH / "avatars").mkdir(exist_ok=True)
    
    # API Keys
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-reasoner")
    DEEPSEEK_ANTHROPIC_BASE_URL = os.getenv("DEEPSEEK_ANTHROPIC_BASE_URL", "https://api.deepseek.com/anthropic")
    
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
    
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "deepseek-chat")
    ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.deepseek.com/anthropic")
    
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
    FLUX_API_KEY = os.getenv("FLUX_API_KEY", "")
    
    # GPU Configuration
    RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY", "")
    RUNPOD_GPU_ID = os.getenv("RUNPOD_GPU_ID", "rtx4090")
    RUNPOD_ENDPOINT_ID = os.getenv("RUNPOD_ENDPOINT_ID", "")
    
    # Redis Configuration
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    
    # FFmpeg Configuration
    FFMPEG_PATH = os.getenv("FFMPEG_PATH", "ffmpeg")
    FFPROBE_PATH = os.getenv("FFPROBE_PATH", "ffprobe")
    
    # Video Generation Settings
    DEFAULT_VIDEO_DURATION = int(os.getenv("DEFAULT_VIDEO_DURATION", 5))
    MAX_PARALLEL_GENERATION = int(os.getenv("MAX_PARALLEL_GENERATION", 4))
    GPU_COST_PER_HOUR_INR = float(os.getenv("GPU_COST_PER_HOUR_INR", 17.0))
    
    # Language Settings
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "hindi")
    SUPPORTED_LANGUAGES = os.getenv("SUPPORTED_LANGUAGES", "hindi,haryanvi,bhojpuri").split(",")
    
    # Website & Affiliate Settings
    BLOG_URL = os.getenv("BLOG_URL", "")
    AFFILIATE_ENABLED = os.getenv("AFFILIATE_ENABLED", "true").lower() == "true"
    ADD_AFFILIATE_LONG_VIDEOS_ONLY = os.getenv("ADD_AFFILIATE_LONG_VIDEOS_ONLY", "true").lower() == "true"
    
    # Server Settings
    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))
    DEBUG_MODE = os.getenv("DEBUG_MODE", "true").lower() == "true"
    
    @classmethod
    def get_cache_path(cls, category: str, filename: str) -> Path:
        """Get cache file path for a specific category"""
        cache_dir = cls.CACHE_PATH / category
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir / filename
    
    @classmethod
    def validate_api_keys(cls) -> dict:
        """Validate which API keys are configured"""
        return {
            "deepseek": bool(cls.DEEPSEEK_API_KEY),
            "groq": bool(cls.GROQ_API_KEY),
            "anthropic": bool(cls.ANTHROPIC_API_KEY),
            "pexels": bool(cls.PEXELS_API_KEY),
            "youtube": bool(cls.YOUTUBE_API_KEY),
            "flux": bool(cls.FLUX_API_KEY),
            "runpod": bool(cls.RUNPOD_API_KEY),
        }
