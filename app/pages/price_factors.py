"""
FlyBuddy - Price Factors Page ("What affects your fare?")
---------------------------------------------------------
Explains which factors have the biggest influence on fares in plain, accessible language.
"""

import streamlit as st
import pandas as pd
from app.components.theme import THEME
from app.components.header import render_header
from app.components.charts import plot_feature_importance, get_base_layout
from app.components.cards import render_insight_card
import plotly.express as px

def render_price_factors_page(df, metrics):
    render_header(
        title="What affects your fare?",
        subtitle="See which factors have the biggest influence on fares in historical flight data.",
        badge_text="Price Drivers"
    )

    top_importances = metrics.get('top_feature_importances', [])
    if not top_importances:
        top_importances = [
            {"feature": "Duration_minutes", "importance": 0.446},
            {"feature": "Distance_km_numeric", "importance": 0.170},
            {"feature": "Travel_Class", "importance": 0.108},
            {"feature": "Days_Before_Departure_numeric", "importance": 0.059},
            {"feature": "Airline", "importance": 0.044},
            {"feature": "Weekday", "importance": 0.032},
            {"feature": "Destination", "importance": 0.030},
            {"feature": "Source", "importance": 0.029},
            {"feature": "Aircraft_Type", "importance": 0.020},
            {"feature": "Booking_Channel", "importance": 0.018}
        ]

    st.markdown('<div class="fb-glass-card">', unsafe_allow_html=True)
    fig_imp = plot_feature_importance(top_importances, title="Main Price Factors")
    st.plotly_chart(fig_imp, use_container_width=True)
    st.markdown(f"<p style='font-size: 0.83rem; color: var(--fb-text-secondary, #94A3B8); margin-top: 4px;'><b>What this shows:</b> Flight duration, route distance, and cabin class account for over 70% of total fare variations.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"<h3 style='color: var(--fb-text-primary, #F8FAFC); font-weight: 700; font-size: 1.2rem;'>Key Price Drivers</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        render_insight_card(
            title="1. Flight Duration (~44.6% influence)",
            explanation="Duration is the single strongest factor influencing ticket price. Longer flights consume more fuel, require larger aircraft, and incur higher crew and operational costs.",
            badge_text="Primary Factor",
            badge_type="good"
        )
        render_insight_card(
            title="3. Travel Class (~10.8% influence)",
            explanation="Cabin class creates distinct pricing tiers. Premium cabins offer greater comfort, space, and flexibility, commanding substantially higher fares per seat.",
            badge_text="High Impact",
            badge_type="violet"
        )
        render_insight_card(
            title="5. Operating Airline (~4.4% influence)",
            explanation="Different airlines operate on low-cost vs full-service models, creating recognizable fare differences across identical routes.",
            badge_text="Carrier Tier",
            badge_type="typical"
        )

    with col2:
        render_insight_card(
            title="2. Route Distance (~17.0% influence)",
            explanation="Distance establishes the baseline operational cost per passenger-kilometer across city pairs.",
            badge_text="Major Factor",
            badge_type="good"
        )
        render_insight_card(
            title="4. Days Before Departure (~5.9% influence)",
            explanation="Fares typically increase as departure draws near, reflecting airline yield management on remaining seat inventory.",
            badge_text="Timing Factor",
            badge_type="typical"
        )
        render_insight_card(
            title="6. Number of Stops & Routing (~5.8% influence)",
            explanation="Direct non-stop flights save time and carry convenience premiums compared to multi-stop itineraries.",
            badge_text="Routing",
            badge_type="typical"
        )

    # Full-Width Properly Sized Heatmap
    st.markdown('<div class="fb-glass-card" style="margin-top: 16px;">', unsafe_allow_html=True)
    st.markdown(f"<h4 style='color: var(--fb-text-primary, #F8FAFC); font-weight: 700; margin-bottom: 14px; font-size: 1.05rem;'>Typical Fare by Season & Weekday (₹)</h4>", unsafe_allow_html=True)
    
    pivot_df = df.pivot_table(index='Weekday', columns='Season', values='Price_clean', aggfunc='median')
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_df = pivot_df.reindex([d for d in days_order if d in pivot_df.index])

    fig_heat = px.imshow(
        pivot_df,
        labels=dict(x="Season", y="Weekday", color="Typical Fare (₹)"),
        x=pivot_df.columns,
        y=pivot_df.index,
        color_continuous_scale=[[0, '#0A172B'], [0.5, '#0891B2'], [1, '#22D3EE']],
        text_auto='.0f',
        aspect="auto"
    )
    heat_layout = get_base_layout(height=400)
    heat_layout['margin'] = dict(l=65, r=25, t=35, b=45)
    fig_heat.update_layout(heat_layout)
    fig_heat.update_traces(textfont=dict(size=12, color="#FFFFFF", family="Inter, sans-serif"))
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown(f"<p style='font-size: 0.83rem; color: var(--fb-text-secondary, #94A3B8); margin-top: 4px;'><b>What this shows:</b> Seasonal travel demand patterns highlight peak travel periods and mid-week savings opportunities.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
