
import pandas as pd
import numpy as np
from src.utils import logger
from src.config import RISK_CONFIG

class RiskPredictor:
  
    def __init__(self):
        self.high_threshold = RISK_CONFIG["high_threshold"]
        self.medium_threshold = RISK_CONFIG["medium_threshold"]
        self.lookback_days = RISK_CONFIG["lookback_days"]
    
    def calculate_risk_score(self, df: pd.DataFrame, product_col: str, 
                            date_col: str = None, category_col: str = None) -> pd.DataFrame:
   
        
        df_copy = df.copy()
        
       
        product_returns = df_copy.groupby(product_col).size()
        total_returns = len(df_copy)
        
        return_rates = (product_returns / total_returns * 100).round(2)
        
        results = pd.DataFrame({
            'product': return_rates.index,
            'return_count': product_returns.values,
            'return_rate_percentage': return_rates.values
        }).reset_index(drop=True)
        
        results['risk_score'] = results['return_rate_percentage'] * 2  
        results['risk_score'] = results['risk_score'].clip(0, 100)
        
        max_returns = results['return_count'].max()
        frequency_factor = (results['return_count'] / max_returns * 20)
        results['risk_score'] = (results['risk_score'] + frequency_factor).clip(0, 100)
        

        results['risk_level'] = results['risk_score'].apply(self._classify_risk)
        
        logger.info(f"Calculated risk scores for {len(results)} products")
        return results.sort_values('risk_score', ascending=False)
    
    def _classify_risk(self, score: float) -> str:
        
        if score >= self.high_threshold:
            return "HIGH"
        elif score >= self.medium_threshold:
            return "MEDIUM"
        else:
            return "LOW"
    
    def predict_returns_trend(self, df: pd.DataFrame, product_col: str, 
                             date_col: str, periods: int = 4) -> dict:
        
        predictions = {}
        
        for product in df[product_col].unique():
            product_data = df[df[product_col] == product].copy()
            
            if date_col in product_data.columns:
                product_data[date_col] = pd.to_datetime(product_data[date_col], errors='coerce')
                
                
                product_data['period'] = product_data[date_col].dt.to_period('W')
                period_counts = product_data.groupby('period').size()
                
                if len(period_counts) > 0:
                    avg_returns = period_counts.mean()
                    trend = "increasing" if period_counts.iloc[-1] > avg_returns else "decreasing"
                    
                    predictions[product] = {
                        'avg_returns_per_week': round(avg_returns, 2),
                        'trend': trend,
                        'recent_returns': period_counts.iloc[-1] if len(period_counts) > 0 else 0
                    }
        
        logger.info(f"Predicted trends for {len(predictions)} products")
        return predictions
    
    def identify_at_risk_products(self, risk_df: pd.DataFrame, threshold: str = "HIGH") -> pd.DataFrame:
        
        at_risk = risk_df[risk_df['risk_level'] == threshold]
        logger.info(f"Identified {len(at_risk)} {threshold} risk products")
        
        return at_risk
    
    def calculate_estimated_impact(self, risk_df: pd.DataFrame, avg_order_value: float = 100) -> pd.DataFrame:
        
        df_copy = risk_df.copy()
        
        df_copy['estimated_monthly_returns'] = df_copy['return_count'] * 4  # Rough estimate
        df_copy['estimated_refund_amount'] = df_copy['estimated_monthly_returns'] * avg_order_value
        
        logger.info(f"Calculated estimated impact for {len(df_copy)} products")
        return df_copy
