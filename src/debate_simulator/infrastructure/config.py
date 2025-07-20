import os
from typing import Optional, Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class AppConfig:
    """Application configuration settings."""
    
    # API Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o"
    
    # Logging Configuration
    log_level: str = "INFO"
    log_file: str = "debate.log"
    enable_debug_logging: bool = False
    
    # Application Settings
    default_rounds: int = 5
    default_delay: float = 1.0
    max_participants: int = 10
    
    # UI Configuration
    page_title: str = "AI Political Debate Simulator"
    page_icon: str = "🤖"
    layout: str = "wide"
    
    # Feature Flags
    enable_competitive_mode: bool = True
    enable_mock_ai: bool = False
    enable_file_logging: bool = True
    enable_console_logging: bool = True
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.openai_api_key and not self.openai_api_key.startswith("sk-"):
            raise ValueError("Invalid OpenAI API key format")
        
        if self.default_rounds < 1 or self.default_rounds > 50:
            raise ValueError("Default rounds must be between 1 and 50")
        
        if self.max_participants < 2 or self.max_participants > 20:
            raise ValueError("Max participants must be between 2 and 20")
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        """Create configuration from environment variables."""
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_file=os.getenv("LOG_FILE", "debate.log"),
            enable_debug_logging=os.getenv("ENABLE_DEBUG_LOGGING", "false").lower() == "true",
            default_rounds=int(os.getenv("DEFAULT_ROUNDS", "5")),
            default_delay=float(os.getenv("DEFAULT_DELAY", "1.0")),
            max_participants=int(os.getenv("MAX_PARTICIPANTS", "10")),
            page_title=os.getenv("PAGE_TITLE", "AI Political Debate Simulator"),
            page_icon=os.getenv("PAGE_ICON", "🤖"),
            layout=os.getenv("LAYOUT", "wide"),
            enable_competitive_mode=os.getenv("ENABLE_COMPETITIVE_MODE", "true").lower() == "true",
            enable_mock_ai=os.getenv("ENABLE_MOCK_AI", "false").lower() == "true",
            enable_file_logging=os.getenv("ENABLE_FILE_LOGGING", "true").lower() == "true",
            enable_console_logging=os.getenv("ENABLE_CONSOLE_LOGGING", "true").lower() == "true"
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "openai_api_key": "***" if self.openai_api_key else None,  # Hide sensitive data
            "openai_model": self.openai_model,
            "log_level": self.log_level,
            "log_file": self.log_file,
            "enable_debug_logging": self.enable_debug_logging,
            "default_rounds": self.default_rounds,
            "default_delay": self.default_delay,
            "max_participants": self.max_participants,
            "page_title": self.page_title,
            "page_icon": self.page_icon,
            "layout": self.layout,
            "enable_competitive_mode": self.enable_competitive_mode,
            "enable_mock_ai": self.enable_mock_ai,
            "enable_file_logging": self.enable_file_logging,
            "enable_console_logging": self.enable_console_logging
        }
    
    def validate_api_key(self) -> bool:
        """Validate the OpenAI API key."""
        if not self.openai_api_key:
            return False
        
        # Basic validation
        if not self.openai_api_key.startswith("sk-"):
            return False
        
        if len(self.openai_api_key) < 20:
            return False
        
        return True
    
    def is_development_mode(self) -> bool:
        """Check if running in development mode."""
        return os.getenv("ENVIRONMENT", "production").lower() in ["development", "dev", "debug"]
    
    def is_production_mode(self) -> bool:
        """Check if running in production mode."""
        return not self.is_development_mode()


