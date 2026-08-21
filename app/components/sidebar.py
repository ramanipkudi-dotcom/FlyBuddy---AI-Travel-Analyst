"""
FlyBuddy - Dark Glass Sidebar Component
---------------------------------------
Provides restored FlyBuddy logo, active route glass card, and clean 6-page navigation.
"""

import streamlit as st
from app.components.theme import THEME

NAV_ITEMS = [
    "Overview",
    "Price Explorer",
    "Price Factors",
    "Best Time to Book",
    "Price Forecast",
    "Recommendations"
]

def render_sidebar():
    """
    Render clean dark glass sidebar with restored FlyBuddy logo and 6 travel-focused pages.
    """
    with st.sidebar:
        # Restored FlyBuddy Logo Header
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px; padding: 2px 0;">
                <div style="width: 38px; height: 38px; border-radius: 10px; background: linear-gradient(135deg, {THEME['primary_cyan']}, {THEME['secondary_violet']}); display: flex; align-items: center; justify-content: center; color: white; font-size: 19px; font-weight: bold; box-shadow: 0 4px 16px rgba(34, 211, 238, 0.4);">
                    ✈
                </div>
                <div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: {THEME['text_primary']}; letter-spacing: -0.02em; line-height: 1.1;">
                        FlyBuddy
                    </div>
                    <div style="font-size: 0.72rem; font-weight: 600; color: {THEME['primary_cyan']}; letter-spacing: 0.06em; text-transform: uppercase;">
                        Travel Analyst
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Active Route Card
        active_route = st.session_state.get('active_route', None)
        active_class = st.session_state.get('active_class', 'Economy')
        
        if active_route:
            st.markdown(
                f"""
                <div style="background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(34, 211, 238, 0.2); border-radius: 12px; padding: 12px 14px; margin-bottom: 20px; box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);">
                    <div style="font-size: 0.68rem; font-weight: 700; color: {THEME['primary_cyan']}; text-transform: uppercase; letter-spacing: 0.05em;">
                        Active Route
                    </div>
                    <div style="font-size: 0.95rem; font-weight: 700; color: {THEME['text_primary']}; margin-top: 2px;">
                        {active_route}
                    </div>
                    <div style="font-size: 0.76rem; color: {THEME['text_secondary']}; margin-top: 1px;">
                        Class: {active_class}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Navigation Label
        st.markdown(
            f"<div style='font-size: 0.7rem; font-weight: 700; color: {THEME['text_secondary']}; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px;'>Navigation</div>",
            unsafe_allow_html=True
        )

        current_page = st.session_state.get('current_page', 'Overview')
        if current_page not in NAV_ITEMS:
            current_page = 'Overview'

        current_idx = NAV_ITEMS.index(current_page) if current_page in NAV_ITEMS else 0

        selected_page = st.radio(
            label="Navigation Menu",
            options=NAV_ITEMS,
            index=current_idx,
            label_visibility="collapsed"
        )

        st.session_state['current_page'] = selected_page

        # Quick Action: Change Trip
        st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
        if st.button("Change Trip", use_container_width=True):
            st.session_state['has_searched'] = False
            st.session_state['current_page'] = 'Overview'
            st.rerun()

        # Tagline Footer
        st.markdown(
            f"""
            <div style="margin-top: 32px; padding-top: 16px; border-top: 1px solid {THEME['border_subtle']};">
                <div style="font-size: 0.78rem; color: {THEME['text_secondary']};">
                    "Travel smarter, not harder."
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    return selected_page
