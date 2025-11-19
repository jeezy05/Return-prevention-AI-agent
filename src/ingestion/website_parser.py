"""Website returns data parser"""

import pandas as pd
from .base_parser import BaseParser
from src.utils import logger

class WebsiteParser(BaseParser):
    """Parse website returns data"""
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
    
    def parse(self) -> pd.DataFrame:
        """Parse website returns data"""
        
        # Load data
        self.load_data()
        
        if self.data.empty:
            return pd.DataFrame()
        
        # Standardize column names
        col_mapping = {}
        columns_lower = {col.lower(): col for col in self.data.columns}
        
        # Map common website column names
        for standard_name, possible_names in [
            ('product_id', ['product_id', 'sku', 'item_id']),
            ('product_name', ['product_name', 'title', 'item_name']),
            ('return_reason', ['return_reason', 'reason', 'return_reason_text']),
            ('return_date', ['return_date', 'date', 'return_date_time']),
            ('refund_amount', ['refund_amount', 'price', 'total']),
            ('customer_feedback', ['customer_feedback', 'notes', 'comments']),
            ('order_id', ['order_id', 'order_number'])
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
        df['source'] = 'Website'
        
        self.data = df
        logger.info(f"Parsed {len(self.data)} website returns")
        
        return self.data
