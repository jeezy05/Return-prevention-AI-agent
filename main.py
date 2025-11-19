"""
Return Prevention AI Agent - Main Pipeline
Complete end-to-end pipeline for analyzing returns and generating recommendations

Uses Ollama for FREE AI analysis (no API costs, runs locally)
See OLLAMA_SETUP.md for installation instructions
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils import logger
from src.config import (
    DATA_SOURCES, RAW_DATA_DIR, PROCESSED_DATA_DIR, 
    REPORTS_DIR, PROCESSING_CONFIG
)

# Import modules
from src.ingestion import (
    AmazonParser, WebsiteParser, ChatParser, 
    ReviewParser, LogParser, QCParser
)
from src.processing import Normalizer, Classifier, PatternDetector, Aggregator
from src.analysis import RootCauseAnalyzer, RiskPredictor, RecommendationEngine
from src.reporting import ReportGenerator

def load_data():
    """Load data from all sources"""
    
    logger.info("=" * 60)
    logger.info("STEP 1: DATA INGESTION")
    logger.info("=" * 60)
    
    data_sources = {}
    
    # Amazon returns
    amazon_file = RAW_DATA_DIR / Path(DATA_SOURCES.get("amazon_returns", "amazon_returns.csv")).name
    if amazon_file.exists():
        logger.info(f"Loading Amazon data from {amazon_file}")
        amazon_parser = AmazonParser(str(amazon_file))
        data_sources['amazon'] = amazon_parser.parse()
    else:
        logger.warning(f"Amazon returns file not found: {amazon_file}")
        data_sources['amazon'] = None
    
    # Website returns
    website_file = RAW_DATA_DIR / Path(DATA_SOURCES.get("website_returns", "website_returns.csv")).name
    if website_file.exists():
        logger.info(f"Loading website data from {website_file}")
        website_parser = WebsiteParser(str(website_file))
        data_sources['website'] = website_parser.parse()
    else:
        logger.warning(f"Website returns file not found: {website_file}")
        data_sources['website'] = None
    
    # Support chats
    chats_file = RAW_DATA_DIR / Path(DATA_SOURCES.get("support_chats", "support_chats.csv")).name
    if chats_file.exists():
        logger.info(f"Loading support chats from {chats_file}")
        chat_parser = ChatParser(str(chats_file))
        data_sources['chats'] = chat_parser.parse()
    else:
        logger.warning(f"Support chats file not found: {chats_file}")
        data_sources['chats'] = None
    
    # Reviews
    reviews_file = RAW_DATA_DIR / Path(DATA_SOURCES.get("reviews", "reviews.csv")).name
    if reviews_file.exists():
        logger.info(f"Loading reviews from {reviews_file}")
        review_parser = ReviewParser(str(reviews_file))
        data_sources['reviews'] = review_parser.parse()
    else:
        logger.warning(f"Reviews file not found: {reviews_file}")
        data_sources['reviews'] = None
    
    # Packaging logs
    logs_file = RAW_DATA_DIR / Path(DATA_SOURCES.get("packaging_logs", "packaging_logs.csv")).name
    if logs_file.exists():
        logger.info(f"Loading packaging logs from {logs_file}")
        log_parser = LogParser(str(logs_file))
        data_sources['logs'] = log_parser.parse()
    else:
        logger.warning(f"Packaging logs file not found: {logs_file}")
        data_sources['logs'] = None
    
    # QC reports
    qc_file = RAW_DATA_DIR / Path(DATA_SOURCES.get("qc_reports", "qc_reports.csv")).name
    if qc_file.exists():
        logger.info(f"Loading QC reports from {qc_file}")
        qc_parser = QCParser(str(qc_file))
        data_sources['qc'] = qc_parser.parse()
    else:
        logger.warning(f"QC reports file not found: {qc_file}")
        data_sources['qc'] = None
    
    logger.info(f"✓ Loaded {sum(1 for v in data_sources.values() if v is not None)} data sources")
    return data_sources

def process_data(data_sources):
    """Process and clean data"""
    
    logger.info("=" * 60)
    logger.info("STEP 2: DATA PROCESSING")
    logger.info("=" * 60)
    
    normalizer = Normalizer()
    classifier = Classifier()
    aggregator = Aggregator()
    
    processed_data = {}
    
    # Process returns data (Amazon + Website)
    returns_dfs = []
    
    for source_name in ['amazon', 'website']:
        df = data_sources.get(source_name)
        if df is not None and not df.empty:
            logger.info(f"Processing {source_name} data...")
            
            # Normalize text columns
            df = normalizer.normalize_dataframe(
                df, 
                ['return_reason', 'customer_feedback']
            )
            
            # Remove duplicates
            df = normalizer.remove_duplicates(df)
            
            # Classify reasons
            if 'return_reason' in df.columns:
                df = classifier.classify_dataframe(df, 'return_reason')
            
            returns_dfs.append(df)
            logger.info(f"✓ Processed {source_name}: {len(df)} records")
    
    # Combine returns data
    if returns_dfs:
        combined_returns = aggregator.combine_dataframes(returns_dfs)
        processed_data['returns'] = combined_returns
        logger.info(f"✓ Combined returns data: {len(combined_returns)} total records")
    
    # Process support chats
    if data_sources.get('chats') is not None and not data_sources['chats'].empty:
        logger.info("Processing support chat data...")
        df = data_sources['chats']
        df = normalizer.normalize_dataframe(df, ['chat_transcript', 'issue_description'])
        processed_data['chats'] = df
        logger.info(f"✓ Processed chats: {len(df)} records")
    
    # Process reviews
    if data_sources.get('reviews') is not None and not data_sources['reviews'].empty:
        logger.info("Processing reviews data...")
        df = data_sources['reviews']
        df = normalizer.normalize_dataframe(df, ['review_text'])
        processed_data['reviews'] = df
        logger.info(f"✓ Processed reviews: {len(df)} records")
    
    # Store packaging and QC data as-is
    if data_sources.get('logs') is not None and not data_sources['logs'].empty:
        processed_data['packaging_logs'] = data_sources['logs']
    if data_sources.get('qc') is not None and not data_sources['qc'].empty:
        processed_data['qc_reports'] = data_sources['qc']
    
    logger.info(f"✓ Data processing complete")
    return processed_data

def analyze_data(processed_data):
    """Analyze data and generate insights"""
    
    logger.info("=" * 60)
    logger.info("STEP 3: DATA ANALYSIS")
    logger.info("=" * 60)
    
    analysis_results = {}
    
    # Pattern detection
    if 'returns' in processed_data and not processed_data['returns'].empty:
        logger.info("Detecting patterns in returns...")
        pattern_detector = PatternDetector()
        classifier_obj = Classifier()
        
        returns_df = processed_data['returns']
        
        # Product patterns
        if 'product_name' in returns_df.columns and 'return_reason' in returns_df.columns:
            product_patterns = pattern_detector.detect_product_issues(
                returns_df,
                'product_name',
                'return_reason'
            )
            analysis_results['product_patterns'] = product_patterns
            logger.info(f"✓ Detected patterns for {len(product_patterns)} products")
        
        # Category distribution
        if 'return_category' in returns_df.columns:
            category_dist = classifier_obj.get_category_distribution(returns_df)
            analysis_results['category_distribution'] = category_dist
            logger.info(f"✓ Category distribution: {list(category_dist.keys())}")
    
    # Risk prediction
    if 'returns' in processed_data and not processed_data['returns'].empty:
        logger.info("Calculating risk scores...")
        risk_predictor = RiskPredictor()
        
        returns_df = processed_data['returns']
        if 'product_name' in returns_df.columns:
            risk_scores = risk_predictor.calculate_risk_score(
                returns_df,
                'product_name'
            )
            analysis_results['risk_scores'] = risk_scores
            logger.info(f"✓ Calculated risk scores for {len(risk_scores)} products")
    
    # Root cause analysis
    logger.info("Performing root cause analysis...")
    root_cause_analyzer = RootCauseAnalyzer()
    
    root_causes = {}
    if 'product_patterns' in analysis_results:
        for product_name, pattern_data in analysis_results['product_patterns'].items():
            logger.info(f"  Analyzing {product_name}...")
            analysis = root_cause_analyzer.analyze_reasons(pattern_data, product_name)
            root_causes[product_name] = analysis
    
    analysis_results['root_causes'] = root_causes
    logger.info(f"✓ Generated root cause analysis for {len(root_causes)} products")
    
    return analysis_results

def generate_recommendations(analysis_results):
    """Generate action recommendations"""
    
    logger.info("=" * 60)
    logger.info("STEP 4: RECOMMENDATION GENERATION")
    logger.info("=" * 60)
    
    recommendation_engine = RecommendationEngine()
    
    logger.info("Generating recommendations...")
    recommendations = {}
    
    if 'root_causes' in analysis_results and 'risk_scores' in analysis_results:
        risk_df = analysis_results['risk_scores']
        root_causes_dict = analysis_results['root_causes']
        
        for _, row in risk_df.iterrows():
            product_name = row['product']
            root_cause = root_causes_dict.get(product_name, '')
            
            rec = recommendation_engine.generate_recommendations(
                root_cause,
                product_name,
                row['return_rate_percentage'],
                row['risk_score']
            )
            
            recommendations[product_name] = rec
            logger.info(f"  ✓ Generated recommendations for {product_name}")
    
    logger.info(f"✓ Generated recommendations for {len(recommendations)} products")
    return recommendations

def generate_report(processed_data, analysis_results, recommendations):
    """Generate final report"""
    
    logger.info("=" * 60)
    logger.info("STEP 5: REPORT GENERATION")
    logger.info("=" * 60)
    
    report_generator = ReportGenerator()
    
    # Prepare report data
    report_data = {}
    
    # Summary metrics
    if 'returns' in processed_data:
        total_returns = len(processed_data['returns'])
        report_data['summary'] = {
            'total_returns': total_returns,
            'data_sources': sum(1 for v in processed_data.values() if v is not None),
            'products_analyzed': len(analysis_results.get('risk_scores', [])) if 'risk_scores' in analysis_results else 0,
            'report_date': 'This Week'
        }
    
    # Top issues
    if 'returns' in processed_data:
        returns_df = processed_data['returns']
        if 'return_reason' in returns_df.columns:
            top_issues = returns_df['return_reason'].value_counts().head(10)
            issues_list = [
                {
                    'reason': reason,
                    'count': int(count),
                    'percentage': round((count / len(returns_df)) * 100, 2),
                    'category': returns_df[returns_df['return_reason'] == reason]['return_category'].iloc[0] if 'return_category' in returns_df.columns else 'Unknown'
                }
                for reason, count in top_issues.items()
            ]
            report_data['top_issues'] = issues_list
    
    # At-risk products
    if 'risk_scores' in analysis_results:
        at_risk = analysis_results['risk_scores'][
            analysis_results['risk_scores']['risk_level'] == 'HIGH'
        ].head(10)
        report_data['at_risk_products'] = at_risk.to_dict('records')
    
    # Root causes
    report_data['root_causes'] = analysis_results.get('root_causes', {})
    
    # Recommendations
    report_data['recommendations'] = recommendations
    
    # Action items
    action_items = []
    recommendation_engine = RecommendationEngine()
    for product_name, rec in recommendations.items():
        actions = recommendation_engine.generate_action_plan(rec, 'HIGH')
        action_items.extend(actions)
    
    report_data['action_items'] = action_items
    
    # Save report
    logger.info("Saving report...")
    report_generator.save_report_data(report_data)
    logger.info(f"✓ Report saved to {REPORTS_DIR}")
    
    return report_data

def main():
    """Main pipeline execution"""
    
    logger.info("\n")
    logger.info("#" * 60)
    logger.info("# RETURN PREVENTION AI AGENT - PIPELINE")
    logger.info("#" * 60)
    logger.info("\n")
    
    try:
        # Step 1: Load data
        data_sources = load_data()
        
        # Check if we have any data
        has_data = any(df is not None and not df.empty for df in data_sources.values())
        if not has_data:
            logger.warning("\n⚠️  No data files found in data/raw directory!")
            logger.warning("Please copy sample data files to: data/raw/")
            logger.warning("Sample files available in: data/templates/")
            return
        
        # Step 2: Process data
        processed_data = process_data(data_sources)
        
        # Step 3: Analyze data
        analysis_results = analyze_data(processed_data)
        
        # Step 4: Generate recommendations
        recommendations = generate_recommendations(analysis_results)
        
        # Step 5: Generate report
        report_data = generate_report(processed_data, analysis_results, recommendations)
        
        logger.info("\n")
        logger.info("#" * 60)
        logger.info("# PIPELINE EXECUTION COMPLETE ✓")
        logger.info("#" * 60)
        logger.info(f"\nReport saved to: {REPORTS_DIR}")
        logger.info("\n")
        
    except Exception as e:
        logger.error(f"\n❌ Pipeline execution failed: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
