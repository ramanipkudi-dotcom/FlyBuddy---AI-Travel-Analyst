"""
FlyBuddy - Price Factors Page ("What Drives Flight Prices?")
------------------------------------------------------------
Deep dive into feature importance, correlations, and category drivers for interview defense.
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
        title="What Drives Flight Prices?",
        subtitle="Analytical breakdown of the primary factors influencing airfares based on EDA and Machine Learning.",
        badge_text="⚡ Price Drivers"
    )

    top_importances = metrics.get('top_feature_importances', [])
    if top_importances:
        st.markdown('<div class="fb-card">', unsafe_allow_html=True)
        fig_imp = plot_feature_importance(top_importances, title="Relative Feature Importance (Random Forest Regressor)")
        st.plotly_chart(fig_imp, use_container_width=True)
        st.markdown(
            f"""
            <div style="font-size: 0.84rem; color: {THEME['text_muted']}; line-height: 1.5;">
                <b>How this is calculated:</b> Feature importance is derived from the Mean Decrease in Impurity across 50 decision trees in the Random Forest Regressor. It measures how much each feature contributes to reducing prediction variance.
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"<h3 style='color: {THEME['deep_navy']}; font-weight: 800; font-size: 1.25rem;'>🔍 Key Driver Analysis</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        render_insight_card(
            icon="⏱",
            title="1. Flight Duration (~44.6% Importance)",
            explanation="Duration is the strongest single predictor of airfare. Long-haul flights consume significantly more fuel, require larger aircraft types, and incur higher crew/route operating expenses.",
            badge_text="Top Driver",
            badge_type="good"
        )
        render_insight_card(
            icon="💺",
            title="3. Travel Class (~10.8% Importance)",
            explanation="Airlines use price discrimination across cabin classes. Premium cabins consume more floor space per passenger and include luxury amenities, creating distinct price multipliers.",
            badge_text="High Impact",
            badge_type="typical"
        )
        render_insight_card(
            icon="✈",
            title="5. Operating Airline (~4.4% Importance)",
            explanation="Different airlines operate on low-cost vs full-service business models, creating baseline price differentials across identical routes.",
            badge_text="Market Tier",
            badge_type="typical"
        )

    with col2:
        render_insight_card(
            icon="📍",
            title="2. Flight Distance (~17.0% Importance)",
            explanation="Distance tightly couples with duration and airport fee structures, forming the fundamental baseline for airline seat-mile revenue management.",
            badge_text="Major Factor",
            badge_type="good"
        )
        render_insight_card(
            icon="📅",
            title="4. Days Before Departure (~5.9% Importance)",
            explanation="Yield management algorithms increase prices exponentially as departure approaches to capture inelastic demand from business and emergency travelers.",
            badge_text="Dynamic Factor",
            badge_type="typical"
        )
        render_insight_card(
            icon="🛑",
            title="6. Total Stops & Route (~5.8% Importance)",
            explanation="Route topology and intermediate layovers determine both aircraft utilization efficiency and passenger convenience premiums.",
            badge_text="Routing Factor",
            badge_type="typical"
        )

    st.markdown('<div class="fb-card" style="margin-top: 14px;">', unsafe_allow_html=True)
    st.markdown(f"<h4 style='color: {THEME['deep_navy']}; font-weight: 700; margin-bottom: 12px;'>Median Price by Season & Weekday (₹)</h4>", unsafe_allow_html=True)
    
    pivot_df = df.pivot_table(index='Weekday', columns='Season', values='Price_clean', aggfunc='median')
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_df = pivot_df.reindex([d for d in days_order if d in pivot_df.index])

    fig_heat = px.imshow(
        pivot_df,
        labels=dict(x="Season", y="Weekday", color="Median Price (₹)"),
        x=pivot_df.columns,
        y=pivot_df.index,
        color_continuous_scale=[[0, THEME['primary_light']], [0.5, THEME['primary_cyan']], [1, THEME['deep_navy']]],
        text_auto='.0f'
    )
    fig_heat.update_layout(get_base_layout(height=340))
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
