
import pandas as pd
from .base_parser import BaseParser
from src.utils import logger

class ChatParser(BaseParser):
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
    
    def parse(self) -> pd.DataFrame:
        
        self.load_data()
        
        if self.data.empty:
            return pd.DataFrame()
        
        col_mapping = {}
        columns_lower = {col.lower(): col for col in self.data.columns}

        for standard_name, possible_names in [
            ('ticket_id', ['ticket_id', 'chat_id', 'conversation_id']),
            ('product_id', ['product_id', 'sku', 'product_sku']),
            ('product_name', ['product_name', 'title', 'item_name']),
            ('chat_transcript', ['transcript', 'message', 'conversation', 'chat_transcript']),
            ('issue_description', ['issue', 'problem', 'description', 'issue_description']),
            ('resolution', ['resolution', 'outcome', 'resolved_as']),
            ('created_date', ['created_date', 'date', 'chat_date']),
            ('status', ['status', 'ticket_status', 'state'])
        ]:
            for possible_name in possible_names:
                if possible_name in columns_lower:
                    col_mapping[standard_name] = columns_lower[possible_name]
                    break
      
        df = pd.DataFrame()
        for standard_name, original_name in col_mapping.items():
            if original_name in self.data.columns:
                df[standard_name] = self.data[original_name]

        df['source'] = 'Support Chat'
        df['is_return_related'] = df['chat_transcript'].fillna('').str.contains(
            r'return|refund|exchange|damaged|broken|defect|issue|problem',
            case=False,
            regex=True
        )
        
        self.data = df
        logger.info(f"Parsed {len(self.data)} support chats, {df['is_return_related'].sum()} return-related")
        
        return self.data
