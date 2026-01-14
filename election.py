import json
import pandas as pd
import matplotlib.pyplot as plt

# โหลดข้อมูล forecast
with open('thailand_election_forecast.json', 'r', encoding='utf-8') as f:
    forecast = json.load(f)

# แปลงเป็น DataFrame
parties = []
seats = []
for party, data in forecast['seat_predictions'].items():
    parties.append(party)
    seats.append(data['total_seats'])

df = pd.DataFrame({'Party': parties, 'Seats': seats})
df = df.sort_values('Seats', ascending=False)

# สร้าง visualization
plt.figure(figsize=(12, 6))
plt.barh(df['Party'], df['Seats'])
plt.xlabel('Number of Seats')
plt.title('Thailand 2026 Election Forecast')
plt.axvline(x=251, color='r', linestyle='--', label='Majority (251)')
plt.legend()
plt.tight_layout()
plt.show()