# Return Prevention AI Agent - Complete Setup & Execution Guide

## ✅ PROJECT COMPLETED

The complete AI agent pipeline has been created with all components ready to use!

---

## 📦 WHAT'S INCLUDED

### Project Structure
```
ReturnCalculator_AI/
├── src/
│   ├── ingestion/          (6 data parsers)
│   ├── processing/         (4 processing modules)
│   ├── analysis/           (3 analysis engines)
│   ├── reporting/          (Report generator)
│   └── utils/              (Helpers & logging)
├── data/
│   ├── raw/                (Input CSV files go here)
│   ├── processed/          (Processed data)
│   └── templates/          (CSV templates)
├── reports/                (Generated reports)
├── main.py                 (Main pipeline)
├── test_pipeline.py        (Quick test)
├── config.yaml             (Configuration)
├── requirements.txt        (Dependencies)
├── .env                    (API keys)
└── README.md              (Documentation)
```

---

## 🚀 QUICK START (5 MINUTES)

### Step 1: Install Dependencies
```bash
cd ReturnCalculator_AI
pip install -r requirements.txt
```

### Step 2: Prepare Test Data
```bash
# Copy sample templates to data/raw for testing
cp data/templates/* data/raw/
```

### Step 3: Run Test
```bash
python test_pipeline.py
```

Expected output:
```
✓ Created sample dataset: 4 records
✓ Normalized text columns
✓ Classified return reasons
✓ Calculated risk scores
✓ ALL TESTS PASSED!
```

### Step 4: Run Full Pipeline
```bash
python main.py
```

This will:
1. Load all data from data/raw/
2. Process and normalize
3. Analyze patterns
4. Generate root causes
5. Create recommendations
6. Generate reports

### Step 5: View Reports
Open generated reports in `reports/` folder:
- `return_report_*.html` - View in browser
- `return_report_*.json` - Raw data

---

## 📊 PIPELINE COMPONENTS

### 1. DATA INGESTION (src/ingestion/)
**Parsers for 6 data sources:**

```python
from src.ingestion import AmazonParser, WebsiteParser, ChatParser, ReviewParser, LogParser, QCParser

# Example usage
amazon = AmazonParser("data/raw/amazon_returns.csv")
returns_df = amazon.parse()
```

**Features:**
- Auto-detects column names (case-insensitive)
- Handles CSV and JSON formats
- Validates required columns
- Logs all operations

**Supported data sources:**
1. **Amazon Returns** - Product returns from Amazon
2. **Website Returns** - Your ecommerce platform returns
3. **Support Chats** - Customer support conversations
4. **Product Reviews** - Customer reviews
5. **Packaging Logs** - Packaging failure records
6. **QC Reports** - Quality control inspection data

---

### 2. DATA PROCESSING (src/processing/)
**4 processing modules:**

```python
from src.processing import Normalizer, Classifier, PatternDetector, Aggregator

# Normalize text
normalizer = Normalizer()
df = normalizer.normalize_dataframe(df, ['return_reason'])

# Classify into categories
classifier = Classifier()
df = classifier.classify_dataframe(df, 'return_reason')

# Detect patterns
detector = PatternDetector()
patterns = detector.detect_product_issues(df, 'product_name', 'return_reason')

# Aggregate data
aggregator = Aggregator()
combined = aggregator.combine_dataframes([df1, df2, df3])
```

**Features:**
- Text normalization (lowercase, remove special chars)
- Automatic deduplication
- Return reason classification into 6 categories:
  - Quality Issues
  - Sizing Issues
  - Design Issues
  - Packaging Issues
  - Shipping Damage
  - Durability Issues
- Pattern detection by product, time, keywords
- Data aggregation from multiple sources

---

### 3. AI ANALYSIS (src/analysis/)
**3 analysis engines:**

#### A. Root Cause Analyzer
```python
from src.analysis import RootCauseAnalyzer

analyzer = RootCauseAnalyzer()
analysis = analyzer.analyze_reasons(
    {
        'total_returns': 45,
        'top_reasons': [('Cracking', 45)]
    },
    'Yoga Mat Pro'
)
```

