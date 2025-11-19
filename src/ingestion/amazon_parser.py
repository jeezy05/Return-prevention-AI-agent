"""Amazon returns data parser"""

import pandas as pd
from .base_parser import BaseParser
from src.utils import logger

class AmazonParser(BaseParser):
    """Parse Amazon returns data"""
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
    
    def parse(self) -> pd.DataFrame:
        """Parse Amazon returns data"""
        
        # Load data
        self.load_data()
        
        if self.data.empty:
            return pd.DataFrame()
        
        # Standardize column names (case-insensitive search)
        col_mapping = {}
        columns_lower = {col.lower(): col for col in self.data.columns}
        
        # Map common Amazon column names
        for standard_name, possible_names in [
            ('product_id', ['asin', 'sku', 'product_id', 'product_sku']),
            ('product_name', ['title', 'product_name', 'product_title']),
            ('return_reason', ['return_reason', 'reason', 'return_reason_code']),
            ('return_date', ['return_date', 'date_returned', 'return_date_time']),
            ('refund_amount', ['refund_amount', 'price', 'refund_amount_usd']),
            ('customer_feedback', ['customer_feedback', 'notes', 'feedback']),
            ('order_id', ['order_id', 'amazon_order_id'])
        ]:
            for possible_name in possible_names:
                if possible_name in columns_lower:
                    col_mapping[standard_name] = columns_lower[possible_name]
                    break
        
        # Create new dataframe with standardized columns
        df = pd.DataFrame()
        for standard_name, original_name in col_mapping.items():
            if original_name in self.data.columns:
                df[standard_name] = self.data[original_name]
        
        # Add source
        df['source'] = 'Amazon'
        
        # Ensure required columns exist
        if 'return_reason' not in df.columns:
            logger.warning("return_reason column not found in Amazon data")
        
        self.data = df
        logger.info(f"Parsed {len(self.data)} Amazon returns")
        
        return self.data
