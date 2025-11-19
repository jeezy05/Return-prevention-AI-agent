# Return Prevention AI Agent - Getting Started

## Quick Start (5 minutes)

### 1. Setup
```bash
# Navigate to project directory
cd ReturnCalculator_AI

# Install dependencies
pip install -r requirements.txt

# Create .env file with your OpenAI API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 2. Prepare Sample Data
```bash
# Copy sample templates to data/raw for testing
cp data/templates/* data/raw/
```

### 3. Run Pipeline
```bash
python main.py
```

### 4. View Report
Reports are generated in the `reports/` folder:
- `return_report_*.html` - Interactive HTML report
- `return_report_*.json` - Raw JSON data

---

## Detailed Workflow

### Step 1: Data Ingestion
The pipeline reads CSV files from `data/raw/` directory:
- `amazon_returns.csv` - Amazon return orders
- `website_returns.csv` - Your website returns
- `support_chats.csv` - Customer support conversations
- `reviews.csv` - Product reviews
- `packaging_logs.csv` - Packaging failure logs
- `qc_reports.csv` - QC inspection reports

**How to prepare your data:**
1. Export data from your systems (Amazon Seller Central, Shopify, Zendesk, etc.)
2. Rename to match the template names
3. Place in `data/raw/` folder

### Step 2: Data Processing
- Normalizes text (lowercase, removes special chars)
- Removes duplicates
- Classifies return reasons into categories:
  - Quality Issues
  - Sizing Issues
  - Design Issues
  - Packaging Issues
  - Shipping Damage
  - Durability Issues

### Step 3: Analysis
- **Pattern Detection**: Identifies recurring issues per product
- **Risk Scoring**: Calculates return risk (0-100) for each product
- **Root Cause Analysis**: Uses AI to identify specific root causes

### Step 4: Recommendations
AI generates specific actions for:
- Design changes
- Material improvements
- Sizing adjustments
- Packaging enhancements
- QC improvements

### Step 5: Report Generation
Creates weekly report with:
- Summary metrics
- Top return reasons
- High-risk products
- Root cause analysis
- Recommended actions
- Prioritized action items

---

## Data Templates

### amazon_returns_template.csv
```
product_id,product_name,return_reason,return_date,refund_amount,customer_feedback,order_id
```

### website_returns_template.csv
```
product_id,product_name,return_reason,return_date,refund_amount,customer_feedback,order_id
```

### support_chats_template.csv
```
ticket_id,product_id,product_name,chat_transcript,issue_description,resolution,created_date,status
```

### reviews_template.csv
```
review_id,product_id,product_name,rating,review_text,review_date,verified_purchase
```

### packaging_logs_template.csv
```
log_id,product_id,product_name,failure_type,description,severity,log_date,quantity_affected
```

### qc_reports_template.csv
```
batch_id,product_id,product_name,defect_type,defect_count,severity,qc_date,total_inspected
```

---

## Configuration

Edit `config.yaml` to customize:
- Data source paths
- Processing settings
- AI model and temperature
- Risk thresholds
- Report settings

---

## Output

Reports are saved in `reports/` folder:

```
reports/
├── return_report_20241119_143022.html    (Interactive report)
├── return_report_20241119_143022.json    (Raw data)
└── logs/
    └── pipeline.log                       (Execution log)
```

---

## Using with LLM

The agent uses **Ollama** for AI-powered analysis (completely FREE):

1. **Download Ollama**: https://ollama.ai/download
2. **Install**: Follow installer prompts
3. **Pull model**: `ollama pull mistral`
4. **Run**: `python main.py`

No API keys needed. Data stays on your machine. See `OLLAMA_SETUP.md` for details.

Without Ollama, the pipeline uses rule-based fallback analysis.

---

## Troubleshooting

### "No data files found"
- Check data/raw/ folder exists
- Copy CSV files from data/templates/ to data/raw/
- Verify file names match exactly

### "OPENAI_API_KEY not set"
- Create .env file: `cp .env.example .env`
- Add your OpenAI API key
- Can still run without key using fallback analysis

### Import errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

---

## Next Steps

1. **Prepare your real data**: Export from your systems
2. **Run weekly**: Set up a cron job or scheduler
3. **Review reports**: Check HTML reports for insights
4. **Take action**: Implement recommendations
5. **Track impact**: Monitor return rate improvements

---

## Project Structure

```
ReturnCalculator_AI/
├── data/
│   ├── raw/                              (Input data)
│   ├── processed/                        (Processed data)
│   └── templates/                        (CSV templates)
├── src/
│   ├── ingestion/                        (Data loading)
│   ├── processing/                       (Data cleaning)
│   ├── analysis/                         (AI analysis)
│   ├── reporting/                        (Report generation)
│   └── utils/                            (Helpers)
├── reports/                              (Generated reports)
├── main.py                               (Main pipeline)
├── config.yaml                           (Configuration)
└── requirements.txt                      (Dependencies)
```

---

## Support

For issues or questions:
1. Check `logs/pipeline.log` for errors
2. Review `config.yaml` settings
3. Verify data format matches templates
4. Ensure OPENAI_API_KEY is set (if using AI)