**Features:**
- Uses OpenAI GPT to identify specific root causes
- Provides severity levels (HIGH/MEDIUM/LOW)
- Estimates frequency and impact
- Fallback rule-based analysis if no LLM

#### B. Risk Predictor
```python
from src.analysis import RiskPredictor

predictor = RiskPredictor()
risk_scores = predictor.calculate_risk_score(df, 'product_name')
# Returns: risk_score (0-100), risk_level (HIGH/MEDIUM/LOW)
```

**Features:**
- Calculates risk score per product (0-100)
- Classifies as HIGH/MEDIUM/LOW risk
- Predicts return trends
- Estimates financial impact

#### C. Recommendation Engine
```python
from src.analysis import RecommendationEngine

engine = RecommendationEngine()
recommendations = engine.generate_recommendations(
    root_causes='Cracking after week 3',
    product_name='Yoga Mat',
    return_rate=15.0,
    risk_score=72.0
)
```

**Features:**
- AI-generated specific recommendations
- Organized by category:
  - Design Actions
  - Materials Actions
  - Sizing Actions
  - Packaging Actions
  - QC Actions
- Priority-based action plan (HIGH/MEDIUM/LOW)

---

### 4. REPORTING (src/reporting/)
**Report generator:**

```python
from src.reporting import ReportGenerator

generator = ReportGenerator()
generator.save_report_data({
    'summary': {...},
    'top_issues': [...],
    'recommendations': {...}
})
```

**Features:**
- HTML report (beautiful, interactive)
- JSON report (raw data)
- Includes:
  - Summary metrics
  - Top return reasons
  - High-risk products
  - Root cause analysis
  - Recommendations
  - Action items

---

### 5. UTILITIES (src/utils/)
**Helper functions:**

```python
from src.utils import (
    normalize_text,
    extract_keywords,
    categorize_return_reason,
    calculate_severity,
    format_currency,
    calculate_percentage
)

# Examples
clean_text = normalize_text("Product Cracking!!!")
keywords = extract_keywords("This yoga mat is breaking apart")
category = categorize_return_reason("Material defect")
severity = calculate_severity("Product broke", frequency=25)
```

---

## 🔧 CONFIGURATION

Edit `config.yaml` to customize:

```yaml
# Data sources
data_sources:
  amazon_returns: "data/raw/amazon_returns.csv"
  website_returns: "data/raw/website_returns.csv"
  support_chats: "data/raw/support_chats.csv"
  # ... more sources

# AI settings
ai_analysis:
  model: "gpt-3.5-turbo"
  temperature: 0.7
  max_tokens: 2000

# Risk thresholds
risk_prediction:
  high_threshold: 70
  medium_threshold: 40

# Report settings
reporting:
  report_format: "html"
  top_issues_count: 5
  top_products_count: 10
```

---

## 🔐 API CONFIGURATION

### Set OpenAI API Key (Optional)
For AI-powered analysis, create `.env` file:

```bash
OPENAI_API_KEY=sk-your-key-here
```

Without this, the pipeline uses rule-based fallback analysis.

### Get OpenAI API Key
1. Visit https://platform.openai.com
2. Sign up / Log in
3. Go to API keys section
4. Create new secret key
5. Copy to `.env` file

**Cost:** $0.50/1M tokens (very cheap!)

---

## 📊 DATA FORMATS

### Input CSV Templates

**amazon_returns_template.csv**
```
product_id, product_name, return_reason, return_date, refund_amount, customer_feedback, order_id
SKU001,    Yoga Mat,      Cracking,      2024-11-15,  49.99,         Poor quality,      ORD123
```

**reviews_template.csv**
```
review_id, product_id, product_name, rating, review_text,           review_date, verified_purchase
REV001,    SKU001,     Yoga Mat,     2,      Cracking after use,   2024-11-10,  true
```

All templates available in `data/templates/` folder.

---

## 📈 OUTPUT EXAMPLES

### Risk Scores
```
Product: Yoga Mat Pro
- Total Returns: 45
- Return Rate: 15%
- Risk Score: 72/100
- Risk Level: HIGH
```

