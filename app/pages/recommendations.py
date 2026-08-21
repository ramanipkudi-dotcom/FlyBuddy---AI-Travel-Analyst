"""
FlyBuddy - Recommendations Page
-------------------------------
Explainable flight recommendation cards sorted by value, lowest price, duration, or stops.
"""

import streamlit as st
import pandas as pd
from app.components.theme import THEME
from app.components.header import render_header
from app.components.cards import render_recommendation_card, render_kpi_card
from src.recommendation import find_recommended_flights

def render_recommendations_page(df):
    source = st.session_state.get('active_source', 'Chennai')
    dest = st.session_state.get('active_dest', 'Mumbai')
    travel_class = st.session_state.get('active_class', 'Economy')
    route_name = f"{source} → {dest}"

    render_header(
        title="Flight Recommendations",
        subtitle=f"Explainable flight recommendations on {route_name} ({travel_class}) based on historical rankings.",
        badge_text="Recommendations"
    )

    with st.container():
        st.markdown('<div class="fb-glass-card" style="padding: 16px 22px;">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            priority = st.selectbox(
                "Recommendation Priority",
                ["Best Value", "Lowest Price", "Fastest Option", "Fewest Stops"],
                index=0,
                key="rec_priority"
            )
        with col2:
            max_stops = st.selectbox(
                "Maximum Stops",
                ["Any Stops", "Direct (Non-stop)", "Up to 1 Stop"],
                index=0,
                key="rec_stops"
            )
        with col3:
            top_count = st.slider("Number of Flights", min_value=3, max_value=15, value=5, key="rec_count")

        st.markdown('</div>', unsafe_allow_html=True)

    max_stops_val = None
    if max_stops == "Direct (Non-stop)":
        max_stops_val = 0
    elif max_stops == "Up to 1 Stop":
        max_stops_val = 1

    recommended = find_recommended_flights(
        df,
        source=source,
        destination=dest,
        travel_class=travel_class,
        priority=priority,
        max_stops=max_stops_val,
        top_n=top_count
    )

    st.markdown(f"<h3 style='color: var(--fb-text-primary, #F8FAFC); font-weight: 700; font-size: 1.2rem;'>Top Ranked Itineraries ({priority})</h3>", unsafe_allow_html=True)

    if not recommended:
        st.warning("No flights matched the selected recommendation criteria. Try relaxing the stops filter.")
        return

    for flight in recommended:
        render_recommendation_card(flight)
