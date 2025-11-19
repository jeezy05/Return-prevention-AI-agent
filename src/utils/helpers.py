"""Helper utilities for the Return Prevention Agent"""

import re
from datetime import datetime
from typing import List, Dict, Any

def normalize_text(text: str) -> str:
    """Normalize text for processing"""
    if not isinstance(text, str):
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove special characters but keep alphanumeric and basic punctuation
    text = re.sub(r'[^a-z0-9\s\.\,\!\?\-]', '', text)
    
    return text

def extract_keywords(text: str, min_length: int = 2) -> List[str]:
    """Extract keywords from text"""
    words = text.split()
    # Filter short words and common stopwords
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'be', 'been', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where', 'why', 'how'}
    keywords = [w for w in words if len(w) >= min_length and w not in stopwords]
    return keywords

def categorize_return_reason(reason: str, custom_categories: Dict[str, List[str]] = None) -> str:
    """Categorize return reason into predefined categories"""
    
    reason_lower = reason.lower()
    
    # Default categories
    default_categories = {
        "Quality Issue": ["defective", "broken", "damaged", "malfunction", "faulty", "not work", "stopped work", "failed"],
        "Sizing Issue": ["too small", "too large", "size", "fit", "length", "width", "height"],
        "Design Issue": ["color", "material", "design", "picture", "description", "not as described"],
        "Packaging Issue": ["packaging", "damaged packaging", "water damage", "poor packaging", "packaging damaged"],
        "Other": []
    }
    
    # Use custom categories if provided
    categories = custom_categories or default_categories
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in reason_lower:
                return category
    
    return "Other"

def calculate_severity(reason: str, frequency: int = 1) -> str:
    """Calculate severity level based on reason and frequency"""
    
    high_severity_keywords = ["defective", "broken", "damaged", "malfunction", "failure", "not work", "crashed"]
    medium_severity_keywords = ["quality", "issue", "problem", "faded", "worn"]
    
    reason_lower = reason.lower()
    
    if any(kw in reason_lower for kw in high_severity_keywords):
        if frequency > 20:
            return "CRITICAL"
        return "HIGH"
    elif any(kw in reason_lower for kw in medium_severity_keywords):
        return "MEDIUM"
    
    return "LOW"

def format_date(date_str: str, input_format: str = "%Y-%m-%d") -> str:
    """Format date string"""
    try:
        date_obj = datetime.strptime(str(date_str), input_format)
        return date_obj.strftime("%B %d, %Y")
    except:
        return str(date_str)

def merge_dictionaries(*dicts: Dict) -> Dict:
    """Merge multiple dictionaries"""
    result = {}
    for d in dicts:
        result.update(d)
    return result

def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"${amount:,.2f}"

def calculate_percentage(part: float, total: float) -> float:
    """Calculate percentage"""
    if total == 0:
        return 0
    return round((part / total) * 100, 2)
