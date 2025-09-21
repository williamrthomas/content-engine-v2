"""Configuration management for Content Engine V2"""

import os
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Database Configuration
    database_url: str = Field(
        default="postgresql://user:password@localhost:5432/content_engine",
        env="DATABASE_URL",
        description="PostgreSQL connection URL"
    )
    
    # LLM Configuration
    openrouter_api_key: str = Field(
        default="",
        env="OPENROUTER_API_KEY", 
        description="OpenRouter API key for LLM services"
    )
    default_model: str = Field(
        default="openai/gpt-3.5-turbo",
        env="DEFAULT_MODEL",
        description="Default LLM model for operations"
    )
    fallback_model: str = Field(
        default="anthropic/claude-3-haiku",
        env="FALLBACK_MODEL", 
        description="Fallback LLM model if default fails"
    )
    
    # Storage Configuration
    assets_dir: Path = Field(
        default=Path("./assets"),
        env="ASSETS_DIR",
        description="Directory for generated assets"
    )
    templates_dir: Path = Field(
        default=Path("./src/templates/markdown"),
        env="TEMPLATES_DIR",
        description="Directory for template files"
    )
    
    # Logging Configuration
    log_level: str = Field(
        default="INFO",
        env="LOG_LEVEL",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )
    log_file: Optional[str] = Field(
        default="content_engine.log",
        env="LOG_FILE",
        description="Log file path (None for console only)"
    )
    
    # CLI Configuration
    cli_theme: str = Field(
        default="dark",
        env="CLI_THEME",
        description="CLI theme (dark, light)"
    )
    progress_bars: bool = Field(
        default=True,
        env="PROGRESS_BARS",
        description="Enable progress bars in CLI"
    )
    
    # Development
    debug: bool = Field(
        default=False,
        env="DEBUG",
        description="Enable debug mode"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def load_settings() -> Settings:
    """Load settings from environment and .env file"""
    # Load .env file if it exists
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(env_path)
    
    return Settings()


# Global settings instance
settings = load_settings()


def get_database_url() -> str:
    """Get the database URL with validation"""
    url = settings.database_url
    if not url or url == "postgresql://user:password@localhost:5432/content_engine":
        raise ValueError(
            "DATABASE_URL not configured. Please set it in your .env file or environment variables."
        )
    return url


def get_openrouter_api_key() -> str:
    """Get OpenRouter API key with validation"""
    key = settings.openrouter_api_key
    if not key or key.startswith("sk-or-your-api-key"):
        raise ValueError(
            "OPENROUTER_API_KEY not configured. Please set it in your .env file or environment variables."
        )
    return key


def ensure_directories() -> None:
    """Ensure required directories exist"""
    settings.assets_dir.mkdir(parents=True, exist_ok=True)
    settings.templates_dir.mkdir(parents=True, exist_ok=True)
    
    # Create jobs directory structure
    jobs_dir = settings.assets_dir / "jobs"
    jobs_dir.mkdir(exist_ok=True)
    
    # Create .gitkeep file
    gitkeep = jobs_dir / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.touch()
