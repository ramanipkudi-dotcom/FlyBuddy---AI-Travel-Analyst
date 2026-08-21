"""
FlyBuddy - Booking Lead-Time Analysis Module
-------------------------------------------
Analyzes historical flight pricing patterns across booking lead times
(Days_Before_Departure) to identify empirical favorable booking windows.
"""

import pandas as pd
import numpy as np

def calculate_booking_lead_time_stats(df, source=None, destination=None, travel_class=None):
    """
    Compute empirical booking lead time price statistics for the whole dataset or a specific route.
    """
    subset = df[df['Price_clean'].notnull() & (df['Price_clean'] > 0) & df['Days_Before_Departure_numeric'].notnull()].copy()

    if source:
        subset = subset[subset['Source'] == source]
    if destination:
        subset = subset[subset['Destination'] == destination]
    if travel_class and travel_class != 'All Classes':
        subset = subset[subset['Travel_Class'] == travel_class]

    if len(subset) < 10:
        return None

    bins = [-1, 7, 14, 21, 35, 50, 100]
    labels = ['Last Minute (0–7d)', 'Short Notice (8–14d)', 'Moderate (15–21d)', 'Advance (22–35d)', 'Early Bird (36–50d)', 'Far Advance (50d+)']
    subset['Window_Bin'] = pd.cut(subset['Days_Before_Departure_numeric'], bins=bins, labels=labels)

    window_stats = subset.groupby('Window_Bin', observed=False).agg(
        median_price=('Price_clean', 'median'),
        mean_price=('Price_clean', 'mean'),
        min_price=('Price_clean', 'min'),
        max_price=('Price_clean', 'max'),
        flight_count=('Price_clean', 'count')
    ).reset_index()

    # Minimum sample threshold of 5 flights per window to avoid single-flight noise
    valid_windows = window_stats[window_stats['flight_count'] >= 5]
    if not valid_windows.empty:
        best_row = valid_windows.loc[valid_windows['median_price'].idxmin()]
        cheapest_window_name = str(best_row['Window_Bin'])
        cheapest_median_price = float(best_row['median_price'])
    else:
        best_row = window_stats.loc[window_stats['median_price'].idxmin()]
        cheapest_window_name = str(best_row['Window_Bin']) if pd.notnull(best_row['Window_Bin']) else 'Advance (22–35d)'
        cheapest_median_price = float(best_row['median_price']) if pd.notnull(best_row['median_price']) else float(subset['Price_clean'].median())

    overall_median = float(subset['Price_clean'].median())
    potential_savings = max(0.0, round(((overall_median - cheapest_median_price) / overall_median) * 100, 1)) if overall_median > 0 else 0.0

    return {
        'window_stats_df': window_stats,
        'cheapest_window': cheapest_window_name,
        'cheapest_median_price': round(cheapest_median_price, 2),
        'overall_median_price': round(overall_median, 2),
        'potential_savings_pct': potential_savings,
        'sample_size': len(subset),
        'disclaimer': 'Insights are derived from historical pricing distributions and do not constitute a financial guarantee for future flight fares.'
    }
