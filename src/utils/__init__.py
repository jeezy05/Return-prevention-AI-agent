"""Utilities module"""

from .logger import logger
from .helpers import (
    normalize_text,
    extract_keywords,
    categorize_return_reason,
    calculate_severity,
    format_date,
    merge_dictionaries,
    format_currency,
    calculate_percentage
)

__all__ = [
    'logger',
    'normalize_text',
    'extract_keywords',
    'categorize_return_reason',
    'calculate_severity',
    'format_date',
    'merge_dictionaries',
    'format_currency',
    'calculate_percentage'
]
