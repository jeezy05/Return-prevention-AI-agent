
import pandas as pd
import os
import requests
from src.utils import logger
from src.config import AI_CONFIG

class RootCauseAnalyzer:
    
    def __init__(self):
        try:
            self.base_url = AI_CONFIG.get("ollama_base_url", "http://localhost:11434")
            self.model = AI_CONFIG.get("model", "mistral")
            self.temperature = AI_CONFIG.get("temperature", 0.7)
            
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                
                models = response.json().get("models", [])
                model_names = [m.get("name", "").split(":")[0] for m in models]
                
                if any(self.model in name for name in model_names):
                    self.client = "ollama"
                    logger.info(f"Connected to Ollama at {self.base_url}")
                else:
                    available = ", ".join(model_names) if model_names else "none"
                    logger.warning(f"Model '{self.model}' not found. Available: {available}")
                    logger.warning(f"Run: ollama pull {self.model}")
                    self.client = None
            else:
                raise Exception("Ollama not responding")
        except Exception as e:
            logger.warning(f"Ollama client not available: {str(e)}. Using fallback analysis.")
            self.client = None
    
    def analyze_reasons(self, reasons_data: dict, product_name: str = None) -> str:
        
        if not self.client:
            return self._fallback_analysis(reasons_data, product_name)
        
        try:
            formatted_data = self._format_for_llm(reasons_data, product_name)
            
            prompt = f"""Analyze these product return data and identify root causes:

{formatted_data}

Please provide:
1. Top 3-5 root causes (specific, pinpointed)
2. Severity level for each cause (HIGH, MEDIUM, LOW)
3. Estimated frequency/impact
4. Affected customer segments if identifiable

Be specific and actionable. Avoid generic statements."""
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": self.temperature
                },
                timeout=120
            )
            
            if response.status_code == 200:
                analysis = response.json().get("response", "")
                logger.info(f"Generated root cause analysis for {product_name or 'product'}")
                return analysis
            else:
                logger.error(f"Ollama error: {response.status_code}")
                return self._fallback_analysis(reasons_data, product_name)
        
        except Exception as e:
            logger.error(f"Error in LLM analysis: {str(e)}")
            return self._fallback_analysis(reasons_data, product_name)
    
    def _format_for_llm(self, reasons_data: dict, product_name: str = None) -> str:
        """Format data for LLM input"""
        
        formatted = f"Product: {product_name or 'Unknown'}\n"
        formatted += f"Total Returns: {reasons_data.get('total_returns', 0)}\n"
        formatted += "Top Return Reasons:\n"
        
        if 'top_reasons' in reasons_data:
            for reason, count in reasons_data['top_reasons']:
                percentage = round((count / reasons_data.get('total_returns', 1)) * 100, 1)
                formatted += f"  - {reason}: {count} returns ({percentage}%)\n"
        
        if 'categories' in reasons_data:
            formatted += "Return Categories:\n"
            for category, stats in reasons_data['categories'].items():
                formatted += f"  - {category}: {stats['count']} ({stats['percentage']}%)\n"
        
        return formatted
    
    def _fallback_analysis(self, reasons_data: dict, product_name: str) -> str:
        """Fallback analysis without LLM"""
        
        analysis = f"Root Cause Analysis for {product_name}:\n"
        analysis += f"Total Returns: {reasons_data.get('total_returns', 0)}\n\n"
        
        if 'top_reasons' in reasons_data:
            analysis += "Top Identified Issues:\n"
            for i, (reason, count) in enumerate(reasons_data['top_reasons'][:5], 1):
                analysis += f"{i}. {reason} ({count} occurrences)\n"
        
        analysis += "\nNote: Use LLM for deeper analysis. Set OPENAI_API_KEY environment variable."
        
        return analysis
    
    def batch_analyze(self, product_data: dict) -> dict:
        """Analyze multiple products"""
        
        results = {}
        
        for product_name, reasons_data in product_data.items():
            results[product_name] = self.analyze_reasons(reasons_data, product_name)
        
        logger.info(f"Batch analyzed {len(results)} products")
        return results
