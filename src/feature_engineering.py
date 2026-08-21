"""
FlyBuddy - Feature Engineering Module
-------------------------------------
Transforms cleaned tabular data into machine-learning ready predictive features.

Feature Engineering Rationale:
- Creates domain-relevant indicators (e.g. Route, Time of Day, Weekend flag).
- Ensures no target leakage occurs.
"""

import re
import pandas as pd
import numpy as np
from datetime import datetime

def extract_time_parts(time_str):
    """
    Extract hour and minute from 12-hour or 24-hour time strings.
    """
    if pd.isna(time_str):
        return np.nan, np.nan
    val_str = str(time_str).strip()
    if not val_str:
        return np.nan, np.nan

    for fmt in ('%I:%M %p', '%I:%M%p', '%I:%M %P', '%I:%M%P', '%H:%M'):
        try:
            t = datetime.strptime(val_str, fmt).time()
            return float(t.hour), float(t.minute)
        except ValueError:
            pass
    return np.nan, np.nan

def categorize_time_of_day(hour):
    """
    Bucket departure hour into standard travel periods.
    """
    if pd.isna(hour):
        return 'Unknown'
    hour = int(hour)
    if 4 <= hour < 8:
        return 'Early Morning'
    elif 8 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Afternoon'
    elif 17 <= hour < 21:
        return 'Evening'
    else:
        return 'Night'

def build_engineered_features(df):
    """
    Generate engineered features on a cleaned dataframe.
    """
    df_feat = df.copy()

    # Route feature: Combines Source and Destination
    df_feat['Route'] = df_feat['Source'].fillna('Unknown') + ' -> ' + df_feat['Destination'].fillna('Unknown')

    # Departure time components
    dep_hours, dep_minutes = zip(*df_feat['Departure_Time'].apply(extract_time_parts))
    df_feat['Departure_Hour'] = dep_hours
    df_feat['Departure_Minute'] = dep_minutes
    df_feat['Departure_Time_Category'] = df_feat['Departure_Hour'].apply(categorize_time_of_day)

    # Weekend flag
    weekend_days = {'Saturday', 'Sunday'}
    df_feat['Is_Weekend'] = df_feat['Weekday'].apply(lambda x: 1 if str(x).strip() in weekend_days else 0)

    # Lead time bucket for analysis
    def categorize_lead_time(days):
        if pd.isna(days):
            return 'Unknown'
        if days < 7:
            return 'Last Minute (< 7d)'
        elif days < 15:
            return 'Short Notice (7-14d)'
        elif days < 30:
            return 'Standard (15-29d)'
        elif days < 60:
            return 'Advance (30-59d)'
        else:
            return 'Far Advance (60d+)'

    df_feat['Lead_Time_Category'] = df_feat['Days_Before_Departure_numeric'].apply(categorize_lead_time)
    return df_feat
