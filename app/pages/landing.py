"""
FlyBuddy - Landing Page
-----------------------
Dribbble Reference Composition:
Spacious hero layout, top navigation, large stacked headline on left,
subtle stats chip, and clean flight search form card on right.
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
    # Initialize keys if missing
    if 'sel_source_box' not in st.session_state:
        st.session_state['sel_source_box'] = st.session_state.get('active_source', 'Chennai')
    if 'sel_dest_box' not in st.session_state:
        st.session_state['sel_dest_box'] = st.session_state.get('active_dest', 'Mumbai')

    # --- Top Navigation Bar inside Hero Container ---
    nav_col1, nav_col2 = st.columns([1.5, 2.5])
    with nav_col1:
        st.markdown(
            f'''<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 24px;">
<div style="width: 38px; height: 38px; border-radius: 10px; background: linear-gradient(135deg, {THEME['primary_cyan']}, {THEME['secondary_violet']}); display: flex; align-items: center; justify-content: center; color: white; font-size: 19px; font-weight: bold; box-shadow: 0 4px 14px rgba(34, 211, 238, 0.4);">✈</div>
<div>
<div style="font-size: 1.3rem; font-weight: 800; color: {THEME['text_primary']}; letter-spacing: -0.02em; line-height: 1.1;">FlyBuddy</div>
<div style="font-size: 0.68rem; font-weight: 600; color: {THEME['primary_cyan']}; letter-spacing: 0.08em; text-transform: uppercase;">TRAVEL ANALYST</div>
</div>
</div>''',
            unsafe_allow_html=True
        )
    with nav_col2:
        st.markdown(
            f'''<div style="display: flex; justify-content: flex-end; align-items: center; gap: 20px; padding-top: 6px;">
<span style="font-size: 0.85rem; color: {THEME['text_secondary']}; font-weight: 500;">Historical Fares</span>
<span style="font-size: 0.85rem; color: {THEME['text_secondary']}; font-weight: 500;">Price Drivers</span>
<span style="font-size: 0.85rem; color: {THEME['text_secondary']}; font-weight: 500;">Booking Windows</span>
<span style="background: rgba(34, 211, 238, 0.15); border: 1px solid rgba(34, 211, 238, 0.3); padding: 4px 12px; border-radius: 9999px; font-size: 0.76rem; font-weight: 700; color: {THEME['primary_cyan']};">100K+ FLIGHTS</span>
</div>''',
            unsafe_allow_html=True
        )

    # --- Main Hero Composition (Left: Headline & Narrative, Right: Clean Flight Form Card) ---
    col_left, col_right = st.columns([1.18, 0.82])

    with col_left:
        st.markdown(
            f'''<div style="padding: 10px 20px 10px 4px;">
<div style="font-size: 3.8rem; font-weight: 900; color: {THEME['text_primary']}; line-height: 1.08; letter-spacing: -0.035em;">
Plan Your<br>
<span style="color: {THEME['primary_cyan']}; text-shadow: 0 0 35px rgba(34, 211, 238, 0.4);">Smartest</span><br>
Flight Route.
</div>
<p style="font-size: 1.08rem; color: {THEME['text_secondary']}; line-height: 1.6; margin-top: 20px; max-width: 480px;">
Explore historical flight prices across 100,000+ flight records, discover optimal booking windows, and understand what drives your fare.
</p>
<div style="margin-top: 24px; display: inline-flex; align-items: center; gap: 8px; background: rgba(15, 23, 42, 0.55); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 8px 14px;">
<span style="color: {THEME['primary_cyan']}; font-size: 0.85rem; font-weight: 700;">100,000+</span>
<span style="color: {THEME['text_secondary']}; font-size: 0.8rem;">flights analyzed across 18 major routes</span>
</div>
</div>''',
            unsafe_allow_html=True
        )

    with col_right:
        st.markdown('<div class="fb-floating-card">', unsafe_allow_html=True)
        
        # Row 1: Balanced Origin & Destination
        col_from, col_to = st.columns(2)
        with col_from:
            source_city = st.selectbox("Origin", CITIES, key="sel_source_box")
        with col_to:
            dest_city = st.selectbox("Destination", CITIES, key="sel_dest_box")

        # Row 2: Class, Date, Passengers
        col_class, col_date, col_passengers = st.columns(3)
        with col_class:
            travel_class = st.selectbox("Class", CLASSES, index=0, key="input_class")
        with col_date:
            travel_date = st.date_input("Date", key="input_date")
        with col_passengers:
            passengers = st.number_input("Guests", min_value=1, max_value=9, value=1, step=1, key="input_passengers")

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

        # Row 3: Primary Animated CTA Button (Single Click)
        if st.button("✦ Analyze My Trip", use_container_width=True):
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
                st.session_state['current_page'] = 'Overview'
                st.session_state['nav_radio_selection'] = 'Overview'
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
