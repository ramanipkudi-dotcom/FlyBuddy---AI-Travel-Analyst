"""
FlyBuddy - Travel Analyst
=========================
Master Streamlit application entry point and router with dark glassmorphism theme.
"""

import os
import json
import joblib
import pandas as pd
import streamlit as st

# Application Components & Theme
from app.components.theme import apply_custom_theme
from app.components.sidebar import render_sidebar
from app.components.loading import render_analysis_loading

# Pages
from app.pages.landing import render_landing_page
from app.pages.overview import render_overview_page
from app.pages.explore import render_explore_page
from app.pages.price_factors import render_price_factors_page
from app.pages.booking_time import render_booking_time_page
from app.pages.forecast import render_forecast_page
from app.pages.recommendations import render_recommendations_page

# Core Data Preprocessing
from src.preprocessing import clean_flight_dataframe
from src.feature_engineering import build_engineered_features

# Set Page Config
st.set_page_config(
    page_title="FlyBuddy — Travel Analyst",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Centralized Theme & Custom CSS
apply_custom_theme()

# --- Cached Data & Model Loaders ---

@st.cache_data(show_spinner=False)
def load_datasets():
    """
    Load raw and preprocessed flight datasets with Streamlit caching.
    """
    csv_path = 'data/flight_pricing_dataset.csv'
    if not os.path.exists(csv_path):
        st.error(f"Dataset not found at {csv_path}. Please check data directory.")
        st.stop()
        
    df_raw = pd.read_csv(csv_path)
    df_clean = clean_flight_dataframe(df_raw)
    df_engineered = build_engineered_features(df_clean)
    return df_raw, df_engineered

@st.cache_resource(show_spinner=False)
def load_model_artifacts():
    """
    Load trained model pipeline and evaluation metrics with Streamlit caching.
    """
    model_path = 'models/price_model.joblib'
    metrics_path = 'models/metrics.json'

    if not os.path.exists(model_path) or not os.path.exists(metrics_path):
        return None, {}

    pipeline = joblib.load(model_path)
    with open(metrics_path, 'r', encoding='utf-8') as f:
        metrics = json.load(f)

    return pipeline, metrics

# --- Master Application Flow ---

def main():
    # Initialize Session State
    if 'has_searched' not in st.session_state:
        st.session_state['has_searched'] = False
    if 'show_loading' not in st.session_state:
        st.session_state['show_loading'] = False
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'Overview'
    if 'active_source' not in st.session_state:
        st.session_state['active_source'] = 'Chennai'
    if 'active_dest' not in st.session_state:
        st.session_state['active_dest'] = 'Mumbai'
    if 'active_route' not in st.session_state:
        st.session_state['active_route'] = 'Chennai → Mumbai'
    if 'active_class' not in st.session_state:
        st.session_state['active_class'] = 'Economy'

    # Load Data & Model
    df_raw, df = load_datasets()
    model_pipeline, metrics = load_model_artifacts()

    # Step 1: Landing Page ("Plan your next flight smarter.")
    if not st.session_state['has_searched']:
        render_landing_page()
        return

    # Step 2: Stepped Loading Screen (Intentional, smooth transition)
    if st.session_state.get('show_loading', False):
        render_analysis_loading(st.session_state['active_source'], st.session_state['active_dest'])
        st.session_state['show_loading'] = False
        st.rerun()

    # Step 3: Main Dashboard with Persistent Left Sidebar
    selected_page = render_sidebar()

    # Master Page Routing
    if selected_page == 'Overview':
        render_overview_page(df, model_pipeline, metrics)
    elif selected_page == 'Price Explorer':
        render_explore_page(df)
    elif selected_page == 'Price Factors':
        render_price_factors_page(df, metrics)
    elif selected_page == 'Best Time to Book':
        render_booking_time_page(df)
    elif selected_page == 'Price Forecast':
        render_forecast_page(df, model_pipeline, metrics)
    elif selected_page == 'Recommendations':
        render_recommendations_page(df)
    else:
        render_overview_page(df, model_pipeline, metrics)

if __name__ == '__main__':
    main()
