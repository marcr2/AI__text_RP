"""
Configuration and logging setup for the debate simulator.
"""
import os
import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default log level
LOG_LEVEL = logging.INFO

class Config:
    """Configuration class for the debate simulator."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.port = os.getenv("PORT")
        self.log_level = LOG_LEVEL
        
    @property
    def is_api_key_configured(self) -> bool:
        """Check if OpenAI API key is properly configured."""
        return bool(self.api_key and self.api_key != "your_openai_api_key_here")
    
    @property
    def is_railway_deployment(self) -> bool:
        """Check if running on Railway deployment."""
        return bool(self.port)

def setup_logging(log_level: Optional[int] = None) -> None:
    """
    Set up logging configuration with file and console handlers.
    
    Args:
        log_level: Logging level to use (defaults to LOG_LEVEL)
    """
    if log_level is None:
        log_level = LOG_LEVEL
        
    # Rotating file handler: 10MB per file, 10 backups
    file_handler = RotatingFileHandler(
        "debate.log", maxBytes=10 * 1024 * 1024, backupCount=10
    )
    file_handler.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Clear existing handlers and set up new ones
    logging.getLogger().handlers = []
    logging.getLogger().addHandler(file_handler)
    logging.getLogger().addHandler(console_handler)
    logging.getLogger().setLevel(log_level)

# Global config instance
config = Config()