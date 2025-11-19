"""Product reviews data parser"""

import pandas as pd
from .base_parser import BaseParser
from src.utils import logger

class ReviewParser(BaseParser):
    """Parse product reviews data"""
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
    
    def parse(self) -> pd.DataFrame:
        """Parse review data"""
        
        # Load data
        self.load_data()
        
        if self.data.empty:
            return pd.DataFrame()
        
        # Standardize column names
        col_mapping = {}
        columns_lower = {col.lower(): col for col in self.data.columns}
        
        # Map common review column names
        for standard_name, possible_names in [
            ('review_id', ['review_id', 'id', 'review_number']),
            ('product_id', ['product_id', 'asin', 'sku', 'product_sku']),
            ('product_name', ['product_name', 'title', 'product_title']),
            ('rating', ['rating', 'stars', 'rating_score']),
            ('review_text', ['review_text', 'text', 'review', 'comment']),
            ('review_date', ['review_date', 'date', 'posted_date']),
            ('verified_purchase', ['verified_purchase', 'verified', 'is_verified'])
        ]:
            for possible_name in possible_names:
                if possible_name in columns_lower:
                    col_mapping[standard_name] = columns_lower[possible_name]
                    break
        
        # Create new dataframe
        df = pd.DataFrame()
        for standard_name, original_name in col_mapping.items():
            if original_name in self.data.columns:
                df[standard_name] = self.data[original_name]
        
        # Add source
        df['source'] = 'Reviews'
        
        # Identify negative reviews (potential quality issues)
        if 'rating' in df.columns:
            df['is_negative_review'] = df['rating'] <= 2
        else:
            df['is_negative_review'] = False
        
        # Identify issue mentions
        df['has_issue_mention'] = df['review_text'].fillna('').str.contains(
            r'broken|damaged|defect|quality|issue|problem|stop work|failed|poor|cheap|quality|cracking|fading',
            case=False,
            regex=True
        )
        
        self.data = df
        logger.info(f"Parsed {len(self.data)} reviews, {df['is_negative_review'].sum()} negative, {df['has_issue_mention'].sum()} with issues")
        
        return self.data
