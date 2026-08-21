"""
FlyBuddy - Explainable Flight Recommendation Module
---------------------------------------------------
Ranks historical flight options based on user priorities (Best Value, Lowest Price,
Fastest Option, Fewest Stops) with optional maximum stops and budget filters,
attaching transparent, data-grounded reason chips.
"""

import pandas as pd
import numpy as np

def find_recommended_flights(df, source=None, destination=None, travel_class='Economy', max_budget=None, max_stops=None, priority='Best Value', top_n=6):
    """
    Filter and rank flights matching the route and constraints, attaching explainable badges.
    
    Parameters:
    - df: Preprocessed flight dataframe
    - source: Origin city (string or None)
    - destination: Destination city (string or None)
    - travel_class: Travel class (e.g. 'Economy', 'Business', 'All Classes')
    - max_budget: Maximum fare cap in INR (float or None)
    - max_stops: Maximum allowed stops (int e.g. 0 for Direct, 1 for up to 1 stop, or None)
    - priority: Ranking priority ('Best Value', 'Lowest Price', 'Fastest Option', 'Fewest Stops')
    - top_n: Number of top recommended flights to return (int)
    """
    subset = df[df['Price_clean'].notnull() & (df['Price_clean'] > 0)].copy()

    if source:
        subset = subset[subset['Source'] == source]
    if destination:
        subset = subset[subset['Destination'] == destination]
    if travel_class and travel_class != 'All Classes':
        subset = subset[subset['Travel_Class'] == travel_class]
    if max_budget is not None and max_budget > 0:
        subset = subset[subset['Price_clean'] <= max_budget]
    if max_stops is not None:
        subset = subset[subset['Total_Stops_num'] <= max_stops]

    if subset.empty:
        # Fallback to route without class/stops filter if too restrictive
        fallback = df[df['Price_clean'].notnull() & (df['Price_clean'] > 0)].copy()
        if source:
            fallback = fallback[fallback['Source'] == source]
        if destination:
            fallback = fallback[fallback['Destination'] == destination]
        if max_stops is not None and not fallback.empty:
            fallback = fallback[fallback['Total_Stops_num'] <= max_stops]
        subset = fallback if not fallback.empty else df.head(50).copy()

    route_median_price = subset['Price_clean'].median() if not subset.empty else 5000.0
    route_min_price = subset['Price_clean'].min() if not subset.empty else 3000.0
    route_min_duration = subset['Duration_minutes'].min() if ('Duration_minutes' in subset and not subset.empty) else 120.0

    # Calculate Value Score (lower price + shorter duration + fewer stops)
    p_min = subset['Price_clean'].min()
    p_max = subset['Price_clean'].max()
    p_norm = (subset['Price_clean'] - p_min) / (p_max - p_min + 1e-5)

    d_col = subset['Duration_minutes'].fillna(180)
    d_min = d_col.min()
    d_max = d_col.max()
    d_norm = (d_col - d_min) / (d_max - d_min + 1e-5)

    s_col = subset['Total_Stops_num'].fillna(1)
    s_norm = s_col / 3.0
    subset['value_score'] = (0.5 * p_norm) + (0.3 * d_norm) + (0.2 * s_norm)

    # Normalize Priority string matching
    pri_lower = str(priority).lower()
    if 'low' in pri_lower or 'cheap' in pri_lower or 'price' in pri_lower:
        ranked = subset.sort_values(by='Price_clean', ascending=True)
    elif 'fast' in pri_lower or 'duration' in pri_lower or 'time' in pri_lower:
        ranked = subset.sort_values(by=['Duration_minutes', 'Price_clean'], ascending=[True, True])
    elif 'stop' in pri_lower or 'few' in pri_lower or 'direct' in pri_lower:
        ranked = subset.sort_values(by=['Total_Stops_num', 'Price_clean'], ascending=[True, True])
    else: # Best Value
        ranked = subset.sort_values(by=['value_score', 'Price_clean'], ascending=[True, True])

    results = []
    for _, row in ranked.head(top_n).iterrows():
        reasons = []
        price = float(row['Price_clean'])
        duration = float(row.get('Duration_minutes', 120)) if pd.notnull(row.get('Duration_minutes')) else 120.0
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
            'source': str(row.get('Source', source if source else 'Origin')),
            'destination': str(row.get('Destination', destination if destination else 'Destination')),
            'travel_class': str(row.get('Travel_Class', travel_class if travel_class else 'Economy')),
            'departure_time': str(row.get('Departure_Time', '08:00 AM')),
            'arrival_time': str(row.get('Arrival_Time', '10:30 AM')),
            'duration_str': dur_str,
            'stops': stops,
            'price': price,
            'aircraft': str(row.get('Aircraft_Type', 'Airbus A320')),
            'reasons': reasons
        })

    return results
