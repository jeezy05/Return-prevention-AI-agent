"""Recommendation generation engine"""

import os
import requests
from src.utils import logger
from src.config import AI_CONFIG

class RecommendationEngine:
    """Generate actionable recommendations based on analysis"""
    
    def __init__(self):
        try:
            self.base_url = AI_CONFIG.get("ollama_base_url", "http://localhost:11434")
            self.model = AI_CONFIG.get("model", "mistral")
            # Test connection
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                # Check if model is available
                models = response.json().get("models", [])
                model_names = [m.get("name", "").split(":")[0] for m in models]
                
                if any(self.model in name for name in model_names):
                    self.client = "ollama"
                else:
                    available = ", ".join(model_names) if model_names else "none"
                    logger.warning(f"Model '{self.model}' not found. Available: {available}")
                    logger.warning(f"Run: ollama pull {self.model}")
                    self.client = None
            else:
                raise Exception("Ollama not responding")
        except Exception as e:
            logger.warning(f"Ollama not available: {str(e)}")
            self.client = None
    
    def generate_recommendations(self, root_causes: str, product_name: str, 
                                return_rate: float, risk_score: float) -> dict:
        """Generate recommendations from root cause analysis"""
        
        if not self.client:
            return self._fallback_recommendations(root_causes, product_name)
        
        try:
            prompt = f"""Based on this return analysis for product '{product_name}':
Return Rate: {return_rate}%
Risk Score: {risk_score}/100

Root Causes:
{root_causes}

Generate specific, actionable recommendations in these categories:
1. DESIGN ACTIONS - Changes to product design
2. MATERIALS ACTIONS - Material or component improvements
3. SIZING ACTIONS - Size/fit adjustments
4. PACKAGING ACTIONS - Packaging improvements
5. QC ACTIONS - Quality control improvements

Format as a bulleted list. Be specific and measurable."""
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=120
            )
            
            if response.status_code == 200:
                recommendations_text = response.json().get("response", "")
                return self._parse_recommendations(recommendations_text, product_name)
            else:
                return self._fallback_recommendations(root_causes, product_name)
        
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return self._fallback_recommendations(root_causes, product_name)
    
    def _parse_recommendations(self, text: str, product_name: str) -> dict:
        """Parse recommendations into structured format"""
        
        recommendations = {
            'product': product_name,
            'design': [],
            'materials': [],
            'sizing': [],
            'packaging': [],
            'qc': []
        }
        
        current_category = None
        
        for line in text.split('\n'):
            line = line.strip()
            
            if 'DESIGN' in line.upper():
                current_category = 'design'
            elif 'MATERIAL' in line.upper():
                current_category = 'materials'
            elif 'SIZING' in line.upper():
                current_category = 'sizing'
            elif 'PACKAGING' in line.upper():
                current_category = 'packaging'
            elif 'QC' in line.upper() or 'QUALITY CONTROL' in line.upper():
                current_category = 'qc'
            elif line.startswith('-') or line.startswith('•') or line.startswith('*'):
                if current_category:
                    recommendations[current_category].append(line.lstrip('-•* '))
        
        return recommendations
    
    def _fallback_recommendations(self, root_causes: str, product_name: str) -> dict:
        """Generate fallback recommendations without LLM"""
        
        recommendations = {
            'product': product_name,
            'design': ['Review product design for identified issues'],
            'materials': ['Evaluate material quality and durability'],
            'sizing': ['Verify sizing accuracy with customers'],
            'packaging': ['Improve packaging protection'],
            'qc': ['Increase QC checks and testing']
        }
        
        return recommendations
    
    def generate_action_plan(self, recommendations: dict, priority_level: str = "HIGH") -> list:
        """Generate prioritized action plan"""
        
        actions = []
        
        # Assign priorities
        priority_mapping = {
            'design': 2,
            'materials': 2,
            'sizing': 3,
            'packaging': 1,
            'qc': 1
        }
        
        for category, items in recommendations.items():
            if category != 'product':
                priority = priority_mapping.get(category, 2)
                
                for item in items:
                    actions.append({
                        'category': category,
                        'action': item,
                        'priority': ['HIGH', 'MEDIUM', 'LOW'][priority - 1],
                        'status': 'TO-DO'
                    })
        
        # Sort by priority
        priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
        actions.sort(key=lambda x: priority_order[x['priority']])
        
        logger.info(f"Generated {len(actions)} action items")
        return actions
    
    def batch_generate_recommendations(self, analysis_results: dict) -> dict:
        """Generate recommendations for multiple products"""
        
        all_recommendations = {}
        
        for product_name, analysis in analysis_results.items():
            all_recommendations[product_name] = self.generate_recommendations(
                analysis.get('root_causes', ''),
                product_name,
                analysis.get('return_rate', 0),
                analysis.get('risk_score', 0)
            )
        
        logger.info(f"Generated recommendations for {len(all_recommendations)} products")
        return all_recommendations
