import json
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Load forecast data
with open('thailand_election_forecast.json', 'r', encoding='utf-8') as f:
    forecast = json.load(f)

# Party colors
party_colors = {
    "People's Party": "#FF6F00",
    "Bhumjaithai Party": "#1E3A8A", 
    "Pheu Thai Party": "#C62828",
    "Democrat Party": "#1976D2",
    "Kla Tham Party": "#2E7D32",
    "United Thai Nation Party": "#64B5F6",
    "Palang Pracharath Party": "#1B5E20",
    "Other Parties Combined": "#9E9E9E"
}

def create_seat_chart():
    """Interactive bar chart of seat predictions"""
    parties = []
    seats = []
    colors = []
    
    for party, data in sorted(forecast['seat_predictions'].items(), 
                             key=lambda x: x[1]['total_seats'], reverse=True):
        parties.append(party)
        seats.append(data['total_seats'])
        colors.append(party_colors.get(party, '#999999'))
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=parties,
        x=seats,
        orientation='h',
        marker=dict(color=colors, line=dict(color='black', width=2)),
        text=seats,
        textposition='outside',
        texttemplate='%{text} seats',
        hovertemplate='<b>%{y}</b><br>Seats: %{x}<extra></extra>'
    ))
    
    fig.add_vline(x=251, line_dash="dash", line_color="red", line_width=3,
                  annotation_text="Majority (251)", annotation_position="top")
    
    fig.update_layout(
        title="Thailand 2026 Election Forecast<br><sub>February 8, 2026</sub>",
        xaxis_title="Number of Seats",
        height=600,
        showlegend=False,
        template="plotly_white",
        font=dict(size=12)
    )
    
    return fig

