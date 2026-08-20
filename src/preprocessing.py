"""
FlyBuddy - Data Preprocessing Module
------------------------------------
Handles all data cleaning, type conversions, and standardizations
for the raw flight pricing dataset.

Why this matters for interviews:
- Real-world flight data contains inconsistencies (e.g. mixed duration formats,
  string numbers, different airport codes/names, and missing values).
- We use deterministic, explainable rules to clean and standardize each column
  without silently discarding valid data.
"""

import re
import pandas as pd
import numpy as np

CITY_CANONICAL_MAP = {
    'AMD': 'Ahmedabad', 'Ahmedabad Airport': 'Ahmedabad', 'Ahmedabad': 'Ahmedabad',
    'BLR': 'Bangalore', 'Bangalore Airport': 'Bangalore', 'Bangalore': 'Bangalore',
    'BKK': 'Bangkok', 'Bangkok Airport': 'Bangkok', 'Bangkok': 'Bangkok',
    'CCU': 'Kolkata', 'Kolkata Airport': 'Kolkata', 'Kolkata': 'Kolkata',
    'DEL': 'Delhi', 'Delhi Airport': 'Delhi', 'DELHI': 'Delhi', 'Delhi': 'Delhi',
    'DOH': 'Doha', 'Doha Airport': 'Doha', 'Doha': 'Doha',
    'DXB': 'Dubai', 'Dubai Airport': 'Dubai', 'Dubai': 'Dubai',
    'FRA': 'Frankfurt', 'Frankfurt Airport': 'Frankfurt', 'Frankfurt': 'Frankfurt',
    'GOI': 'Goa', 'Goa Airport': 'Goa', 'Goa': 'Goa',
    'HYD': 'Hyderabad', 'Hyderabad Airport': 'Hyderabad', 'Hyderabad': 'Hyderabad',
    'JAI': 'Jaipur', 'Jaipur Airport': 'Jaipur', 'Jaipur': 'Jaipur',
    'JFK': 'New York', 'New York Airport': 'New York', 'New York': 'New York',
    'LHR': 'London', 'London Airport': 'London', 'London': 'London',
    'MAA': 'Chennai', 'Chennai Airport': 'Chennai', 'Chennai': 'Chennai',
    'BOM': 'Mumbai', 'Mumbai Airport': 'Mumbai', 'Mumbai': 'Mumbai',
    'PNQ': 'Pune', 'Pune Airport': 'Pune', 'Pune': 'Pune',
    'SIN': 'Singapore', 'Singapore Airport': 'Singapore', 'Singapore': 'Singapore',
    'SYD': 'Sydney', 'Sydney Airport': 'Sydney', 'Sydney': 'Sydney',
}

def parse_duration_to_minutes(duration_val):
    """
    Convert flight duration into minutes so all duration values use one consistent numerical format.
    Handles '1h 10m', '609 min', and decimal hours like '1.67'.
    """
    if pd.isna(duration_val):
        return np.nan
        
    val_str = str(duration_val).strip()
    if not val_str:
        return np.nan

    # Format 1: Hours and Minutes e.g. '1h 10m', '2h', '45m'
    hm_match = re.match(r'(?:(\d+)\s*h)?\s*(?:(\d+)\s*m)?', val_str, re.IGNORECASE)
    if hm_match and (hm_match.group(1) or hm_match.group(2)):
        hours = int(hm_match.group(1)) if hm_match.group(1) else 0
        minutes = int(hm_match.group(2)) if hm_match.group(2) else 0
        if hours > 0 or minutes > 0:
            return float(hours * 60 + minutes)

    # Format 2: Direct minutes string e.g. '609 min'
    min_match = re.match(r'^(\d+(?:\.\d+)?)\s*min', val_str, re.IGNORECASE)
    if min_match:
        return float(min_match.group(1))

    # Format 3: Decimal hours as float string e.g. '1.67' or '14.80'
    try:
        decimal_hours = float(val_str)
        return round(decimal_hours * 60.0, 1)
    except ValueError:
        return np.nan

def parse_total_stops_to_int(stops_val):
    """
    Normalize varied stop representations into a clean integer (0, 1, 2, 3).
    """
    if pd.isna(stops_val):
        return np.nan
        
    val_str = str(stops_val).strip().lower()
    if not val_str:
        return np.nan
        
    if 'non' in val_str or val_str == '0':
        return 0
    if '1' in val_str:
        return 1
    if '2' in val_str:
        return 2
    if '3' in val_str:
        return 3
        
    try:
        return int(float(val_str))
    except (ValueError, TypeError):
        return np.nan

def clean_city_name(city_val):
    """
    Standardize airport codes and airport suffix strings into canonical city names.
    """
    if pd.isna(city_val):
        return np.nan
    val_str = str(city_val).strip()
    return CITY_CANONICAL_MAP.get(val_str, val_str)

def clean_flight_dataframe(df_raw):
    """
    Main cleaning routine for the raw flight pricing dataset.
    Returns cleaned dataframe with standardized columns and types.
    """
    df = df_raw.copy()

    df['Source'] = df['Source'].apply(clean_city_name)
    df['Destination'] = df['Destination'].apply(clean_city_name)

    df['Duration_minutes'] = df['Duration'].apply(parse_duration_to_minutes)
    df['Total_Stops_num'] = df['Total_Stops'].apply(parse_total_stops_to_int)

    numeric_fields = ['Days_Before_Departure', 'Distance_km', 'Passenger_Count', 'Price']
    for field in numeric_fields:
        if field in df.columns:
            df[field + '_numeric'] = pd.to_numeric(df[field], errors='coerce')

    if 'Price_numeric' in df.columns:
        df['Price_clean'] = df['Price_numeric']

    df['Departure_Date_clean'] = pd.to_datetime(df['Departure_Date'], errors='coerce')

    return df
