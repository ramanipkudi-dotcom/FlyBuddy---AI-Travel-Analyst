"""
FlyBuddy - Landing Page ("Where are you flying?")
-------------------------------------------------
First user touchpoint: clean, travel-focused trip configuration screen.
"""

import streamlit as st
from app.components.theme import THEME

CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad",
    "Pune", "Ahmedabad", "Jaipur", "Goa", "Dubai", "Singapore",
    "Bangkok", "Doha", "London", "Frankfurt", "New York", "Sydney"
]

CLASSES = ["Economy", "Premium Economy", "Business", "First"]

def render_landing_page():
    st.markdown(
        f"""
        <div style="text-align: center; max-width: 780px; margin: 20px auto 32px auto;">
            <div style="display: inline-block; padding: 6px 14px; background: {THEME['primary_light']}; border: 1px solid rgba(18, 184, 212, 0.3); border-radius: 24px; font-size: 0.82rem; font-weight: 700; color: {THEME['primary_cyan']}; margin-bottom: 12px;">
                ✈ AI-POWERED FLIGHT INTELLIGENCE
            </div>
            <h1 style="font-size: 2.8rem; font-weight: 800; color: {THEME['deep_navy']}; line-height: 1.15; letter-spacing: -0.03em;">
                Where are you flying?
            </h1>
            <p style="font-size: 1.1rem; color: {THEME['text_muted']}; margin-top: 10px; line-height: 1.5;">
                Tell FlyBuddy your route. We will analyze real historical flight pricing, uncover cost drivers, and find the smartest booking windows for you.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        st.markdown(f'<div class="fb-hero-card">', unsafe_allow_html=True)
        
        col_from, col_swap, col_to = st.columns([5, 1, 5])
        
        default_from_idx = CITIES.index(st.session_state.get('search_source', 'Chennai')) if st.session_state.get('search_source', 'Chennai') in CITIES else 3
        default_to_idx = CITIES.index(st.session_state.get('search_dest', 'Mumbai')) if st.session_state.get('search_dest', 'Mumbai') in CITIES else 0

        with col_from:
            source_city = st.selectbox("From (Origin)", CITIES, index=default_from_idx, key="input_source")
        
        with col_swap:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("⇄", help="Swap departure and destination"):
                st.session_state['search_source'] = default_to_idx
                st.session_state['search_dest'] = default_from_idx
                st.rerun()

        with col_to:
            dest_city = st.selectbox("To (Destination)", CITIES, index=default_to_idx, key="input_dest")

        col_class, col_date, col_passengers = st.columns(3)
        with col_class:
            travel_class = st.selectbox("Travel Class", CLASSES, index=0, key="input_class")
        with col_date:
            travel_date = st.date_input("Target Departure Date", key="input_date")
        with col_passengers:
            passengers = st.number_input("Passengers", min_value=1, max_value=9, value=1, step=1, key="input_passengers")

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        
        col_cta1, col_cta2, col_cta3 = st.columns([1, 2, 1])
        with col_cta2:
            if st.button("🚀 Analyze My Trip", use_container_width=True):
                if source_city == dest_city:
                    st.warning("Origin and Destination cannot be the same. Please choose different cities.")
                else:
                    st.session_state['active_source'] = source_city
                    st.session_state['active_dest'] = dest_city
                    st.session_state['active_route'] = f"{source_city} → {dest_city}"
                    st.session_state['active_class'] = travel_class
                    st.session_state['active_passengers'] = passengers
                    st.session_state['active_date'] = str(travel_date)
                    st.session_state['has_searched'] = True
                    st.session_state['show_loading'] = True
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-top: 24px;">
            <div class="fb-card" style="text-align: center; padding: 20px;">
                <div style="font-size: 1.8rem; margin-bottom: 8px;">📊</div>
                <div style="font-weight: 700; color: {THEME['deep_navy']};">Empirical Distributions</div>
                <div style="font-size: 0.82rem; color: {THEME['text_muted']}; margin-top: 4px;">100,000 real flight prices analyzed across routes and airlines.</div>
            </div>
            <div class="fb-card" style="text-align: center; padding: 20px;">
                <div style="font-size: 1.8rem; margin-bottom: 8px;">🧠</div>
                <div style="font-weight: 700; color: {THEME['deep_navy']};">Machine Learning Model</div>
                <div style="font-size: 0.82rem; color: {THEME['text_muted']}; margin-top: 4px;">Trained Random Forest capturing non-linear pricing dynamics.</div>
            </div>
            <div class="fb-card" style="text-align: center; padding: 20px;">
                <div style="font-size: 1.8rem; margin-bottom: 8px;">📅</div>
                <div style="font-weight: 700; color: {THEME['deep_navy']};">Optimal Lead Times</div>
                <div style="font-size: 0.82rem; color: {THEME['text_muted']}; margin-top: 4px;">Data-driven booking windows based on historical trends.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
