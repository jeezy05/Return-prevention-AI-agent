"""Configuration management for the Return Prevention Agent"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent

# Load config from YAML
CONFIG_PATH = PROJECT_ROOT / "config.yaml"

def load_config():
    """Load configuration from YAML file"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r') as f:
            return yaml.safe_load(f)
    else:
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")

# Load configuration
CONFIG = load_config()

# API Configuration
# Ollama is now used (free, self-hosted) - no API key needed
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
TEMPLATES_DIR = DATA_DIR / "templates"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Create directories if they don't exist
for dir_path in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, TEMPLATES_DIR, REPORTS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Data sources
DATA_SOURCES = CONFIG["data_sources"]

# Processing settings
PROCESSING_CONFIG = CONFIG["processing"]

# AI settings
AI_CONFIG = CONFIG["ai_analysis"]

# Risk prediction settings
RISK_CONFIG = CONFIG["risk_prediction"]

# Reporting settings
REPORTING_CONFIG = CONFIG["reporting"]

# Logging settings
LOGGING_CONFIG = CONFIG["logging"]
