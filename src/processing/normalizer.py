import pandas as pd
from src.utils import normalize_text, logger

class Normalizer:
    def __init__(self):
        pass
    
    def normalize_dataframe(self, df: pd.DataFrame, text_columns: list) -> pd.DataFrame:
        df_copy = df.copy()
        for col in text_columns:
            if col in df_copy.columns:
                df_copy[f'{col}_normalized'] = df_copy[col].fillna('').apply(normalize_text)
        logger.info(f"Normalized {len(text_columns)} text columns")
        return df_copy
    
    def remove_duplicates(self, df: pd.DataFrame, subset_cols: list = None) -> pd.DataFrame:
        if subset_cols is None:
            subset_cols = df.columns.tolist()
        initial_len = len(df)
        df_clean = df.drop_duplicates(subset=subset_cols, keep='first')
        removed = initial_len - len(df_clean)
        logger.info(f"Removed {removed} duplicate records")
        return df_clean
    
    def fill_missing_values(self, df: pd.DataFrame, strategy: str = 'forward') -> pd.DataFrame:
        df_copy = df.copy()
        if strategy == 'forward':
            df_copy = df_copy.fillna(method='ffill')
        elif strategy == 'backward':
            df_copy = df_copy.fillna(method='bfill')
        elif strategy == 'zero':
            df_copy = df_copy.fillna(0)
        elif strategy == 'empty':
            df_copy = df_copy.fillna('')
        logger.info(f"Filled missing values using {strategy} strategy")
        return df_copy
