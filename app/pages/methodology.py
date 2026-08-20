"""
FlyBuddy - Methodology & System Architecture Page
-------------------------------------------------
Comprehensive documentation of the technical approach, ML principles, and recruitment talking points.
"""

import streamlit as st
from app.components.theme import THEME
from app.components.header import render_header
from app.components.cards import render_insight_card

def render_methodology_page():
    render_header(
        title="Methodology & Architecture",
        subtitle="End-to-end design decisions, software engineering principles, and interview explanation reference.",
        badge_text="📖 Technical Guide"
    )

    st.markdown(
        f"""
        <div class="fb-card" style="line-height: 1.6;">
            <h3 style="color: {THEME['deep_navy']}; font-weight: 800; margin-top: 0;">1. Problem Formulation</h3>
            <p>
                Airfare pricing in modern commercial aviation is driven by algorithmic dynamic yield management. 
                FlyBuddy approaches this as a <b>tabular supervised regression problem</b>: given route characteristics, carrier, cabin class, duration, distance, and booking lead time, predict the expected price distribution and identify actionable traveler decisions.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="fb-card" style="line-height: 1.6;">
            <h3 style="color: {THEME['deep_navy']}; font-weight: 800; margin-top: 0;">2. End-to-End System Architecture</h3>
            <div style="background: {THEME['background']}; border: 1px solid {THEME['border']}; border-radius: 10px; padding: 18px; font-family: monospace; font-size: 0.9rem; color: {THEME['deep_navy']}; margin: 12px 0;">
                Raw Dataset (CSV) → Preprocessing (Cleaning & Canonicalization) → Feature Engineering → Pipeline (Imputer + OHE) → Model Training (Baseline vs. RF) → Artifact Serialization (Joblib & JSON) → FlyBuddy Streamlit Dashboard
            </div>
            <p style="color: {THEME['text_muted']}; font-size: 0.88rem;">
                Model training is decoupled from the web application via <code>train_model.py</code>. Streamlit loads pre-serialized model artifacts using <code>@st.cache_resource</code> to maintain sub-second response times.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="fb-card" style="line-height: 1.6;">
            <h3 style="color: {THEME['deep_navy']}; font-weight: 800; margin-top: 0;">3. Evaluation Metrics Explained</h3>
            <ul style="color: {THEME['text_muted']}; font-size: 0.9rem; line-height: 1.7;">
                <li><b>MAE (Mean Absolute Error):</b> Measures the average rupee deviation between actual and predicted fares in natural units (₹). Less sensitive to extreme luxury outliers than RMSE.</li>
                <li><b>RMSE (Root Mean Squared Error):</b> Penalizes large pricing prediction errors more heavily.</li>
                <li><b>R² (Coefficient of Determination):</b> Measures the proportion of flight price variance explained by the model features (0.6164 for Random Forest).</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="fb-card" style="line-height: 1.6;">
            <h3 style="color: {THEME['deep_navy']}; font-weight: 800; margin-top: 0;">4. Technology Stack & Rationale</h3>
            <ul style="color: {THEME['text_muted']}; font-size: 0.9rem; line-height: 1.7;">
                <li><b>Python 3.13:</b> Core runtime for data processing and machine learning.</li>
                <li><b>Pandas & NumPy:</b> High-performance tabular manipulation, aggregation, and vector operations.</li>
                <li><b>Scikit-learn:</b> Industry standard for ColumnTransformer pipelines, Ridge regression, and Random Forest.</li>
                <li><b>Plotly:</b> Interactive, accessible vector charting answering specific traveler questions.</li>
                <li><b>Streamlit:</b> Rapid, stateful, responsive Python UI layer.</li>
                <li><b>Joblib:</b> Fast serialization for trained Scikit-learn Pipelines.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