def create_pie_chart():
    """Pie chart of seat distribution"""
    parties = []
    seats = []
    colors = []
    
    for party, data in forecast['seat_predictions'].items():
        parties.append(party)
        seats.append(data['total_seats'])
        colors.append(party_colors.get(party, '#999999'))
    
    fig = go.Figure(data=[go.Pie(
        labels=parties,
        values=seats,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        textinfo='label+value+percent',
        texttemplate='<b>%{label}</b><br>%{value} seats<br>(%{percent})',
        hovertemplate='<b>%{label}</b><br>Seats: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title="Seat Distribution by Party",
        height=600,
        template="plotly_white"
    )
    
    return fig

def create_confidence_intervals():
    """Interactive confidence interval chart"""
    parties = []
    lower_bounds = []
    upper_bounds = []
    predictions = []
    colors = []
    
    for party, data in sorted(forecast['seat_predictions'].items(),
                             key=lambda x: x[1]['total_seats']):
        if party == "Other Parties Combined":
            continue
        parties.append(party)
        predictions.append(data['total_seats'])
        colors.append(party_colors.get(party, '#999999'))
        
        ci = data['confidence_interval'].strip('[]').split('-')
        lower_bounds.append(int(ci[0]))
        upper_bounds.append(int(ci[1]))
    
    fig = go.Figure()
    
    # Add confidence interval bars
    for i, (party, lower, upper, pred, color) in enumerate(zip(parties, lower_bounds, upper_bounds, predictions, colors)):
        fig.add_trace(go.Scatter(
            x=[lower, upper],
            y=[party, party],
            mode='lines',
            line=dict(color=color, width=20),
            opacity=0.3,
            showlegend=False,
            hovertemplate=f'<b>{party}</b><br>Range: {lower}-{upper} seats<extra></extra>'
        ))
        
        # Add prediction point
        fig.add_trace(go.Scatter(
            x=[pred],
            y=[party],
            mode='markers+text',
            marker=dict(size=15, color=color, line=dict(color='black', width=2)),
            text=[f'{pred}'],
            textposition='middle right',
            showlegend=False,
            hovertemplate=f'<b>{party}</b><br>Prediction: {pred} seats<extra></extra>'
        ))
    
    fig.add_vline(x=251, line_dash="dash", line_color="red", line_width=2,
                  annotation_text="Majority", annotation_position="top")
    
    fig.update_layout(
        title="Seat Predictions with Confidence Intervals<br><sub>Point = Prediction, Bar = Possible Range</sub>",
        xaxis_title="Number of Seats",
        height=600,
        template="plotly_white",
        font=dict(size=12)
    )
    
    return fig

def create_coalition_scenarios():
    """Coalition scenarios visualization"""
    scenarios = []
    probabilities = []
    titles = []
    
    scenario_titles = {
        'scenario_1_people_party_led': "People's Party-Led",
        'scenario_2_bhumjaithai_led': 'Bhumjaithai-Led',
        'scenario_3_grand_coalition': 'Grand Coalition',
        'scenario_4_deadlock': 'Deadlock'
    }
    
    for key, data in forecast['coalition_scenarios'].items():
        scenarios.append(key)
        probabilities.append(float(data['probability'].strip('%')))
        titles.append(scenario_titles[key])
    
    fig = go.Figure(data=[go.Bar(
        x=titles,
        y=probabilities,
        marker=dict(color=['#FF6B35', '#4CAF50', '#2196F3', '#9E9E9E'],
                   line=dict(color='black', width=2)),
        text=probabilities,
        texttemplate='%{text}%',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Probability: %{y}%<extra></extra>'
    )])
    
    fig.update_layout(
        title="Coalition Formation Scenarios",
        yaxis_title="Probability (%)",
        height=500,
        template="plotly_white",
        showlegend=False,
        font=dict(size=12)
    )
    
    return fig

def create_regional_breakdown():
    """Regional seat distribution"""
    regions = []
    seats = []
    
    for region, data in forecast['regional_breakdown'].items():
        region_name = region.replace('_', ' ')
        regions.append(region_name)
        
        if isinstance(data['total_seats'], str):
            seat_count = int(data['total_seats'].replace('~', ''))
        else:
            seat_count = data['total_seats']
        seats.append(seat_count)
    
    fig = go.Figure(data=[go.Bar(
        x=regions,
        y=seats,
        marker=dict(color=['#FF6B35', '#4CAF50', '#E53935', '#2196F3', '#9C27B0'],
                   line=dict(color='black', width=2)),
        text=seats,
        texttemplate='%{text} seats',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Seats: %{y}<extra></extra>'
    )])
    
    fig.update_layout(
        title="Seat Distribution by Region",
        yaxis_title="Number of Seats",
        height=500,
        template="plotly_white",
        showlegend=False,
        font=dict(size=12)
    )
    
    return fig

def create_comparison_chart():
    """Historical comparison"""
    elections = ['2019', '2023', '2026 (Forecast)']
    
    # Simplified data for key parties
    peoples_data = [81, 151, 163]  # Future Forward -> Move Forward -> People's Party
    pheu_thai_data = [136, 141, 92]
    bhumjaithai_data = [51, 71, 125]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=elections, y=peoples_data,
        mode='lines+markers',
        name="People's Party (Progressive)",
        line=dict(color='#FF6B35', width=3),
        marker=dict(size=12)
    ))
    
    fig.add_trace(go.Scatter(
        x=elections, y=pheu_thai_data,
        mode='lines+markers',
        name='Pheu Thai Party',
        line=dict(color='#E53935', width=3),
        marker=dict(size=12)
    ))
    
    fig.add_trace(go.Scatter(
        x=elections, y=bhumjaithai_data,
        mode='lines+markers',
        name='Bhumjaithai Party',
        line=dict(color='#4CAF50', width=3),
        marker=dict(size=12)
    ))
    
    fig.update_layout(
        title="Historical Seat Trends (2019-2026)",
        yaxis_title="Number of Seats",
        height=500,
        template="plotly_white",
        font=dict(size=12),
        hovermode='x unified'
    )
    
    return fig

