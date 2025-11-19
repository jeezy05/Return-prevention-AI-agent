"""Logging configuration for the Return Prevention Agent"""

import logging
import sys
from pathlib import Path
from src.config import LOGGING_CONFIG, PROJECT_ROOT

# Create logs directory
logs_dir = PROJECT_ROOT / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)

def setup_logger(name):
    """Setup logger with file and console handlers"""
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOGGING_CONFIG["level"]))
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler - use UTF-8 encoding for emoji support on Windows
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    # Force UTF-8 for console output on Windows
    if sys.stdout.encoding.lower() != 'utf-8':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    logger.addHandler(console_handler)
    
    # File handler
    log_file = logs_dir / Path(LOGGING_CONFIG["file"]).name
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

# Create module logger
logger = setup_logger(__name__)
