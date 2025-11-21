
import pandas as pd
from pathlib import Path
from typing import Optional
from src.utils import logger

class BaseParser:
    
    def __init__(self, file_path: str):
        """Initialize parser with file path"""
        self.file_path = Path(file_path)
        self.data = None
        self.source_name = self.__class__.__name__
    
    def load_data(self) -> pd.DataFrame:
        try:
            if not self.file_path.exists():
                logger.warning(f"File not found: {self.file_path}")
                return pd.DataFrame()
            
            if self.file_path.suffix.lower() == '.csv':
                self.data = pd.read_csv(self.file_path)
            elif self.file_path.suffix.lower() in ['.json', '.jsonl']:
                self.data = pd.read_json(self.file_path)
            else:
                raise ValueError(f"Unsupported file format: {self.file_path.suffix}")
            
            logger.info(f"Loaded {len(self.data)} records from {self.source_name}")
            return self.data
        
        except Exception as e:
            logger.error(f"Error loading data from {self.source_name}: {str(e)}")
            return pd.DataFrame()
    
    def validate_columns(self, required_columns: list) -> bool:
        if self.data is None:
            return False
        
        missing = [col for col in required_columns if col not in self.data.columns]
        if missing:
            logger.warning(f"{self.source_name} missing columns: {missing}")
            return False
        return True
    
    def parse(self) -> pd.DataFrame:
        raise NotImplementedError("Subclasses must implement parse()")
    
    def save_processed(self, output_path: str) -> None:
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            self.data.to_csv(output_path, index=False)
            logger.info(f"Saved {len(self.data)} records to {output_path}")
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
