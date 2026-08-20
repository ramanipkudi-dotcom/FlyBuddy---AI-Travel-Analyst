"""
FlyBuddy - Flight Price Forecast Page (Stretch / Future Feature)
---------------------------------------------------------------
Provides the clean UI and architecture placeholder for future time-series forecasting.
"""

import streamlit as st
from app.components.theme import THEME
from app.components.header import render_header
from app.components.cards import render_insight_card

def render_forecast_page():
    render_header(
        title="Flight Price Forecast",
        subtitle="Anticipate upcoming fare trends using time-series and seasonal modeling.",
        badge_text="📈 Coming Next"
    )

    st.markdown(
        f"""
        <div class="fb-card" style="text-align: center; padding: 48px 32px;">
            <div style="width: 60px; height: 60px; border-radius: 16px; background: {THEME['primary_light']}; display: flex; align-items: center; justify-content: center; margin: 0 auto 16px auto; font-size: 28px;">
                📈
            </div>
            <h2 style="font-size: 1.6rem; font-weight: 800; color: {THEME['deep_navy']}; margin-bottom: 8px;">
                Flight Price Forecasting Engine
            </h2>
            <p style="font-size: 0.98rem; color: {THEME['text_muted']}; max-width: 620px; margin: 0 auto 24px auto; line-height: 1.6;">
                The forecasting module will integrate autoregressive time-series modeling (e.g. ARIMA / Prophet / LightGBM lag features) to forecast future date-specific price fluctuations based on macro seasonality and historical lead times.
            </p>
            <span class="fb-badge fb-badge-typical" style="padding: 6px 16px; font-size: 0.85rem;">
                Architecture Prepared • Module Planned for Next Phase
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"<h3 style='color: {THEME['deep_navy']}; font-weight: 800; font-size: 1.25rem; margin-top: 24px;'>🏗️ Planned Forecasting Architecture</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        render_insight_card(
            icon="📅",
            title="Temporal Feature Extraction",
            explanation="Will extract day-of-year, seasonal quarter, holiday calendar proximity, and cyclical sin/cos encodings for smooth time continuity.",
            badge_text="Feature Pipeline",
            badge_type="typical"
        )
    with col2:
        render_insight_card(
            icon="📊",
            title="Confidence Intervals",
            explanation="Predictions will include 80% and 95% uncertainty intervals so travelers can assess price volatility risks.",
            badge_text="Probabilistic",
            badge_type="typical"
        )
