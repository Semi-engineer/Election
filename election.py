import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import seaborn as sns

# ตั้งค่า style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# โหลดข้อมูล forecast
with open('thailand_election_forecast.json', 'r', encoding='utf-8') as f:
    forecast = json.load(f)

# สีของแต่ละพรรค (ใช้สีจริงของพรรค)
party_colors = {
    "People's Party": "#FF6B35",
    "Bhumjaithai Party": "#4CAF50", 
    "Pheu Thai Party": "#E53935",
    "Democrat Party": "#2196F3",
    "Kla Tham Party": "#9C27B0",
    "United Thai Nation Party": "#00BCD4",
    "Palang Pracharath Party": "#3F51B5",
    "Other Parties Combined": "#9E9E9E"
}

def create_seat_visualization():
    """Bar chart showing seat distribution"""
    parties = []
    seats = []
    colors = []
    
    for party, data in forecast['seat_predictions'].items():
        parties.append(party)
        seats.append(data['total_seats'])
        colors.append(party_colors.get(party, '#999999'))
    
    df = pd.DataFrame({'Party': parties, 'Seats': seats, 'Color': colors})
    df = df.sort_values('Seats', ascending=False)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    bars = ax.barh(df['Party'], df['Seats'], color=df['Color'], edgecolor='black', linewidth=1.5)
    
    # Add seat numbers on bars
    for i, (bar, seat) in enumerate(zip(bars, df['Seats'])):
        ax.text(bar.get_width() + 3, bar.get_y() + bar.get_height()/2, 
                f'{seat} seats', va='center', fontsize=11, fontweight='bold')
    
    ax.axvline(x=251, color='red', linestyle='--', linewidth=2.5, label='Majority (251 seats)', alpha=0.7)
    ax.set_xlabel('Number of Seats', fontsize=13, fontweight='bold')
    ax.set_title('Thailand 2026 Election Forecast\n(February 8, 2026)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=11, loc='lower right')
    ax.set_xlim(0, max(df['Seats']) + 30)
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    return fig

def create_parliament_semicircle():
    """Parliament semicircle diagram"""
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_aspect('equal')
    
    total_seats = 500
    radius_step = 0.15
    seats_per_row = [20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 70]
    
    seat_assignments = []
    for party, data in sorted(forecast['seat_predictions'].items(), 
                             key=lambda x: x[1]['total_seats'], reverse=True):
        for _ in range(data['total_seats']):
            seat_assignments.append(party)
    
    seat_idx = 0
    for row_idx, seats_in_row in enumerate(seats_per_row):
        radius = 1 + row_idx * radius_step
        for seat_pos in range(seats_in_row):
            if seat_idx >= total_seats:
                break
            angle = np.pi * (seat_pos / (seats_in_row - 1))
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            
            party = seat_assignments[seat_idx]
            color = party_colors.get(party, '#999999')
            
            circle = plt.Circle((x, y), 0.08, color=color, ec='black', linewidth=0.5)
            ax.add_patch(circle)
            seat_idx += 1
    
    # Add legend
    legend_elements = []
    for party, data in sorted(forecast['seat_predictions'].items(), 
                             key=lambda x: x[1]['total_seats'], reverse=True):
        legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                         markerfacecolor=party_colors.get(party, '#999999'),
                                         markersize=12, label=f"{party}: {data['total_seats']}"))
    
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05),
             ncol=3, fontsize=10, frameon=True)
    
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-0.5, 2.5)
    ax.axis('off')
    ax.set_title('Parliament Seat Layout (500 Seats)\nElection: February 8, 2026', 
                 fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    return fig

def create_coalition_scenarios():
    """Chart showing coalition formation scenarios"""
    scenarios = forecast['coalition_scenarios']
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Possible Coalition Formation Scenarios', fontsize=16, fontweight='bold')
    
    scenario_list = [
        ('scenario_1_people_party_led', "People's Party-Led Government"),
        ('scenario_2_bhumjaithai_led', 'Bhumjaithai-Led Government'),
        ('scenario_3_grand_coalition', 'Grand Coalition'),
        ('scenario_4_deadlock', 'Deadlock')
    ]
    
    for idx, (scenario_key, title) in enumerate(scenario_list):
        ax = axes[idx // 2, idx % 2]
        scenario = scenarios[scenario_key]
        
        prob = float(scenario['probability'].strip('%'))
        
        # Circle showing probability
        circle = plt.Circle((0.5, 0.7), 0.2, color='lightblue', ec='black', linewidth=2)
        ax.add_patch(circle)
        ax.text(0.5, 0.7, f"{prob}%", ha='center', va='center', 
               fontsize=24, fontweight='bold')
        
        ax.text(0.5, 0.4, title, ha='center', va='center', 
               fontsize=12, fontweight='bold', wrap=True)
        
        # Show composition
        composition_text = scenario['composition'][:80] + '...' if len(scenario['composition']) > 80 else scenario['composition']
        ax.text(0.5, 0.2, composition_text, ha='center', va='center', 
               fontsize=9, wrap=True)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    
    plt.tight_layout()
    return fig

def create_regional_breakdown():
    """Chart showing seat distribution by region"""
    regions = forecast['regional_breakdown']
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    region_names = []
    region_seats = []
    
    for region, data in regions.items():
        region_name = region.replace('_', ' ')
        region_names.append(region_name)
        
        if isinstance(data['total_seats'], str):
            seats = int(data['total_seats'].replace('~', ''))
        else:
            seats = data['total_seats']
        region_seats.append(seats)
    
    bars = ax.bar(region_names, region_seats, color=['#FF6B35', '#4CAF50', '#E53935', '#2196F3', '#9C27B0'],
                  edgecolor='black', linewidth=1.5)
    
    for bar, seats in zip(bars, region_seats):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
               f'{seats} seats', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_ylabel('Number of Seats', fontsize=13, fontweight='bold')
    ax.set_title('Seat Distribution by Region', fontsize=16, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    return fig

def create_confidence_intervals():
    """Chart showing confidence intervals"""
    parties = []
    lower_bounds = []
    upper_bounds = []
    predictions = []
    
    for party, data in forecast['seat_predictions'].items():
        if party == "Other Parties Combined":
            continue
        parties.append(party.replace(' Party', ''))
        predictions.append(data['total_seats'])
        
        ci = data['confidence_interval'].strip('[]').split('-')
        lower_bounds.append(int(ci[0]))
        upper_bounds.append(int(ci[1]))
    
    df = pd.DataFrame({
        'Party': parties,
        'Prediction': predictions,
        'Lower': lower_bounds,
        'Upper': upper_bounds
    }).sort_values('Prediction', ascending=True)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    y_pos = np.arange(len(df))
    
    for i, (idx, row) in enumerate(df.iterrows()):
        party_name = row['Party']
        full_party_name = party_name + ' Party' if party_name != "People's" else "People's Party"
        color = party_colors.get(full_party_name, '#999999')
        
        # Confidence interval bar
        ax.barh(i, row['Upper'] - row['Lower'], left=row['Lower'], 
               height=0.5, color=color, alpha=0.3, edgecolor='black')
        
        # Prediction point
        ax.plot(row['Prediction'], i, 'o', color=color, markersize=12, 
               markeredgecolor='black', markeredgewidth=2, zorder=3)
        
        # Show numbers
        ax.text(row['Prediction'], i, f"  {row['Prediction']}", 
               va='center', fontsize=10, fontweight='bold')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df['Party'])
    ax.set_xlabel('Number of Seats', fontsize=13, fontweight='bold')
    ax.set_title('Seat Predictions with Confidence Intervals\n(Point = Prediction, Bar = Possible Range)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.axvline(x=251, color='red', linestyle='--', linewidth=2, label='Majority', alpha=0.7)
    ax.legend(fontsize=11)
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    return fig

def print_summary():
    """Print summary of key information"""
    print("=" * 80)
    print("Thailand 2026 Election Forecast Summary".center(80))
    print("=" * 80)
    print(f"\nElection Date: {forecast['election_date']}")
    print(f"Forecast Date: {forecast['forecast_date']}")
    print(f"Confidence Level: {forecast['forecast_confidence']}")
    print(f"\nTotal Seats: {forecast['total_seats']} seats")
    print(f"  - Constituency: {forecast['constituency_seats']} seats")
    print(f"  - Party List: {forecast['party_list_seats']} seats")
    
    print("\n" + "-" * 80)
    print("Party Rankings (Forecast):")
    print("-" * 80)
    
    sorted_parties = sorted(forecast['seat_predictions'].items(), 
                          key=lambda x: x[1]['total_seats'], reverse=True)
    
    for rank, (party, data) in enumerate(sorted_parties, 1):
        print(f"\n{rank}. {party}")
        print(f"   Total Seats: {data['total_seats']} seats")
        print(f"   - Constituency: {data['constituency_seats']} | Party List: {data['party_list_seats']}")
        print(f"   Confidence Interval: {data['confidence_interval']}")
        print(f"   Vote Share: {data['vote_share_estimate']}")
    
    print("\n" + "=" * 80)
    print("Coalition Formation Scenarios:")
    print("=" * 80)
    
    for scenario_key, scenario in forecast['coalition_scenarios'].items():
        print(f"\n{scenario_key.replace('_', ' ').title()}:")
        print(f"  Probability: {scenario['probability']}")
        print(f"  Composition: {scenario['composition']}")
    
    print("\n" + "=" * 80)

# Run all functions
if __name__ == "__main__":
    print_summary()
    
    print("\nGenerating charts...")
    
    fig1 = create_seat_visualization()
    fig1.savefig('1_seat_forecast.png', dpi=300, bbox_inches='tight')
    
    fig2 = create_parliament_semicircle()
    fig2.savefig('2_parliament_layout.png', dpi=300, bbox_inches='tight')
    
    fig3 = create_coalition_scenarios()
    fig3.savefig('3_coalition_scenarios.png', dpi=300, bbox_inches='tight')
    
    fig4 = create_regional_breakdown()
    fig4.savefig('4_regional_breakdown.png', dpi=300, bbox_inches='tight')
    
    fig5 = create_confidence_intervals()
    fig5.savefig('5_confidence_intervals.png', dpi=300, bbox_inches='tight')
    
    print("\n✓ All charts saved successfully!")
    print("  - 1_seat_forecast.png")
    print("  - 2_parliament_layout.png")
    print("  - 3_coalition_scenarios.png")
    print("  - 4_regional_breakdown.png")
    print("  - 5_confidence_intervals.png")
    
    plt.show()