This folder contains diverse test CSVs to validate the Return Prevention AI pipeline.

Files:
- `amazon_returns_test.csv` - Simulates Amazon returns with sizing issues, defective parts, wrong items, odor complaints, missing parts, and several date formats. Includes numeric refund values and multi-lingual notes.
- `website_returns_test.csv` - Webstore returns with inconsistent column names and reasons; tests parser auto-detection and handling of emoji and special characters.
- `support_chats_test.csv` - Support chat logs mapping to order IDs; contains agent/customer messages including escalation triggers, photos, and specific symptom details.
- `reviews_test.csv` - Product reviews with ratings; includes poor fit, durability complaints, and mismatched expectations.
- `packaging_logs_test.csv` - Shipping/packaging logs with 'TransitImpact', 'WrongLabeling', 'MoistureDamage', and other events to test pattern detection and packaging recommendations.
- `qc_reports_test.csv` - Simulated QC inspections by SKU; includes high-priority defects like stitching failures and calibration issues.

How to run:
1. Place these files in `data/raw/` (they are already included) and make sure `config.yaml` points to `data/raw` as the input directory.
2. Run the pipeline:

```powershell
python main.py
```

What to look for:
- Parsers should detect different column names (e.g., `ReturnReason`, `return_reason`, `CustomerNote`).
- The normalizer should strip extra whitespace, fix date formats, and handle emoji correctly.
- Classifier should categorize returns into the 6 categories (Quality, Sizing, Design, Packaging, Shipping, Durability).
- PatternDetector should show product-level, temporal, and packaging patterns.
- RootCauseAnalyzer & RecommendationEngine (via Ollama) should produce meaningful analysis and action items for items like "sole separation" and "size chart".

If you want additional formats (JSON, XML) or more edge-cases (non-Latin characters, extreme long notes), tell me and I will add them.  