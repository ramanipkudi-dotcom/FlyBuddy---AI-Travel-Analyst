"""
FlyBuddy - About Page ("How FlyBuddy Works")
--------------------------------------------
Explains data sources, methodology, feature calculations, and chart interpretations.
"""

import streamlit as st
from app.components.theme import THEME
from app.components.header import render_header

def render_about_page():
    render_header(
        title="How FlyBuddy Works",
        subtitle="Understand how your flight insights are calculated from historical flight data.",
        badge_text="Methodology & Guide"
    )

    st.markdown(
        f"""
        <div class="fb-glass-card">
            <div style="font-size: 0.78rem; font-weight: 700; color: {THEME['primary_cyan']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
                1. Historical Dataset
            </div>
            <div style="font-size: 1.25rem; font-weight: 800; color: var(--fb-text-primary, #F8FAFC); margin-bottom: 8px;">
                Comprehensive Historical Flight Records
            </div>
            <p style="font-size: 0.92rem; color: var(--fb-text-secondary, #94A3B8); line-height: 1.6; margin-bottom: 12px;">
                FlyBuddy analyzes approximately <b>100,000 authentic flight observations</b> across 18 major domestic and international hubs. Each record captures key journey attributes including operating airline, origin, destination, cabin tier, stop count, journey duration, flight distance, booking lead time, seasonal indicators, day of week, and fare.
            </p>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                <span class="fb-badge fb-badge-typical">100K+ Observations</span>
                <span class="fb-badge fb-badge-typical">18 Major Airports</span>
                <span class="fb-badge fb-badge-typical">Empirical Fare Distributions</span>
                <span class="fb-badge fb-badge-typical">Filtered by Selected Trip</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div class="fb-glass-card" style="height: 100%;">
                <div style="font-size: 0.78rem; font-weight: 700; color: {THEME['primary_cyan']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
                    2. Route Overview
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: var(--fb-text-primary, #F8FAFC); margin-bottom: 8px;">
                    Dynamic Route Indicators
                </div>
                <p style="font-size: 0.88rem; color: var(--fb-text-secondary, #94A3B8); line-height: 1.55;">
                    The Overview page filters the master dataset to the user's specific Origin, Destination, and Travel Class. Summary indicators (<b>Typical Fare</b> as median, <b>Lowest Observed Fare</b> as min, and <b>Flights Analyzed</b>) are computed dynamically from actual matching records rather than hardcoded approximations.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="fb-glass-card" style="height: 100%;">
                <div style="font-size: 0.78rem; font-weight: 700; color: {THEME['primary_cyan']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
                    3. Price Explorer
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: var(--fb-text-primary, #F8FAFC); margin-bottom: 8px;">
                    Multi-Attribute Filtering
                </div>
                <p style="font-size: 0.88rem; color: var(--fb-text-secondary, #94A3B8); line-height: 1.55;">
                    Price Explorer lets users slice historical flight data across carriers, cabin classes, stop categories, seasons, and booking channels. Charts recalculate reactively upon filter changes to reveal price density, airline differentials, and lead-time patterns.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown(
            f"""
            <div class="fb-glass-card" style="height: 100%;">
                <div style="font-size: 0.78rem; font-weight: 700; color: {THEME['primary_cyan']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
                    4. Price Factors
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: var(--fb-text-primary, #F8FAFC); margin-bottom: 8px;">
                    Fare Associations & Drivers
                </div>
                <p style="font-size: 0.88rem; color: var(--fb-text-secondary, #94A3B8); line-height: 1.55;">
                    Examines factors associated with fare variance. Flight duration and route distance establish baseline operating costs (~61.6% combined relative importance), while cabin class, booking lead time, operating airline, and stops create tier multipliers.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="fb-glass-card" style="height: 100%;">
                <div style="font-size: 0.78rem; font-weight: 700; color: {THEME['primary_cyan']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
                    5. Best Time to Book
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: var(--fb-text-primary, #F8FAFC); margin-bottom: 8px;">
                    Empirical Lead-Time Windows
                </div>
                <p style="font-size: 0.88rem; color: var(--fb-text-secondary, #94A3B8); line-height: 1.55;">
                    Flights are grouped into empirical booking lead-time bins (0–7d, 8–14d, 15–21d, 22–35d, 36–50d, 50d+). The recommended booking window is derived purely from the lowest median fare observed in the historical dataset for that specific route and class.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        st.markdown(
            f"""
            <div class="fb-glass-card" style="height: 100%;">
                <div style="font-size: 0.78rem; font-weight: 700; color: {THEME['primary_cyan']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
                    6. Price Forecast
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: var(--fb-text-primary, #F8FAFC); margin-bottom: 8px;">
                    Machine Learning Fare Estimation
                </div>
                <p style="font-size: 0.88rem; color: var(--fb-text-secondary, #94A3B8); line-height: 1.55;">
                    Uses a trained machine learning regression pipeline to estimate expected fares based on selected airline, class, stops, season, weekday, and advance days. Provides an expected price range based on model error margins (MAE) and generates a 1–60 day advance price trend curve.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col6:
        st.markdown(
            f"""
            <div class="fb-glass-card" style="height: 100%;">
                <div style="font-size: 0.78rem; font-weight: 700; color: {THEME['primary_cyan']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
                    7. Recommendations
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: var(--fb-text-primary, #F8FAFC); margin-bottom: 8px;">
                    Explainable Flight Rankings
                </div>
                <p style="font-size: 0.88rem; color: var(--fb-text-secondary, #94A3B8); line-height: 1.55;">
                    Rankings prioritize flights across <b>Best Value</b> (composite score balancing price, duration, and stops), <b>Lowest Price</b>, <b>Fastest Option</b>, and <b>Fewest Stops</b> with clear reason tags explaining why each flight was ranked.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class="fb-glass-card" style="margin-top: 14px;">
            <div style="font-size: 0.78rem; font-weight: 700; color: {THEME['primary_cyan']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
                8. How to Read Visualizations
            </div>
            <div style="font-size: 1.2rem; font-weight: 800; color: var(--fb-text-primary, #F8FAFC); margin-bottom: 8px;">
                Targeted Visual Insights
            </div>
            <p style="font-size: 0.9rem; color: var(--fb-text-secondary, #94A3B8); line-height: 1.55;">
                Every graph is designed to answer a specific traveler question. Look for the single-line <b>“What this shows:”</b> takeaway underneath each chart for concise interpretations regarding booking windows, carrier models, seat category premiums, and seasonal demand.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="padding: 14px 18px; border-radius: 12px; background: var(--fb-glass-card, rgba(15, 23, 42, 0.45)); border: 1px solid var(--fb-border-subtle, rgba(255, 255, 255, 0.08)); margin-top: 16px; text-align: center;">
            <span style="font-size: 0.82rem; color: var(--fb-text-secondary, #94A3B8);">
                <b>Analytical Notice:</b> FlyBuddy's insights and fare estimates are derived from historical flight pricing distributions and should be treated as analytical guidance rather than a financial guarantee of future fares.
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )
