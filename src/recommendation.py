"""
FlyBuddy - Explainable Flight Recommendation Module
---------------------------------------------------
Ranks historical flight options based on user priorities (Cheapest, Fastest,
Fewest Stops, Best Value) and provides transparent reason chips.

Why this matters for interviews:
- Avoids black-box recommendation scores by attaching clear, rule-based explanations
  (e.g. 'Non-stop', 'Lowest Fare on Route', 'Below Route Average').
"""

import pandas as pd
import numpy as np

def find_recommended_flights(df, source, destination, travel_class='Economy', max_budget=None, priority='Best Value', top_n=6):
    """
    Filter and rank flights matching the route, attaching explainable badges.
    """
    subset = df[df['Price_clean'].notnull() & (df['Price_clean'] > 0)].copy()

    if source:
        subset = subset[subset['Source'] == source]
    if destination:
        subset = subset[subset['Destination'] == destination]
    if travel_class and travel_class != 'All Classes':
        subset = subset[subset['Travel_Class'] == travel_class]
    if max_budget and max_budget > 0:
        subset = subset[subset['Price_clean'] <= max_budget]

    if subset.empty:
        subset = df[df['Price_clean'].notnull() & (df['Price_clean'] > 0)].head(100).copy()

    route_median_price = subset['Price_clean'].median()
    route_min_price = subset['Price_clean'].min()
    route_min_duration = subset['Duration_minutes'].min() if 'Duration_minutes' in subset else 120

    # Calculate Value Score (lower price + shorter duration + fewer stops)
    p_norm = (subset['Price_clean'] - subset['Price_clean'].min()) / (subset['Price_clean'].max() - subset['Price_clean'].min() + 1e-5)
    d_norm = (subset['Duration_minutes'].fillna(180) - subset['Duration_minutes'].min()) / (subset['Duration_minutes'].max() - subset['Duration_minutes'].min() + 1e-5)
    s_norm = subset['Total_Stops_num'].fillna(1) / 2.0
    subset['value_score'] = (0.5 * p_norm) + (0.3 * d_norm) + (0.2 * s_norm)

    if priority == 'Cheapest':
        ranked = subset.sort_values(by='Price_clean', ascending=True)
    elif priority == 'Fastest':
        ranked = subset.sort_values(by=['Duration_minutes', 'Price_clean'], ascending=[True, True])
    elif priority == 'Fewest Stops':
        ranked = subset.sort_values(by=['Total_Stops_num', 'Price_clean'], ascending=[True, True])
    else: # Best Value
        ranked = subset.sort_values(by=['value_score', 'Price_clean'], ascending=[True, True])

    results = []
    for _, row in ranked.head(top_n).iterrows():
        reasons = []
        price = float(row['Price_clean'])
        duration = float(row.get('Duration_minutes', 120)) if pd.notnull(row.get('Duration_minutes')) else 120
        stops = int(row.get('Total_Stops_num', 0)) if pd.notnull(row.get('Total_Stops_num')) else 0

        if price <= route_min_price * 1.05:
            reasons.append('Lowest Fare on Route')
        elif price < route_median_price:
            reasons.append('Below Route Average')

        if stops == 0:
            reasons.append('Non-Stop Direct')
        elif stops == 1:
            reasons.append('Single Quick Layover')

        if duration <= route_min_duration * 1.1:
            reasons.append('Fastest Travel Time')

        if not reasons:
            reasons.append('Solid Standard Option')

        hours = int(duration // 60)
        mins = int(duration % 60)
        dur_str = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"

        results.append({
            'airline': str(row.get('Airline', 'Airline')),
            'source': str(row.get('Source', source)),
            'destination': str(row.get('Destination', destination)),
            'travel_class': str(row.get('Travel_Class', travel_class)),
            'departure_time': str(row.get('Departure_Time', '08:00 AM')),
            'arrival_time': str(row.get('Arrival_Time', '10:30 AM')),
            'duration_str': dur_str,
            'stops': stops,
            'price': price,
            'aircraft': str(row.get('Aircraft_Type', 'Airbus A320')),
            'reasons': reasons
        })

    return results
