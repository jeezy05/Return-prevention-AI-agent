"""Data aggregation module"""

import pandas as pd
from src.utils import logger

class Aggregator:
    """Aggregate data from multiple sources"""
    
    def __init__(self):
        pass
    
    def combine_dataframes(self, dataframes: list, common_columns: list = None) -> pd.DataFrame:
        """Combine multiple dataframes"""
        
        if not dataframes:
            logger.warning("No dataframes to combine")
            return pd.DataFrame()
        
        combined = pd.concat(dataframes, ignore_index=True, sort=False)
        
        logger.info(f"Combined {len(dataframes)} dataframes into {len(combined)} total records")
        return combined
    
    def aggregate_by_product(self, df: pd.DataFrame, product_col: str) -> pd.DataFrame:
        """Aggregate data by product"""
        
        if product_col not in df.columns:
            logger.warning(f"Product column {product_col} not found")
            return pd.DataFrame()
        
        agg_dict = {}
        
        # Add numeric columns
        for col in df.select_dtypes(include=['number']).columns:
            agg_dict[col] = 'sum'
        
        # Count total returns
        agg_dict['product_name'] = 'first'
        
        aggregated = df.groupby(product_col, as_index=False).agg(agg_dict)
        aggregated['return_count'] = df.groupby(product_col).size().values
        
        logger.info(f"Aggregated data by {product_col}: {len(aggregated)} unique products")
        return aggregated
    
    def aggregate_by_category(self, df: pd.DataFrame, category_col: str) -> pd.DataFrame:
        """Aggregate data by category"""
        
        if category_col not in df.columns:
            logger.warning(f"Category column {category_col} not found")
            return pd.DataFrame()
        
        aggregated = df.groupby(category_col, as_index=False).size()
        aggregated.columns = [category_col, 'count']
        aggregated['percentage'] = (aggregated['count'] / aggregated['count'].sum() * 100).round(2)
        
        logger.info(f"Aggregated data by {category_col}: {len(aggregated)} unique categories")
        return aggregated
    
    def aggregate_all_sources(self, dataframes_dict: dict) -> dict:
        """Aggregate all data sources with metadata"""
        
        summary = {}
        
        for source_name, df in dataframes_dict.items():
            if df.empty:
                summary[source_name] = {'total_records': 0}
            else:
                summary[source_name] = {
                    'total_records': len(df),
                    'columns': df.columns.tolist(),
                    'date_range': {
                        'start': None,
                        'end': None
                    }
                }
                
                # Find date columns
                date_cols = df.select_dtypes(include=['datetime64']).columns
                if len(date_cols) > 0:
                    date_col = date_cols[0]
                    summary[source_name]['date_range']['start'] = str(df[date_col].min())
                    summary[source_name]['date_range']['end'] = str(df[date_col].max())
        
        logger.info(f"Aggregated summary for {len(dataframes_dict)} sources")
        return summary
