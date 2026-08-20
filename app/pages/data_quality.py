"""
FlyBuddy - Dataset & Data Quality Page
--------------------------------------
Audit of dataset rows, columns, nulls, duplicates, data types, and the 5-stage cleaning pipeline.
"""

import streamlit as st
import pandas as pd
from app.components.theme import THEME
from app.components.header import render_header
from app.components.cards import render_kpi_card, render_insight_card

def render_data_quality_page(df_raw, df_clean):
    render_header(
        title="Dataset & Data Quality",
        subtitle="Transparent audit of raw data quality, missing values, anomalies, and preprocessing stages.",
        badge_text="🛡️ Data Quality Audit"
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Total Rows", f"{len(df_raw):,}", "Original Dataset")
    with col2:
        render_kpi_card("Raw Columns", f"{len(df_raw.columns)}", "18 Ingested Features")
    with col3:
        null_count = df_raw.isnull().sum().sum()
        render_kpi_card("Missing Values", f"{null_count:,}", "Cleaned & Imputed")
    with col4:
        render_kpi_card("Cleaned Target Rows", f"{df_clean['Price_clean'].notnull().sum():,}", "Valid Supervised Targets")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    st.markdown(f"<h3 style='color: {THEME['deep_navy']}; font-weight: 800; font-size: 1.25rem;'>🔄 Preprocessing & Cleaning Pipeline</h3>", unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 24px;">
            <div class="fb-card" style="padding: 14px 18px; border-left: 4px solid {THEME['primary_cyan']};">
                <b>Stage 1: Raw Data Ingestion & Audit</b> — Ingests 100,000 flight records; inspects data types, missing value distributions, and column formats.
            </div>
            <div class="fb-card" style="padding: 14px 18px; border-left: 4px solid {THEME['primary_cyan']};">
                <b>Stage 2: Format Standardization</b> — Parses mixed duration formats ('1h 10m', '609 min', '1.67') into unified <code>duration_minutes</code>. Normalizes stops ('non-stop', '1 stop', '2') into integer <code>total_stops_num</code>.
            </div>
            <div class="fb-card" style="padding: 14px 18px; border-left: 4px solid {THEME['primary_cyan']};">
                <b>Stage 3: Canonical Entity Mapping</b> — Standardizes 18 airport codes and suffix variations ('BOM', 'Mumbai Airport', 'Mumbai') into clean canonical city names.
            </div>
            <div class="fb-card" style="padding: 14px 18px; border-left: 4px solid {THEME['primary_cyan']};">
                <b>Stage 4: Feature Engineering</b> — Synthesizes <code>Route</code>, <code>Departure_Time_Category</code>, <code>Is_Weekend</code>, and <code>Lead_Time_Category</code>.
            </div>
            <div class="fb-card" style="padding: 14px 18px; border-left: 4px solid {THEME['primary_cyan']};">
                <b>Stage 5: Pipeline Imputation & Encoding</b> — Applies median numerical imputation and One-Hot Encoding strictly inside the Scikit-learn Pipeline on the training fold.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"<h3 style='color: {THEME['deep_navy']}; font-weight: 800; font-size: 1.25rem;'>📋 Raw Missing Value Audit</h3>", unsafe_allow_html=True)
    
    st.markdown('<div class="fb-card">', unsafe_allow_html=True)
    null_series = df_raw.isnull().sum()
    null_df = pd.DataFrame({
        'Feature Column': null_series.index,
        'Missing Values': null_series.values,
        'Missing %': (null_series.values / len(df_raw) * 100).round(2),
        'Cleaning Strategy': [
            'Kept as identifier (not in ML)',
            'Categorical Imputation (Mode)',
            'Canonical City Map + Mode',
            'Canonical City Map + Mode',
            'Parsed to datetime',
            'Parsed to hour & minute',
            'Parsed to hour & minute',
            'Regex conversion to minutes',
            'Normalized to integer (0, 1, 2)',
            'Median numerical imputation',
            'Categorical Imputation (Mode)',
            'Median numerical imputation',
            'Mode categorical imputation',
            'Mode categorical imputation',
            'Mode categorical imputation',
            'Mode categorical imputation',
            'Median numerical imputation',
            'Rows with null target omitted from training'
        ]
    })
    st.dataframe(null_df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
