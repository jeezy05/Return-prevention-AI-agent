"""Packaging failure logs parser"""

import pandas as pd
from .base_parser import BaseParser
from src.utils import logger

class LogParser(BaseParser):
    """Parse packaging failure logs"""
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
    
    def parse(self) -> pd.DataFrame:
        """Parse packaging failure logs"""
        
        # Load data
        self.load_data()
        
        if self.data.empty:
            return pd.DataFrame()
        
        # Standardize column names
        col_mapping = {}
        columns_lower = {col.lower(): col for col in self.data.columns}
        
        # Map common packaging log column names
        for standard_name, possible_names in [
            ('log_id', ['log_id', 'id', 'event_id']),
            ('product_id', ['product_id', 'sku', 'item_id']),
            ('product_name', ['product_name', 'item_name', 'title']),
            ('failure_type', ['failure_type', 'type', 'issue_type']),
            ('description', ['description', 'notes', 'details']),
            ('severity', ['severity', 'level', 'impact']),
            ('log_date', ['log_date', 'date', 'timestamp']),
            ('quantity_affected', ['quantity', 'count', 'quantity_affected'])
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
        df['source'] = 'Packaging Logs'
        
        # Ensure numeric fields
        if 'quantity_affected' in df.columns:
            df['quantity_affected'] = pd.to_numeric(df['quantity_affected'], errors='coerce').fillna(0)
        
        self.data = df
        logger.info(f"Parsed {len(self.data)} packaging failure logs")
        
        return self.data
