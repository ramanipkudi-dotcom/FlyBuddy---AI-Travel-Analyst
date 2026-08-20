"""
FlyBuddy - Flight Recommendations Page
--------------------------------------
Filterable flight finder with transparent, explainable reason chips.
"""

import streamlit as st
import pandas as pd
from app.components.theme import THEME
from app.components.header import render_header
from app.components.cards import render_recommendation_card
from src.recommendation import find_recommended_flights

def render_recommendations_page(df):
    render_header(
        title="Find Your Best Flight",
        subtitle="Personalized recommendations ranked by your travel priorities with transparent explanations.",
        badge_text="✨ Smart Ranking"
    )

    with st.container():
        st.markdown('<div class="fb-card" style="padding: 16px 20px;">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        sources = sorted([str(x) for x in df['Source'].dropna().unique()])
        dests = sorted([str(x) for x in df['Destination'].dropna().unique()])
        classes = ['Economy', 'Premium Economy', 'Business', 'First']
        priorities = ['Best Value', 'Cheapest', 'Fastest', 'Fewest Stops']

        default_from_idx = sources.index(st.session_state.get('active_source', 'Chennai')) if st.session_state.get('active_source', 'Chennai') in sources else 0
        default_to_idx = dests.index(st.session_state.get('active_dest', 'Mumbai')) if st.session_state.get('active_dest', 'Mumbai') in dests else 0

        with col1:
            sel_src = st.selectbox("Origin", sources, index=default_from_idx, key="rec_src")
        with col2:
            sel_dst = st.selectbox("Destination", dests, index=default_to_idx, key="rec_dst")
        with col3:
            sel_class = st.selectbox("Travel Class", classes, index=0, key="rec_class")
        with col4:
            sel_prio = st.selectbox("Priority Ranking", priorities, index=0, key="rec_prio")

        st.markdown('</div>', unsafe_allow_html=True)

    recs = find_recommended_flights(df, source=sel_src, destination=sel_dst, travel_class=sel_class, priority=sel_prio, top_n=6)

    st.markdown(f"<h3 style='color: {THEME['deep_navy']}; font-weight: 800; font-size: 1.25rem; margin-top: 10px;'>✈ Recommended Options ({sel_src} → {sel_dst})</h3>", unsafe_allow_html=True)

    if not recs:
        st.info("No matching flights found for this specific route and filter criteria.")
    else:
        for flight in recs:
            render_recommendation_card(flight)