### Recommendations
```
DESIGN ACTIONS:
- Review material durability (cracking issue)
- Test elasticity in humid climates
- Increase thickness by 1mm

MATERIALS ACTIONS:
- Switch to higher-grade PVC
- Add UV protection layer
```

### Action Items
```
🔴 HIGH PRIORITY (This Week)
[MATERIALS] Switch to higher-grade PVC for yoga mats

🟡 MEDIUM PRIORITY (Next 2 Weeks)
[DESIGN] Add thickness to prevent cracking
```

---

## 🧪 TESTING

### Run Quick Test
```bash
python test_pipeline.py
```

### Run Full Pipeline
```bash
python main.py
```

### Check Logs
```bash
cat logs/pipeline.log
```

---

## 📝 INTEGRATION GUIDE

### Using as Module
```python
from main import load_data, process_data, analyze_data, generate_recommendations, generate_report

# Use in your application
data = load_data()
processed = process_data(data)
analysis = analyze_data(processed)
recommendations = generate_recommendations(analysis)
report = generate_report(processed, analysis, recommendations)
```

### Weekly Automation (Cron Job)
```bash
# Run pipeline every Monday at 8 AM
0 8 * * 1 cd /path/to/ReturnCalculator_AI && python main.py
```

### Scheduling on Windows
Use Task Scheduler to run `main.py` weekly.

---

## 🐛 TROUBLESHOOTING

### Issue: "No data files found"
**Solution:**
```bash
# Copy templates to raw folder
cp data/templates/* data/raw/
# Or place your CSV files in data/raw/
```

### Issue: "OPENAI_API_KEY not set"
**Solution:**
```bash
# Create .env file with your key
echo "OPENAI_API_KEY=sk-xxx" > .env
# Or run without AI (uses fallback)
```

### Issue: Import errors
**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Issue: "pandas not found"
**Solution:**
```bash
pip install pandas numpy openai
```

---

## 📚 FILE MAPPING

| File | Purpose |
|------|---------|
| `main.py` | Main pipeline entry point |
| `test_pipeline.py` | Quick validation test |
| `config.yaml` | Configuration settings |
| `.env` | API keys (not in repo) |
| `requirements.txt` | Python dependencies |
| `src/ingestion/*.py` | Data loading (6 parsers) |
| `src/processing/*.py` | Data cleaning (4 modules) |
| `src/analysis/*.py` | AI analysis (3 engines) |
| `src/reporting/*.py` | Report generation |
| `src/utils/*.py` | Helper functions |
| `data/templates/` | CSV templates |
| `data/raw/` | Input data |
| `data/processed/` | Processed data |
| `reports/` | Generated reports |

---

## ✨ FEATURES SUMMARY

✅ **6 Data Sources** - Amazon, Website, Chats, Reviews, Packaging, QC
✅ **Automated Parsing** - Auto-detects column names
✅ **Text Processing** - Normalization, deduplication
✅ **Classification** - 6-category return reason taxonomy
✅ **Pattern Detection** - By product, time, keywords
✅ **Risk Scoring** - 0-100 risk scale per product
✅ **AI Analysis** - OpenAI GPT-powered root causes
✅ **Recommendations** - Specific, actionable items
✅ **Pretty Reports** - HTML + JSON formats
✅ **Logging** - Full audit trail
✅ **Modular Design** - Use components independently
✅ **Fallback Mode** - Works without OpenAI API

---

## 🎯 NEXT STEPS

1. **Prepare Data**: Export CSVs from your systems
2. **Place in data/raw/**: Copy your files there
3. **Run Pipeline**: `python main.py`
4. **Review Report**: Open HTML in browser
5. **Take Action**: Implement recommendations
6. **Track Results**: Monitor return rate improvements

---

## 📞 SUPPORT

For issues:
1. Check `logs/pipeline.log` for error details
2. Verify CSV file format matches templates
3. Ensure OPENAI_API_KEY is set (if using AI)
4. Review `config.yaml` settings
5. Run `test_pipeline.py` to validate setup

---

## 🎉 YOU'RE ALL SET!

The AI agent pipeline is ready to use. Start with:
```bash
python test_pipeline.py    # Quick validation
python main.py             # Full analysis
```

Happy analyzing! 🚀
