import pandas as pd
from src.utils import categorize_return_reason, logger

class Classifier:
    def __init__(self):
        self.categories = {
            "Quality Issue": ["defective", "broken", "damaged", "malfunction", "faulty", "not work", "stopped work", "failed", "cracking", "cracked"],
            "Sizing Issue": ["too small", "too large", "size", "fit", "length", "width", "height", "short", "long"],
            "Design Issue": ["color", "material", "design", "picture", "description", "not as described", "not as expected"],
            "Packaging Issue": ["packaging", "damaged packaging", "water damage", "poor packaging", "damaged", "wet"],
            "Shipping Damage": ["shipping damage", "damaged in transit", "arrived damaged"],
            "Durability Issue": ["wear", "faded", "deteriorating", "break", "quit", "stop", "crack"]
        }
    
    def classify_reason(self, reason: str) -> str:
        return categorize_return_reason(reason, self.categories)
    
    def classify_dataframe(self, df: pd.DataFrame, reason_column: str) -> pd.DataFrame:
        df_copy = df.copy()
        
        if reason_column not in df_copy.columns:
            logger.warning(f"Column {reason_column} not found in dataframe")
            return df_copy
        
        df_copy['return_category'] = df_copy[reason_column].fillna('').apply(self.classify_reason)
        category_counts = df_copy['return_category'].value_counts()
        logger.info(f"Classified returns: {dict(category_counts)}")
        return df_copy
    
    def get_category_distribution(self, df: pd.DataFrame) -> dict:
        if 'return_category' not in df.columns:
            logger.warning("return_category column not found")
            return {}
        
        total = len(df)
        distribution = {}
        
        for category in df['return_category'].unique():
            count = (df['return_category'] == category).sum()
            distribution[category] = {
                'count': count,
                'percentage': round((count / total) * 100, 2)
            }
        
        return distribution
