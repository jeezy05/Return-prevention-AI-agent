# Return Prevention AI Agent - Quick Reference

## 🏗️ ARCHITECTURE DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────┐
│                          DATA SOURCES                               │
├─────────────────────────────────────────────────────────────────────┤
│  Amazon  │  Website  │  Support  │  Reviews  │  Packaging │   QC    │
│ Returns  │  Returns  │   Chats   │   Data    │    Logs    │ Reports │
└────┬──────────┬─────────────┬──────────┬──────────┬─────────┬────────┘
     │          │             │          │          │         │
     └──────────┴─────────────┴──────────┴──────────┴─────────┴────────┐
                                                                        │
                      ┌──────────────────────────────────┐              │
                      │   INGESTION LAYER                │◄─────────────┘
                      │  (6 CSV Parsers)                 │
                      │  - AmazonParser                  │
                      │  - WebsiteParser                 │
                      │  - ChatParser                    │
                      │  - ReviewParser                  │
                      │  - LogParser                     │
                      │  - QCParser                      │
                      └──────────────────┬───────────────┘
                                         │
                      ┌──────────────────▼───────────────┐
                      │   PROCESSING LAYER               │
                      │  (4 Processing Modules)          │
                      │  - Normalizer (text cleanup)     │
                      │  - Classifier (6 categories)     │
                      │  - PatternDetector (trends)      │
                      │  - Aggregator (combine data)     │
                      └──────────────────┬───────────────┘
                                         │
                      ┌──────────────────▼───────────────┐
                      │   ANALYSIS LAYER                 │
                      │  (3 Analysis Engines)            │
                      │  - RootCauseAnalyzer (LLM)       │
                      │  - RiskPredictor (scoring)       │
                      │  - RecommendationEngine (AI)     │
                      └──────────────────┬───────────────┘
                                         │
                      ┌──────────────────▼───────────────┐
                      │   REPORTING LAYER                │
                      │  - ReportGenerator               │
                      │  - HTML Reports                  │
                      │  - JSON Export                   │
                      └──────────────────┬───────────────┘
                                         │
                      ┌──────────────────▼───────────────┐
                      │   OUTPUT                         │
                      │  - Return Risk Predictions       │
                      │  - Root Causes                   │
                      │  - Action Items                  │
                      │  - Weekly Reports                │
                      └──────────────────────────────────┘
```

---

## 📋 QUICK START COMMANDS

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy sample data
cp data/templates/* data/raw/

# 3. Quick test
python test_pipeline.py

# 4. Full analysis
python main.py

# 5. View report
# Open reports/return_report_*.html in browser
```

---

## 🔑 KEY COMPONENTS

### Input Layer (Ingestion)
| Parser | File | Purpose |
|--------|------|---------|
| AmazonParser | amazon_returns.csv | Amazon return orders |
| WebsiteParser | website_returns.csv | Your store returns |
| ChatParser | support_chats.csv | Support tickets |
| ReviewParser | reviews.csv | Product reviews |
| LogParser | packaging_logs.csv | Packaging failures |
| QCParser | qc_reports.csv | QC inspection results |

### Processing Layer
| Module | Function |
|--------|----------|
| Normalizer | Clean text, remove duplicates |
| Classifier | Categorize into 6 issue types |
| PatternDetector | Find trends & anomalies |
| Aggregator | Combine from multiple sources |

### Analysis Layer
| Engine | Output |
|--------|--------|
| RootCauseAnalyzer | Specific root causes |
| RiskPredictor | Risk scores (0-100) |
| RecommendationEngine | Actionable items |

### Output Layer (Reporting)
| Format | Use Case |
|--------|----------|
| HTML Report | Visual dashboard |
| JSON Report | Data integration |
| Action Items | Implementation |

---

## 📊 DATA FLOW EXAMPLE

```
Input:
  50 Amazon returns: "Yoga mat cracking"
  30 Reviews: "Material broke after week"
  20 QC logs: "Seam failure detected"
         │
         ▼
Processing:
  Normalize → "cracking", "broke", "seam failure"
  Classify → All → "Quality Issue"
  Detect patterns → 100 instances of cracking
         │
         ▼
Analysis:
  Root cause: "Material insufficient for humidity"
  Risk score: 85/100 (HIGH RISK)
  Trend: Increasing (15% per week)
         │
         ▼
Recommendations:
  DESIGN: Test material in humid conditions
  MATERIALS: Upgrade to reinforced PVC
  PACKAGING: Add moisture barrier
  QC: Increase seam strength tests
         │
         ▼
Output:
  HTML Report with:
  - Risk dashboard
  - Top 5 issues
  - 12 action items
  - Implementation timeline
```

---

## 🎯 USAGE SCENARIOS

### Scenario 1: Weekly Report
```bash
# Every Monday morning
python main.py
# Generates return analysis for the past week
# Identifies new issues
# Provides recommendations
```

### Scenario 2: Product-Specific Analysis
```python
from src.ingestion import AmazonParser
from src.analysis import RiskPredictor

# Analyze specific product
parser = AmazonParser("returns.csv")
df = parser.parse()
df = df[df['product_name'] == 'Yoga Mat']

predictor = RiskPredictor()
risk_scores = predictor.calculate_risk_score(df, 'product_name')
```

### Scenario 3: Real-time Monitoring
```python
# Schedule to run daily/hourly
from main import load_data, analyze_data

# Continuous monitoring
data = load_data()
analysis = analyze_data(data)

# Alert if risk increases
```

---

## 📈 EXAMPLE OUTPUT

