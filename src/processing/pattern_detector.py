import pandas as pd
from collections import Counter
from src.utils import logger, extract_keywords

class PatternDetector:
    def __init__(self):
        pass
    
    def detect_product_issues(self, df: pd.DataFrame, product_col: str, reason_col: str) -> dict:
        patterns = {}
        for product in df[product_col].unique():
            product_data = df[df[product_col] == product]
            reasons = product_data[reason_col].fillna('').tolist()
            reason_counts = Counter(reasons)
            top_reasons = reason_counts.most_common(5)
            patterns[product] = {
                'total_returns': len(product_data),
                'top_reasons': top_reasons,
                'return_rate': round((len(product_data) / len(df)) * 100, 2)
            }
        logger.info(f"Detected patterns for {len(patterns)} products")
        return patterns
    
    def detect_temporal_patterns(self, df: pd.DataFrame, date_col: str, reason_col: str = None) -> dict:
        patterns = {'by_week': {}, 'by_month': {}}
        if date_col not in df.columns:
            logger.warning(f"Date column {date_col} not found")
            return patterns
        
        df_copy = df.copy()
        df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
        df_copy['week'] = df_copy[date_col].dt.isocalendar().week
        weekly_counts = df_copy.groupby('week').size()
        patterns['by_week'] = weekly_counts.to_dict()
        df_copy['month'] = df_copy[date_col].dt.to_period('M')
        monthly_counts = df_copy.groupby('month').size()
        patterns['by_month'] = {str(k): v for k, v in monthly_counts.to_dict().items()}
        logger.info("Detected temporal patterns")
        return patterns
    
    def detect_keyword_patterns(self, df: pd.DataFrame, text_col: str, top_n: int = 10) -> dict:
        if text_col not in df.columns:
            logger.warning(f"Text column {text_col} not found")
            return {}
        
        all_keywords = []
        for text in df[text_col].fillna(''):
            keywords = extract_keywords(str(text))
            all_keywords.extend(keywords)
        
        keyword_counts = Counter(all_keywords)
        top_keywords = keyword_counts.most_common(top_n)
        
        patterns = {
            'top_keywords': top_keywords,
            'unique_keywords': len(keyword_counts),
            'total_keywords': len(all_keywords)
        }
        
        logger.info(f"Detected {len(keyword_counts)} unique keywords")
        return patterns
    
    def detect_severity_patterns(self, df: pd.DataFrame, severity_col: str) -> dict:
        if severity_col not in df.columns:
            logger.warning(f"Severity column {severity_col} not found")
            return {}
        
        patterns = {}
        severity_counts = df[severity_col].value_counts()
        
        for severity, count in severity_counts.items():
            patterns[severity] = {
                'count': count,
                'percentage': round((count / len(df)) * 100, 2)
            }
        
        logger.info(f"Detected severity patterns: {patterns}")
        return patterns