def generate_html_dashboard():
    """Generate complete HTML dashboard"""
    
    # Create all charts
    fig1 = create_seat_chart()
    fig2 = create_pie_chart()
    fig3 = create_confidence_intervals()
    fig4 = create_coalition_scenarios()
    fig5 = create_regional_breakdown()
    fig6 = create_comparison_chart()
    
    # Generate HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thailand 2026 Election Forecast Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .info-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .info-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s;
        }}
        
        .info-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.15);
        }}
        
        .info-card h3 {{
            color: #667eea;
            font-size: 2em;
            margin-bottom: 10px;
        }}
        
        .info-card p {{
            color: #666;
            font-size: 1em;
        }}
        
        .chart-section {{
            padding: 30px;
        }}
        
        .chart-container {{
            margin-bottom: 40px;
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .summary {{
            background: #f8f9fa;
            padding: 30px;
            margin: 30px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
        }}
        
        .summary h2 {{
            color: #667eea;
            margin-bottom: 15px;
        }}
        
        .summary ul {{
            list-style-position: inside;
            line-height: 1.8;
            color: #444;
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        
        .methodology {{
            background: #fff3cd;
            padding: 20px;
            margin: 30px;
            border-radius: 10px;
            border-left: 5px solid #ffc107;
        }}
        
        .methodology h3 {{
            color: #856404;
            margin-bottom: 10px;
        }}
        
        .methodology p {{
            color: #856404;
            line-height: 1.6;
            font-size: 0.95em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗳️ Thailand 2026 Election Forecast</h1>
            <p>Interactive Dashboard | Election Date: February 8, 2026</p>
            <p>Forecast Date: {forecast['forecast_date']} | Confidence: {forecast['forecast_confidence']}</p>
        </div>
        
        <div class="info-cards">
            <div class="info-card">
                <h3>500</h3>
                <p>Total Seats</p>
            </div>
            <div class="info-card">
                <h3>251</h3>
                <p>Seats for Majority</p>
            </div>
            <div class="info-card">
                <h3>163</h3>
                <p>Leading Party Forecast</p>
            </div>
            <div class="info-card">
                <h3>8</h3>
                <p>Major Parties</p>
            </div>
        </div>
        
        <div class="chart-section">
            <div class="chart-container">
                {fig1.to_html(include_plotlyjs=False, div_id="chart1")}
            </div>
            
            <div class="chart-container">
                {fig3.to_html(include_plotlyjs=False, div_id="chart3")}
            </div>
            
            <div class="chart-container">
                {fig2.to_html(include_plotlyjs=False, div_id="chart2")}
            </div>
            
            <div class="chart-container">
                {fig4.to_html(include_plotlyjs=False, div_id="chart4")}
            </div>
            
            <div class="chart-container">
                {fig5.to_html(include_plotlyjs=False, div_id="chart5")}
            </div>
            
            <div class="chart-container">
                {fig6.to_html(include_plotlyjs=False, div_id="chart6")}
            </div>
        </div>
        
        <div class="summary">
            <h2>📊 Key Findings</h2>
            <ul>
                <li><strong>People's Party</strong> leads with 163 seats (confidence interval: 145-180)</li>
                <li><strong>Bhumjaithai Party</strong> surges to 125 seats, up from 71 in 2023</li>
                <li><strong>Pheu Thai Party</strong> declines to 92 seats, down from 141 in 2023</li>
                <li>No single party reaches the 251-seat majority threshold</li>
                <li>Coalition formation remains highly uncertain with 30-40% undecided voters</li>
                <li>Bhumjaithai-led coalition (50% probability) most likely scenario</li>
            </ul>
        </div>
        
        <div class="methodology">
            <h3>⚠️ Methodology & Limitations</h3>
            <p><strong>Confidence Level:</strong> {forecast['forecast_confidence']}</p>
            <p><strong>Method:</strong> {forecast['methodology_summary'][:300]}...</p>
            <p><strong>Key Uncertainties:</strong> High undecided voter rate (30-40%), legal challenges to People's Party MPs, volatile nationalist sentiment, compressed campaign period.</p>
        </div>
        
        <div class="footer">
            <p>📅 Generated: {forecast['forecast_date']} | Data sources: NIDA, Suan Dusit, Thai Rath polls</p>
            <p>⚠️ This is a probabilistic forecast, not a prediction. Actual results may vary significantly.</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html_content

if __name__ == "__main__":
    print("Generating interactive HTML dashboard...")
    
    html = generate_html_dashboard()
    
    with open('election_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✓ Dashboard created successfully!")
    print("  → Open 'election_dashboard.html' in your browser")