### Summary Metrics
```
Total Returns This Week: 523
Data Sources: 6
Products Analyzed: 47
High-Risk Products: 8
```

### Top Issues
```
1. Yoga Mat Cracking - 125 (24%)
2. Shoes Too Small - 89 (17%)
3. Water Bottle Leaking - 67 (13%)
4. Poor Color Quality - 54 (10%)
5. Packaging Damaged - 48 (9%)
```

### Risk Scores
```
Product: Yoga Mat Pro
- Return Rate: 25%
- Risk Score: 88/100
- Risk Level: CRITICAL
- Trend: INCREASING
- Estimated Impact: $12,500/month
```

### Recommendations
```
🔴 HIGH PRIORITY
[MATERIALS] Switch from standard PVC to reinforced PVC (+2mm thickness)
[DESIGN] Add stress relief grooves at seams
[QC] Increase humidity testing from 2hrs to 8hrs

🟡 MEDIUM PRIORITY
[PACKAGING] Add silica gel desiccant packets
[DESIGN] Add care instructions for humid climates
```

---

## 🔧 CONFIGURATION CHEAT SHEET

### Enable AI Features (FREE with Ollama)

```bash
# 1. Download from https://ollama.ai
# 2. Install and run Ollama
# 3. Pull model:
ollama pull mistral

# 4. Run pipeline:
python main.py
```

**Cost**: $0 (no subscriptions)
**Setup time**: 15 minutes
**No API keys needed**

### Customize Thresholds
```yaml
# In config.yaml
risk_prediction:
  high_threshold: 70    # Score >= 70 = HIGH
  medium_threshold: 40  # Score >= 40 = MEDIUM
  low_threshold: 0      # Score < 40 = LOW
```

### Add Custom Categories
```python
# In classifier.py
self.categories = {
    "Custom Category": ["keyword1", "keyword2"],
    # ...
}
```

---

## 📦 DEPENDENCIES

```
Core:
  pandas        - Data manipulation
  numpy         - Numerical operations
  requests      - HTTP requests

AI:
  openai        - GPT API (optional)

Reporting:
  jinja2        - HTML templates
  reportlab     - PDF generation
  matplotlib    - Charts

Development:
  pytest        - Testing
  python-dotenv - Environment variables
```

---

## 🚨 TROUBLESHOOTING QUICK FIXES

| Problem | Solution |
|---------|----------|
| No data found | Copy CSVs to `data/raw/` |
| Import errors | Run `pip install -r requirements.txt` |
| API errors | Check `.env` file has OPENAI_API_KEY |
| Report not generating | Check `logs/pipeline.log` for errors |
| Slow processing | Reduce data size or filter by date |

---

## 💡 PRO TIPS

1. **Start with sample data**: Use templates to test
2. **Check logs**: Always review `logs/pipeline.log`
3. **Use JSON for integration**: Export to JSON for APIs
4. **Automate weekly**: Set up cron job for Mondays
5. **Monitor trends**: Compare reports week-over-week
6. **Implement gradually**: Pick 3-5 top recommendations
7. **Track metrics**: Measure return rate reduction

---

## 📞 COMMON QUESTIONS

**Q: Can I use without OpenAI API?**
A: Yes! Rule-based fallback analysis works fine.

**Q: How often should I run?**
A: Weekly recommended for trend analysis.

**Q: Can I add more data sources?**
A: Yes, create new Parser class inheriting BaseParser.

**Q: What's the processing time?**
A: ~30 seconds for 1000 returns (varies with AI).

**Q: Can I export to database?**
A: Yes, save processed data to SQL database.

---

## 🎓 NEXT LEARNING STEPS

1. **Run test**: `python test_pipeline.py`
2. **Read code**: Review `src/ingestion/base_parser.py`
3. **Customize**: Modify config.yaml
4. **Extend**: Add new Parser class
5. **Integrate**: Import in your application

---

## 📚 FILE REFERENCE

```
Main Pipeline:
  main.py              - Entry point (run this!)
  test_pipeline.py     - Quick validation

Configuration:
  config.yaml          - Settings
  .env                 - API keys
  requirements.txt     - Dependencies

Source Code (src/):
  ingestion/           - Data loading (6 parsers)
  processing/          - Data cleaning (4 modules)
  analysis/            - AI analysis (3 engines)
  reporting/           - Report generation
  utils/               - Helpers & logging

Data:
  data/raw/            - Input CSVs (copy here)
  data/processed/      - Cleaned data
  data/templates/      - CSV format examples

Output:
  reports/             - Generated reports
  logs/                - Execution logs

Documentation:
  README.md            - Main docs
  PLAN.md              - Architecture & design
  SETUP_GUIDE.md       - Installation guide
  API_INTEGRATION_GUIDE.md - Data sources
  QUICK_REFERENCE.md   - This file!
```

---

## ⚡ PERFORMANCE TIPS

- **Small dataset** (< 100 returns): 5 seconds
- **Medium dataset** (100-1000 returns): 15 seconds
- **Large dataset** (1000+ returns): 30-60 seconds
- **With AI analysis**: Add 10-20 seconds per product

---

## 🎯 SUCCESS CRITERIA

✅ Pipeline runs without errors
✅ Generates HTML & JSON reports
✅ Identifies at least 3 unique root causes
✅ Provides 5+ actionable recommendations
✅ Completes in under 2 minutes
✅ Risk scores correlate with return rates

---

## 🚀 YOU'RE READY!

```bash
# Three commands to get started:
pip install -r requirements.txt
cp data/templates/* data/raw/
python main.py
```

Then check `reports/` folder for your first report! 🎉
