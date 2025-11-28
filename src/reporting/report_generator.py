import json
from datetime import datetime
from pathlib import Path
import pandas as pd
from src.utils import logger, format_currency, format_date
from src.config import PROJECT_ROOT, REPORTS_DIR

class ReportGenerator:
    def __init__(self):
        self.report_dir = REPORTS_DIR
        self.report_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_html_report(self, data: dict, filename: str = None) -> str:
        if filename is None:
            filename = f"return_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = self.report_dir / filename
        html_content = self._build_html(data)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info(f"Generated HTML report: {filepath}")
        return str(filepath)
    
    def generate_json_report(self, data: dict, filename: str = None) -> str:
        if filename is None:
            filename = f"return_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.report_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        logger.info(f"Generated JSON report: {filepath}")
        return str(filepath)
    
    def _build_html(self, data: dict) -> str:
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        chart_data = self._prepare_chart_data(data)
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Return Prevention Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ box-sizing: border-box; }}
        
        /* PHASE 1: Foundation & Colors */
        :root {{
            --primary: #007bff;
            --success: #28a745;
            --warning: #ffc107;
            --danger: #dc3545;
            --critical: #d32f2f;
            --info: #17a2b8;
            --light: #f8f9fa;
            --dark: #333333;
            --border: #dee2e6;
        }}
        
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }}
        
        .container {{ 
            max-width: 1600px; 
            margin: 0 auto; 
            background-color: white; 
            padding: 40px; 
            border-radius: 12px; 
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }}
        
        /* Typography */
        h1 {{ 
            color: var(--dark); 
            font-size: 32px;
            font-weight: 700;
            margin: 0 0 5px 0;
            padding-bottom: 15px;
            border-bottom: 4px solid var(--primary);
        }}
        
        .report-meta {{
            color: #666;
            font-size: 14px;
            margin-bottom: 30px;
        }}
        
        h2 {{ 
            color: var(--dark); 
            font-size: 24px;
            font-weight: 600;
            margin-top: 40px; 
            margin-bottom: 20px; 
            border-left: 5px solid var(--primary);
            padding-left: 15px;
        }}
        
        h3 {{ 
            color: #555; 
            font-size: 18px;
            font-weight: 600;
            margin-top: 15px; 
            margin-bottom: 10px; 
        }}
        
        /* PHASE 1: Sections & Layout */
        .section {{ 
            margin: 40px 0; 
            animation: fadeIn 0.3s ease-in;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* PHASE 1: Metrics Cards */
        .summary-box {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
            gap: 20px; 
            margin: 20px 0;
        }}
        
        .metric {{ 
            background: linear-gradient(135deg, var(--light) 0%, white 100%);
            padding: 25px;
            border-radius: 10px;
            border-left: 5px solid var(--primary);
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }}
        
        .metric:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.12);
        }}
        
        .metric .value {{ 
            font-size: 32px; 
            font-weight: 700; 
            color: var(--primary); 
            margin-bottom: 5px;
        }}
        
        .metric .label {{ 
            font-size: 13px; 
            color: #888; 
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .metric .trend {{
            margin-top: 10px;
            font-size: 14px;
            font-weight: 600;
        }}
        
        .metric .trend.up {{ color: var(--danger); }}
        .metric .trend.down {{ color: var(--success); }}
        .metric .trend.stable {{ color: var(--warning); }}
        
        /* PHASE 1: Badges & Tags */
        .badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin-right: 8px;
            margin-bottom: 8px;
        }}
        
        .badge-critical {{ background: #ffebee; color: var(--critical); border: 1px solid #ef5350; }}
        .badge-high {{ background: #fff3e0; color: #f57c00; border: 1px solid #ffb74d; }}
        .badge-medium {{ background: #fffde7; color: #f9a825; border: 1px solid #ffd54f; }}
        .badge-low {{ background: #e8f5e9; color: var(--success); border: 1px solid #81c784; }}
        
        /* PHASE 1: Progress Bars */
        .progress-bar {{
            background: var(--light);
            border-radius: 8px;
            height: 8px;
            overflow: hidden;
            margin: 10px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            border-radius: 8px;
            background: linear-gradient(90deg, var(--primary), #0056b3);
            transition: width 0.3s ease;
        }}
        
        .progress-label {{
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            color: #666;
            margin-bottom: 5px;
            font-weight: 500;
        }}
        
        /* PHASE 1: Trend Indicators */
        .trend-indicator {{
            font-weight: 600;
            font-size: 14px;
            display: inline-block;
        }}
        
        .trend-up {{ color: var(--danger); }}
        .trend-down {{ color: var(--success); }}
        .trend-stable {{ color: #999; }}
        
        /* PHASE 2: Chart Containers */
        .chart-container {{
            position: relative;
            height: 400px;
            margin: 30px 0;
            padding: 20px;
            background: var(--light);
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        .chart-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .chart-small {{
            position: relative;
            height: 300px;
            margin: 20px 0;
            padding: 20px;
            background: var(--light);
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        /* Tables with hover effects */
        table {{ 
            width: 100%; 
            border-collapse: collapse; 
            margin: 20px 0;
            font-size: 14px;
        }}
        
        th {{ 
            background: linear-gradient(135deg, var(--primary), #0056b3);
            color: white; 
            padding: 16px 12px; 
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.5px;
        }}
        
        td {{ 
            padding: 14px 12px; 
            border-bottom: 1px solid var(--border);
            word-wrap: break-word;
        }}
        
        tr:hover {{ 
            background-color: #f9f9f9;
        }}
        
        tr:last-child td {{
            border-bottom: 2px solid var(--primary);
        }}
        
        /* PHASE 1: Risk Level Styling */
        .risk-critical {{
            background: #ffebee;
            color: var(--critical);
            font-weight: 700;
            padding: 6px 12px;
            border-radius: 6px;
        }}
        
        .risk-high {{
            background: #fff3e0;
            color: #f57c00;
            font-weight: 700;
            padding: 6px 12px;
            border-radius: 6px;
        }}
        
        .risk-medium {{
            background: #fffde7;
            color: #f9a825;
            font-weight: 700;
            padding: 6px 12px;
            border-radius: 6px;
        }}
        
        .risk-low {{
            background: #e8f5e9;
            color: var(--success);
            font-weight: 700;
            padding: 6px 12px;
            border-radius: 6px;
        }}
        
        /* PHASE 1: Action Items */
        .action-item {{
            background: linear-gradient(90deg, #fff8e1 0%, #fffde7 100%);
            padding: 16px;
            margin: 12px 0; 
            border-left: 4px solid var(--warning);
            border-radius: 6px;
            word-wrap: break-word;
            transition: all 0.3s ease;
        }}
        
        .action-item:hover {{
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transform: translateX(5px);
        }}
        
        .action-item strong {{ 
            color: var(--primary);
            font-weight: 700;
        }}
        
        .action-item.high {{
            background: linear-gradient(90deg, #ffebee 0%, #ffcdd2 100%);
            border-left-color: var(--danger);
        }}
        
        .action-item.medium {{
            background: linear-gradient(90deg, #fff3e0 0%, #ffe0b2 100%);
            border-left-color: #ff9800;
        }}
        
        .cause-card {{
            background: linear-gradient(135deg, var(--light) 0%, #e3f2fd 100%);
            padding: 20px;
            margin: 20px 0;
            border-radius: 10px;
            border-left: 5px solid var(--primary);
            line-height: 1.7;
        }}
        
        .cause-card h3 {{
            margin-top: 0;
            color: var(--dark);
        }}
        
        .cause-card p {{
            white-space: pre-wrap;
            word-wrap: break-word;
            color: #555;
            font-size: 14px;
        }}
        
        .footer {{
            text-align: center; 
            color: #999; 
            font-size: 12px; 
            margin-top: 50px; 
            border-top: 2px solid var(--border); 
            padding-top: 30px;
            font-weight: 500;
        }}
        
        @media (max-width: 1200px) {{
            .container {{ padding: 20px; }}
            .summary-box {{ grid-template-columns: repeat(2, 1fr); }}
            .chart-row {{ grid-template-columns: 1fr; }}
        }}
        
        @media (max-width: 768px) {{
            .container {{ padding: 15px; }}
            h1 {{ font-size: 24px; }}
            h2 {{ font-size: 20px; }}
            .summary-box {{ grid-template-columns: 1fr; }}
            .chart-container {{ height: 300px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Weekly Return Prevention Report</h1>
        <div class="report-meta">
            <strong>Generated:</strong> {timestamp}
        </div>
"""
        if 'summary' in data:
            html += self._build_summary_section(data['summary'])
        html += self._build_charts_section(chart_data)
        if 'top_issues' in data:
            html += self._build_top_issues_section(data['top_issues'])
        if 'at_risk_products' in data:
            html += self._build_at_risk_section(data['at_risk_products'])
        if 'root_causes' in data:
            html += self._build_root_causes_section(data['root_causes'])
        if 'recommendations' in data:
            html += self._build_recommendations_section(data['recommendations'])
        if 'action_items' in data:
            html += self._build_action_items_section(data['action_items'])
        
        html += f"""
        <div class="footer">
            <p>🤖 Return Prevention AI Agent | Report Generated Automatically</p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _prepare_chart_data(self, data: dict) -> dict:
        chart_data = {}
        if 'top_issues' in data:
            issues = data['top_issues'][:8]
            chart_data['top_issues'] = {
                'labels': [issue.get('reason', '')[:30] for issue in issues],
                'data': [issue.get('count', 0) for issue in issues],
                'percentages': [issue.get('percentage', 0) for issue in issues]
            }
        if 'summary' in data and 'categories' in data.get('summary', {}):
            categories = data['summary']['categories']
            chart_data['categories'] = {
                'labels': list(categories.keys()),
                'data': list(categories.values())
            }
        if 'at_risk_products' in data:
            products = data['at_risk_products']
            risk_levels = {}
            for product in products:
                level = product.get('risk_level', 'UNKNOWN')
                risk_levels[level] = risk_levels.get(level, 0) + 1
            chart_data['risk_distribution'] = risk_levels
        return chart_data
    
    def _build_charts_section(self, chart_data: dict) -> str:
        if not chart_data:
            return ""
        
        html = """
        <div class="section">
            <h2>📈 Visual Analytics</h2>
            <div class="chart-row">
"""
        if 'top_issues' in chart_data:
            issues = chart_data['top_issues']
            labels_json = json.dumps(issues['labels'])
            data_json = json.dumps(issues['data'])
            html += f"""
                <div class="chart-small">
                    <canvas id="topIssuesChart"></canvas>
                </div>
                <script>
                    new Chart(document.getElementById('topIssuesChart'), {{
                        type: 'bar',
                        data: {{
                            labels: {labels_json},
                            datasets: [{{
                                label: 'Return Count',
                                data: {data_json},
                                backgroundColor: [
                                    '#dc3545', '#ff7043', '#ff9800', '#ffc107', 
                                    '#ffeb3b', '#8bc34a', '#4caf50', '#2196f3'
                                ],
                                borderRadius: 6,
                                borderSkipped: false
                            }}]
                        }},
                        options: {{
                            indexAxis: 'y',
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {{
                                legend: {{ display: false }},
                                title: {{
                                    display: true,
                                    text: '🚨 Top Return Reasons',
                                    font: {{ size: 14, weight: 'bold' }}
                                }}
                            }},
                            scales: {{
                                x: {{ beginAtZero: true, ticks: {{ color: '#666' }} }},
                                y: {{ ticks: {{ color: '#666' }} }}
                            }}
                        }}
                    }});
                </script>
            </div>
"""
        if 'risk_distribution' in chart_data:
            risk_dist = chart_data['risk_distribution']
            risk_labels = []
            risk_data = []
            risk_colors = []
            risk_color_map = {
                'CRITICAL': '#d32f2f',
                'HIGH': '#f57c00',
                'MEDIUM': '#fbc02d',
                'LOW': '#388e3c'
            }
            for level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
                if level in risk_dist:
                    risk_labels.append(level)
                    risk_data.append(risk_dist[level])
                    risk_colors.append(risk_color_map.get(level, '#ccc'))
            if risk_data:
                labels_json = json.dumps(risk_labels)
                data_json = json.dumps(risk_data)
                colors_json = json.dumps(risk_colors)
                html += f"""
                <div class="chart-small">
                    <canvas id="riskDistributionChart"></canvas>
                </div>
                <script>
                    new Chart(document.getElementById('riskDistributionChart'), {{
                        type: 'doughnut',
                        data: {{
                            labels: {labels_json},
                            datasets: [{{
                                data: {data_json},
                                backgroundColor: {colors_json},
                                borderColor: 'white',
                                borderWidth: 2
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {{
                                legend: {{ position: 'bottom', labels: {{ padding: 15 }} }},
                                title: {{
                                    display: true,
                                    text: '⚠️ Product Risk Distribution',
                                    font: {{ size: 14, weight: 'bold' }}
                                }}
                            }}
                        }}
                    }});
                </script>
            </div>
"""
        html += """
            </div>
        </div>
"""
        return html
    
    def _build_summary_section(self, summary: dict) -> str:
        html = """
        <div class="section">
            <h2>📈 Key Metrics</h2>
            <div class="summary-box">
"""
        metric_icons = {
            'total_returns': '📦',
            'unique_products': '🏷️',
            'average_return_rate': '📊',
            'high_risk_count': '🚨',
            'avg_risk_score': '⚡'
        }
        for key, value in summary.items():
            icon = metric_icons.get(key, '📌')
            html += f"""
                <div class="metric">
                    <div style="font-size: 24px; margin-bottom: 5px;">{icon}</div>
                    <div class="value">{value}</div>
                    <div class="label">{key.replace('_', ' ').title()}</div>
                </div>
"""
        html += """
            </div>
        </div>
"""
        return html
    
    def _build_top_issues_section(self, issues: list) -> str:
        html = """
        <div class="section">
            <h2>🚨 Top Return Reasons</h2>
            <table>
                <tr>
                    <th>Issue</th>
                    <th style="width: 100px;">Count</th>
                    <th style="width: 120px;">Progress</th>
                    <th style="width: 150px;">Category</th>
                </tr>
"""
        max_count = max([issue.get('count', 0) for issue in issues[:10]], default=1)
        for issue in issues[:10]:
            count = issue.get('count', 0)
            percentage = issue.get('percentage', 0)
            category = issue.get('category', 'Other')
            if percentage >= 40:
                badge_class = 'badge-critical'
            elif percentage >= 25:
                badge_class = 'badge-high'
            elif percentage >= 10:
                badge_class = 'badge-medium'
            else:
                badge_class = 'badge-low'
            progress_width = (count / max_count) * 100 if max_count > 0 else 0
            html += f"""
                <tr>
                    <td><strong>{issue.get('reason', 'Unknown')}</strong></td>
                    <td><span class="badge {badge_class}">{count}</span></td>
                    <td>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {progress_width}%"></div>
                        </div>
                        <div class="progress-label" style="font-size: 12px;">{percentage}%</div>
                    </td>
                    <td>{category}</td>
                </tr>
"""
        html += """
            </table>
        </div>
"""
        return html
    
    def _build_at_risk_section(self, products: list) -> str:
        html = """
        <div class="section">
            <h2>⚠️ High-Risk Products</h2>
            <table>
                <tr>
                    <th>Product</th>
                    <th style="width: 130px;">Return Count</th>
                    <th style="width: 140px;">Return Rate</th>
                    <th style="width: 140px;">Risk Score</th>
                    <th style="width: 120px;">Status</th>
                </tr>
"""
        for product in products[:10]:
            risk_level = product.get('risk_level', 'UNKNOWN')
            risk_score = product.get('risk_score', 0)
            return_rate = product.get('return_rate_percentage', 0)
            if risk_level == 'CRITICAL':
                risk_badge = '<span class="badge badge-critical">🔴 CRITICAL</span>'
            elif risk_level == 'HIGH':
                risk_badge = '<span class="badge badge-high">🟠 HIGH</span>'
            elif risk_level == 'MEDIUM':
                risk_badge = '<span class="badge badge-medium">🟡 MEDIUM</span>'
            else:
                risk_badge = '<span class="badge badge-low">🟢 LOW</span>'
            bar_width = min(risk_score, 100)
            bar_color = '#d32f2f' if bar_width >= 70 else '#f57c00' if bar_width >= 50 else '#fbc02d' if bar_width >= 30 else '#388e3c'
            html += f"""
                <tr>
                    <td><strong>{product.get('product', 'Unknown')}</strong></td>
                    <td>{product.get('return_count', 0)}</td>
                    <td>
                        <div class="progress-bar" style="background: #e0e0e0;">
                            <div class="progress-fill" style="width: {min(return_rate * 2, 100)}%; background: #ff9800;"></div>
                        </div>
                        <span style="font-size: 12px; color: #666;">{return_rate:.1f}%</span>
                    </td>
                    <td>
                        <div style="font-weight: 600; font-size: 14px; color: {bar_color};">{risk_score:.0f}/100</div>
                        <div class="progress-bar" style="background: #e0e0e0; margin-top: 4px;">
                            <div class="progress-fill" style="width: {bar_width}%; background: {bar_color};"></div>
                        </div>
                    </td>
                    <td>{risk_badge}</td>
                </tr>
"""
        html += """
            </table>
        </div>
"""
        return html
    
    def _build_root_causes_section(self, causes: dict) -> str:
        html = """
        <div class="section">
            <h2>🔍 Root Cause Analysis</h2>
"""
        for product, analysis in list(causes.items())[:10]:
            safe_analysis = analysis.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
            html += f"""
            <div class="cause-card">
                <h3 style="margin-top: 0; color: #007bff;">{product}</h3>
                <p>{safe_analysis}</p>
            </div>
"""
        html += """
        </div>
"""
        return html
    
    def _build_recommendations_section(self, recommendations: dict) -> str:
        html = """
        <div class="section">
            <h2>💡 Strategic Recommendations</h2>
"""
        for product, rec_data in list(recommendations.items())[:5]:
            html += f"""
            <div style="margin-bottom: 30px; background: linear-gradient(135deg, #f0f4ff 0%, #e8f1ff 100%); padding: 20px; border-radius: 10px; border-left: 5px solid #007bff;">
                <h3 style="color: #007bff; margin-top: 0;">{product}</h3>
"""
            if rec_data.get('design'):
                html += """
                <div style="margin: 15px 0;">
                    <h4 style="color: #555; font-weight: 600; margin-bottom: 10px;">🎨 Design Actions</h4>
"""
                for action in rec_data.get('design', [])[:3]:
                    html += f'<div style="padding: 8px 12px; background: white; margin: 6px 0; border-radius: 4px; border-left: 3px solid #007bff; font-size: 13px;">✓ {action}</div>'
                html += "</div>"
            if rec_data.get('materials'):
                html += """
                <div style="margin: 15px 0;">
                    <h4 style="color: #555; font-weight: 600; margin-bottom: 10px;">🔧 Materials Actions</h4>
"""
                for action in rec_data.get('materials', [])[:3]:
                    html += f'<div style="padding: 8px 12px; background: white; margin: 6px 0; border-radius: 4px; border-left: 3px solid #ff9800; font-size: 13px;">✓ {action}</div>'
                html += "</div>"
            if rec_data.get('packaging'):
                html += """
                <div style="margin: 15px 0;">
                    <h4 style="color: #555; font-weight: 600; margin-bottom: 10px;">📦 Packaging Actions</h4>
"""
                for action in rec_data.get('packaging', [])[:3]:
                    html += f'<div style="padding: 8px 12px; background: white; margin: 6px 0; border-radius: 4px; border-left: 3px solid #4caf50; font-size: 13px;">✓ {action}</div>'
                html += "</div>"
            html += """
            </div>
"""
        html += """
        </div>
"""
        return html
    
    def _build_action_items_section(self, actions: list) -> str:
        html = """
        <div class="section">
            <h2>✅ Action Plan</h2>
"""
        high_priority = [a for a in actions if a.get('priority') == 'HIGH']
        medium_priority = [a for a in actions if a.get('priority') == 'MEDIUM']
        low_priority = [a for a in actions if a.get('priority') == 'LOW']
        
        if high_priority:
            html += '<h3 style="color: #d32f2f; margin-top: 20px;">🔴 HIGH PRIORITY - Complete ASAP</h3>'
            for action in high_priority[:8]:
                html += f"""
            <div class="action-item high">
                <span class="badge badge-critical">{action.get('category', 'GENERAL').upper()}</span>
                <strong>{action.get('action', 'Action')}</strong>
            </div>
"""
        
        if medium_priority:
            html += '<h3 style="color: #f57c00; margin-top: 20px;">🟠 MEDIUM PRIORITY - Plan This Month</h3>'
            for action in medium_priority[:6]:
                html += f"""
            <div class="action-item medium">
                <span class="badge badge-high">{action.get('category', 'GENERAL').upper()}</span>
                <strong>{action.get('action', 'Action')}</strong>
            </div>
"""
        
        if low_priority:
            html += '<h3 style="color: #fbc02d; margin-top: 20px;">🟡 LOW PRIORITY - Monitor and Plan</h3>'
            for action in low_priority[:4]:
                html += f"""
            <div class="action-item medium">
                <span class="badge badge-medium">{action.get('category', 'GENERAL').upper()}</span>
                <strong>{action.get('action', 'Action')}</strong>
            </div>
"""
        
        html += """
        </div>
"""
        return html
    
    def save_report_data(self, data: dict, filename: str = None) -> None:
        if filename is None:
            base_filename = f"return_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        else:
            base_filename = filename.replace('.html', '').replace('.json', '')
        self.generate_html_report(data, f"{base_filename}.html")
        self.generate_json_report(data, f"{base_filename}.json")
        logger.info(f"Saved report data: {base_filename}")
