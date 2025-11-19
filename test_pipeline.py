"""
Quick test script to verify pipeline works
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils import logger
from src.ingestion import AmazonParser
from src.processing import Normalizer, Classifier
from src.analysis import RiskPredictor
import pandas as pd

def test_pipeline():
    """Quick pipeline test"""
    
    logger.info("=" * 60)
    logger.info("TESTING RETURN PREVENTION AI AGENT")
    logger.info("=" * 60)
    
    # Create sample data
    logger.info("\n1. Creating sample data...")
    sample_data = {
        'product_id': ['SKU001', 'SKU001', 'SKU002', 'SKU002'],
        'product_name': ['Yoga Mat', 'Yoga Mat', 'Running Shoes', 'Running Shoes'],
        'return_reason': ['Cracking after use', 'Faded color', 'Too small', 'Broke after week'],
        'return_date': ['2024-11-15', '2024-11-14', '2024-11-13', '2024-11-12'],
        'refund_amount': [49.99, 49.99, 79.99, 79.99],
        'order_id': ['ORD001', 'ORD002', 'ORD003', 'ORD004']
    }
    
    df = pd.DataFrame(sample_data)
    logger.info(f"✓ Created sample dataset: {len(df)} records")
    
    # Test normalization
    logger.info("\n2. Testing text normalization...")
    normalizer = Normalizer()
    df = normalizer.normalize_dataframe(df, ['return_reason'])
    logger.info(f"✓ Normalized text columns")
    
    # Test classification
    logger.info("\n3. Testing classification...")
    classifier = Classifier()
    df = classifier.classify_dataframe(df, 'return_reason')
    logger.info(f"✓ Classified return reasons")
    logger.info(f"   Categories: {df['return_category'].value_counts().to_dict()}")
    
    # Test risk prediction
    logger.info("\n4. Testing risk prediction...")
    risk_predictor = RiskPredictor()
    risk_scores = risk_predictor.calculate_risk_score(df, 'product_name')
    logger.info(f"✓ Calculated risk scores for {len(risk_scores)} products")
    for _, row in risk_scores.iterrows():
        logger.info(f"   {row['product']}: {row['risk_score']:.1f}/100 ({row['risk_level']})")
    
    logger.info("\n" + "=" * 60)
    logger.info("✓ ALL TESTS PASSED!")
    logger.info("=" * 60)
    logger.info("\nPipeline is ready to use. Run 'python main.py' to execute full analysis.")

if __name__ == "__main__":
    test_pipeline()