class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config: Optional[AppConfig] = None, load_dotenv_file: bool = True):
        """Initialize configuration manager."""
        if load_dotenv_file:
            load_dotenv()
        
        self._config = config or AppConfig.from_env()
    
    @property
    def config(self) -> AppConfig:
        """Get the current configuration."""
        return self._config
    
    def reload_config(self) -> None:
        """Reload configuration from environment."""
        load_dotenv()
        self._config = AppConfig.from_env()
    
    def update_config(self, **kwargs) -> None:
        """Update specific configuration values."""
        for key, value in kwargs.items():
            if hasattr(self._config, key):
                setattr(self._config, key, value)
            else:
                raise ValueError(f"Unknown configuration key: {key}")
    
    def get_streamlit_config(self) -> Dict[str, Any]:
        """Get configuration for Streamlit page setup."""
        return {
            "page_title": self._config.page_title,
            "page_icon": self._config.page_icon,
            "layout": self._config.layout,
            "initial_sidebar_state": "expanded"
        }
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get configuration for logging setup."""
        return {
            "log_level": self._config.log_level,
            "log_file": self._config.log_file,
            "enable_file": self._config.enable_file_logging,
            "enable_console": self._config.enable_console_logging
        }
    
    def get_ai_config(self) -> Dict[str, Any]:
        """Get configuration for AI client."""
        return {
            "api_key": self._config.openai_api_key,
            "model": self._config.openai_model,
            "use_mock": self._config.enable_mock_ai
        }
    
    def check_required_config(self) -> list[str]:
        """Check for missing required configuration."""
        missing = []
        
        if not self._config.openai_api_key and not self._config.enable_mock_ai:
            missing.append("OPENAI_API_KEY")
        
        return missing
    
    def is_properly_configured(self) -> bool:
        """Check if the application is properly configured."""
        return len(self.check_required_config()) == 0


# Global configuration manager instance
_global_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """Get the global configuration manager."""
    global _global_config_manager
    
    if _global_config_manager is None:
        _global_config_manager = ConfigManager()
    
    return _global_config_manager


def get_config() -> AppConfig:
    """Get the current application configuration."""
    return get_config_manager().config


def set_config_manager(config_manager: ConfigManager) -> None:
    """Set a custom configuration manager."""
    global _global_config_manager
    _global_config_manager = config_manager


def reload_config() -> None:
    """Reload configuration from environment."""
    get_config_manager().reload_config()


# Environment variable helpers
def get_env_bool(key: str, default: bool = False) -> bool:
    """Get a boolean value from environment variables."""
    value = os.getenv(key, str(default)).lower()
    return value in ["true", "1", "yes", "on"]


def get_env_int(key: str, default: int = 0) -> int:
    """Get an integer value from environment variables."""
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        return default


def get_env_float(key: str, default: float = 0.0) -> float:
    """Get a float value from environment variables."""
    try:
        return float(os.getenv(key, str(default)))
    except ValueError:
        return default


# Railway deployment helpers
def is_railway_deployment() -> bool:
    """Check if running on Railway."""
    return "RAILWAY_ENVIRONMENT" in os.environ


def get_railway_port() -> Optional[int]:
    """Get the port for Railway deployment."""
    if "PORT" in os.environ:
        try:
            return int(os.environ["PORT"])
        except ValueError:
            pass
    return None


# Configuration validation
def validate_environment() -> Dict[str, Any]:
    """Validate the current environment configuration."""
    config = get_config()
    validation_results = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "info": []
    }
    
    # Check API key
    if not config.openai_api_key and not config.enable_mock_ai:
        validation_results["errors"].append("OpenAI API key is required when not using mock AI")
        validation_results["valid"] = False
    elif config.openai_api_key and not config.validate_api_key():
        validation_results["errors"].append("OpenAI API key format is invalid")
        validation_results["valid"] = False
    
    # Check deployment environment
    if is_railway_deployment():
        validation_results["info"].append("Running on Railway deployment")
        port = get_railway_port()
        if port:
            validation_results["info"].append(f"Using Railway port: {port}")
    
    # Check development mode
    if config.is_development_mode():
        validation_results["warnings"].append("Running in development mode")
    
    return validation_results


# Example usage and testing
def print_config_summary() -> None:
    """Print a summary of the current configuration."""
    config = get_config()
    validation = validate_environment()
    
    print("=== Debate Simulator Configuration ===")
    print(f"Environment: {'Development' if config.is_development_mode() else 'Production'}")
    print(f"API Key Configured: {'Yes' if config.openai_api_key else 'No'}")
    print(f"Mock AI Enabled: {config.enable_mock_ai}")
    print(f"Competitive Mode: {config.enable_competitive_mode}")
    print(f"Default Rounds: {config.default_rounds}")
    print(f"Log Level: {config.log_level}")
    
    if validation["errors"]:
        print("\nERRORS:")
        for error in validation["errors"]:
            print(f"  - {error}")
    
    if validation["warnings"]:
        print("\nWARNINGS:")
        for warning in validation["warnings"]:
            print(f"  - {warning}")
    
    if validation["info"]:
        print("\nINFO:")
        for info in validation["info"]:
            print(f"  - {info}")
    
    print(f"\nConfiguration Valid: {validation['valid']}")
    print("=" * 40)