"""QC reports data parser"""

import pandas as pd
from .base_parser import BaseParser
from src.utils import logger

class QCParser(BaseParser):
    """Parse QC reports data"""
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
    
    def parse(self) -> pd.DataFrame:
        """Parse QC report data"""
        
        # Load data
        self.load_data()
        
        if self.data.empty:
            return pd.DataFrame()
        
        # Standardize column names
        col_mapping = {}
        columns_lower = {col.lower(): col for col in self.data.columns}
        
        # Map common QC column names
        for standard_name, possible_names in [
            ('batch_id', ['batch_id', 'lot_id', 'batch_number']),
            ('product_id', ['product_id', 'sku', 'item_id']),
            ('product_name', ['product_name', 'item_name', 'title']),
            ('defect_type', ['defect_type', 'issue_type', 'type']),
            ('defect_count', ['defect_count', 'count', 'quantity']),
            ('severity', ['severity', 'level', 'impact']),
            ('qc_date', ['qc_date', 'date', 'inspection_date']),
            ('total_inspected', ['total_inspected', 'batch_size', 'total_count'])
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
        df['source'] = 'QC Reports'
        
        # Ensure numeric fields
        for col in ['defect_count', 'total_inspected']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Calculate defect rate
        if 'defect_count' in df.columns and 'total_inspected' in df.columns:
            df['defect_rate'] = (df['defect_count'] / df['total_inspected'].replace(0, 1)) * 100
        
        self.data = df
        logger.info(f"Parsed {len(self.data)} QC reports")
        
        return self.data
