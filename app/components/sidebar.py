"""
FlyBuddy - Dark Glass Sidebar Component
---------------------------------------
Provides restored FlyBuddy logo, active route glass card, single-click clean text navigation,
and About page.
"""

import streamlit as st
from app.components.theme import THEME

NAV_ITEMS = [
    "Overview",
    "Price Explorer",
    "Price Factors",
    "Best Time to Book",
    "Price Forecast",
    "Recommendations",
    "About"
]

def render_sidebar():
    """
    Render clean dark glass sidebar with restored FlyBuddy logo and 7 travel-focused pages.
    """
    with st.sidebar:
        # FlyBuddy Logo Header (Enlarged, prominent, and positioned near top)
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 18px; padding: 0 0 2px 0;">
                <div style="width: 42px; height: 42px; border-radius: 11px; background: linear-gradient(135deg, {THEME['primary_cyan']}, {THEME['secondary_violet']}); display: flex; align-items: center; justify-content: center; color: white; font-size: 21px; font-weight: bold; box-shadow: 0 4px 16px rgba(34, 211, 238, 0.45);">
                    ✈
                </div>
                <div>
                    <div style="font-size: 1.45rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.02em; line-height: 1.1;">
                        FLYBUDDY
                    </div>
                    <div style="font-size: 0.72rem; font-weight: 700; color: {THEME['primary_cyan']}; letter-spacing: 0.08em; text-transform: uppercase;">
                        TRAVEL ANALYST
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
                <div style="background: rgba(10, 25, 50, 0.65); backdrop-filter: blur(16px); border: 1px solid rgba(120, 210, 255, 0.22); border-top: 1px solid rgba(255, 255, 255, 0.25); border-radius: 14px; padding: 12px 15px; margin-bottom: 16px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);">
                    <div style="font-size: 0.68rem; font-weight: 700; color: {THEME['primary_cyan']}; text-transform: uppercase; letter-spacing: 0.06em;">
                        Active Route
                    </div>
                    <div style="font-size: 0.96rem; font-weight: 700; color: #F8FAFC; margin-top: 2px;">
                        {active_route}
                    </div>
                    <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 1px;">
                        Class: {active_class}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Navigation Label
        st.markdown(
            f"<div style='font-size: 0.7rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px;'>Navigation</div>",
            unsafe_allow_html=True
        )

        # Single-Click Navigation Sync Callback
        if 'nav_radio_selection' not in st.session_state:
            st.session_state['nav_radio_selection'] = st.session_state.get('current_page', 'Overview')

        def on_nav_change():
            st.session_state['current_page'] = st.session_state['nav_radio_selection']

        # Clean text navigation items (Zero emojis/symbols)
        selected_page = st.radio(
            label="Navigation Menu",
            options=NAV_ITEMS,
            label_visibility="collapsed",
            key="nav_radio_selection",
            on_change=on_nav_change
        )

        st.session_state['current_page'] = selected_page

        # Quick Action: Change Trip (Single Click)
        st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
        def reset_to_landing():
            st.session_state['has_searched'] = False
            st.session_state['current_page'] = 'Overview'
            st.session_state['nav_radio_selection'] = 'Overview'

        st.button("Change Trip", use_container_width=True, on_click=reset_to_landing)

        # Tagline Footer
        st.markdown(
            f"""
            <div style="margin-top: 24px; padding-top: 12px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                <div style="font-size: 0.78rem; color: #94A3B8;">
                    "Travel smarter, not harder."
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    return selected_page
