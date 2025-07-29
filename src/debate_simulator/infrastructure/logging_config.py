import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional


class LoggingConfig:
    """Centralized logging configuration for the debate simulator."""
    
    DEFAULT_LOG_LEVEL = logging.INFO
    DEFAULT_LOG_FORMAT = "%(asctime)s %(levelname)s: %(message)s"
    DEFAULT_LOG_FILE = "debate.log"
    DEFAULT_MAX_BYTES = 10 * 1024 * 1024  # 10MB
    DEFAULT_BACKUP_COUNT = 10
    
    def __init__(
        self,
        log_level: int = None,
        log_format: str = None,
        log_file: str = None,
        max_bytes: int = None,
        backup_count: int = None,
        enable_console: bool = True,
        enable_file: bool = True
    ):
        """Initialize logging configuration."""
        self.log_level = log_level or self.DEFAULT_LOG_LEVEL
        self.log_format = log_format or self.DEFAULT_LOG_FORMAT
        self.log_file = log_file or self.DEFAULT_LOG_FILE
        self.max_bytes = max_bytes or self.DEFAULT_MAX_BYTES
        self.backup_count = backup_count or self.DEFAULT_BACKUP_COUNT
        self.enable_console = enable_console
        self.enable_file = enable_file
        
        self._configured = False
    
    def setup_logging(self) -> None:
        """Set up logging with the configured parameters."""
        if self._configured:
            return
        
        # Clear existing handlers
        logging.getLogger().handlers = []
        
        # Set root logger level
        logging.getLogger().setLevel(self.log_level)
        
        # Create formatter
        formatter = logging.Formatter(self.log_format)
        
        # File handler
        if self.enable_file:
            file_handler = RotatingFileHandler(
                self.log_file, 
                maxBytes=self.max_bytes, 
                backupCount=self.backup_count
            )
            file_handler.setLevel(self.log_level)
            file_handler.setFormatter(formatter)
            logging.getLogger().addHandler(file_handler)
        
        # Console handler
        if self.enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.log_level)
            console_handler.setFormatter(formatter)
            logging.getLogger().addHandler(console_handler)
        
        self._configured = True
        logging.info("Logging configuration initialized")
    
    def set_level(self, level: int) -> None:
        """Change the logging level dynamically."""
        self.log_level = level
        logging.getLogger().setLevel(level)
        
        # Update all handlers
        for handler in logging.getLogger().handlers:
            handler.setLevel(level)
        
        logging.info(f"Logging level changed to {logging.getLevelName(level)}")
    
    def enable_debug_logging(self) -> None:
        """Enable debug level logging."""
        self.set_level(logging.DEBUG)
    
    def disable_debug_logging(self) -> None:
        """Disable debug level logging (return to default)."""
        self.set_level(self.DEFAULT_LOG_LEVEL)
    
    def get_current_level(self) -> str:
        """Get the current logging level name."""
        return logging.getLevelName(logging.getLogger().level)


# Global logging configuration instance
_global_config: Optional[LoggingConfig] = None


def setup_default_logging() -> LoggingConfig:
    """Set up default logging configuration."""
    global _global_config
    
    if _global_config is None:
        _global_config = LoggingConfig()
        _global_config.setup_logging()
    
    return _global_config


def get_logging_config() -> Optional[LoggingConfig]:
    """Get the current global logging configuration."""
    return _global_config


def set_logging_config(config: LoggingConfig) -> None:
    """Set a custom global logging configuration."""
    global _global_config
    _global_config = config
    config.setup_logging()


def enable_debug_logging() -> None:
    """Enable debug logging globally."""
    config = get_logging_config()
    if config:
        config.enable_debug_logging()


def disable_debug_logging() -> None:
    """Disable debug logging globally."""
    config = get_logging_config()
    if config:
        config.disable_debug_logging()


def get_current_log_level() -> str:
    """Get current log level name."""
    config = get_logging_config()
    if config:
        return config.get_current_level()
    return "Not configured"


# Convenience function for creating specialized loggers
def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name."""
    # Ensure default logging is set up
    if _global_config is None:
        setup_default_logging()
    
    return logging.getLogger(name)


# Specialized loggers for different components
def get_ai_logger() -> logging.Logger:
    """Get logger for AI client operations."""
    return get_logger("debate_simulator.ai")


def get_debate_logger() -> logging.Logger:
    """Get logger for debate operations."""
    return get_logger("debate_simulator.debate")


def get_character_logger() -> logging.Logger:
    """Get logger for character operations."""
    return get_logger("debate_simulator.character")


def get_ui_logger() -> logging.Logger:
    """Get logger for UI operations."""
    return get_logger("debate_simulator.ui")


# Context manager for temporary log level changes
class TemporaryLogLevel:
    """Context manager to temporarily change log level."""
    
    def __init__(self, level: int):
        """Initialize with the temporary level."""
        self.temp_level = level
        self.original_level = None
    
    def __enter__(self):
        """Enter the context and set temporary level."""
        config = get_logging_config()
        if config:
            self.original_level = logging.getLogger().level
            config.set_level(self.temp_level)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context and restore original level."""
        config = get_logging_config()
        if config and self.original_level is not None:
            config.set_level(self.original_level)


# Example usage functions
def log_debate_start(topic: str, participants: list) -> None:
    """Log the start of a debate."""
    logger = get_debate_logger()
    logger.info(f"Debate started. Topic: '{topic}', Participants: {participants}")


def log_debate_end(topic: str, rounds: int, participants: list) -> None:
    """Log the end of a debate."""
    logger = get_debate_logger()
    logger.info(f"Debate ended. Topic: '{topic}', Rounds: {rounds}, Participants: {participants}")


def log_ai_request(prompt: str, character: str = None) -> None:
    """Log an AI request."""
    logger = get_ai_logger()
    char_info = f" for {character}" if character else ""
    logger.debug(f"AI request sent{char_info}: {prompt[:100]}...")


def log_ai_response(response: str, character: str = None) -> None:
    """Log an AI response."""
    logger = get_ai_logger()
    char_info = f" from {character}" if character else ""
    logger.debug(f"AI response received{char_info}: {response}")


def log_character_creation(character_name: str, character_type: str) -> None:
    """Log character creation."""
    logger = get_character_logger()
    logger.info(f"Character created: {character_name} ({character_type})")


def log_ui_action(action: str, details: str = None) -> None:
    """Log UI actions."""
    logger = get_ui_logger()
    detail_info = f" - {details}" if details else ""
    logger.info(f"UI Action: {action}{detail_info}")