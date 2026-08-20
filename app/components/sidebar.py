"""
FlyBuddy - Persistent Left Sidebar Component
--------------------------------------------
Renders the left navigation panel with FlyBuddy branding, route badge,
and grouped navigation sections.
"""

import streamlit as st
from app.components.theme import THEME

NAV_ITEMS = [
    {"id": "Overview", "label": "Overview", "icon": "📊", "section": "TRIP"},
    {"id": "Price Explorer", "label": "Price Explorer", "icon": "🔍", "section": "ANALYZE"},
    {"id": "Price Factors", "label": "Price Factors", "icon": "⚡", "section": "ANALYZE"},
    {"id": "Best Time to Book", "label": "Best Time to Book", "icon": "📅", "section": "ANALYZE"},
    {"id": "Price Forecast", "label": "Price Forecast", "icon": "📈", "section": "ANALYZE"},
    {"id": "Recommendations", "label": "Recommendations", "icon": "✨", "section": "ANALYZE"},
    {"id": "Model Insights", "label": "Model Insights", "icon": "🧠", "section": "MODEL"},
    {"id": "Data Quality", "label": "Data Quality", "icon": "🛡️", "section": "DATA"},
    {"id": "Methodology", "label": "Methodology", "icon": "📖", "section": "INFO"}
]

def render_sidebar():
    """
    Render persistent sidebar navigation. Returns currently selected page string.
    """
    with st.sidebar:
        # Brand Header & Logo
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 16px; padding: 4px 0;">
                <div style="width: 38px; height: 38px; border-radius: 10px; background: linear-gradient(135deg, {THEME['primary_cyan']}, {THEME['secondary_blue']}); display: flex; align-items: center; justify-content: center; color: white; font-size: 20px; font-weight: bold; box-shadow: 0 3px 8px rgba(18, 184, 212, 0.3);">
                    ✈
                </div>
                <div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: {THEME['deep_navy']}; line-height: 1.1;">
                        FlyBuddy
                    </div>
                    <div style="font-size: 0.72rem; font-weight: 600; color: {THEME['primary_cyan']}; letter-spacing: 0.04em;">
                        AI TRAVEL ANALYST
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Active Trip Status Pill
        active_route = st.session_state.get('active_route', None)
        active_class = st.session_state.get('active_class', 'Economy')
        
        if active_route:
            st.markdown(
                f"""
                <div style="background: {THEME['primary_light']}; border: 1px solid rgba(18, 184, 212, 0.3); border-radius: 10px; padding: 10px 12px; margin-bottom: 20px;">
                    <div style="font-size: 0.7rem; font-weight: 700; color: {THEME['primary_cyan']}; text-transform: uppercase;">
                        Active Route
                    </div>
                    <div style="font-size: 0.88rem; font-weight: 700; color: {THEME['deep_navy']}; margin-top: 2px;">
                        ✈ {active_route}
                    </div>
                    <div style="font-size: 0.75rem; color: {THEME['text_muted']}; margin-top: 1px;">
                        Class: {active_class}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Navigation Options
        st.markdown(f"<div style='font-size: 0.72rem; font-weight: 700; color: {THEME['text_muted']}; text-transform: uppercase; margin-bottom: 8px;'>Navigation</div>", unsafe_allow_html=True)

        current_page = st.session_state.get('current_page', 'Overview')
        page_labels = [f"{item['icon']}  {item['label']}" for item in NAV_ITEMS]
        
        # Find index of current page
        current_idx = 0
        for i, item in enumerate(NAV_ITEMS):
            if item['id'] == current_page:
                current_idx = i
                break

        selected_label = st.radio(
            label="Menu",
            options=page_labels,
            index=current_idx,
            label_visibility="collapsed"
        )

        selected_id = NAV_ITEMS[page_labels.index(selected_label)]['id']
        st.session_state['current_page'] = selected_id

        # Switch Route Quick Action
        st.markdown("---")
        if st.button("🔄 Change Trip / Route", use_container_width=True):
            st.session_state['has_searched'] = False
            st.session_state['current_page'] = 'Overview'
            st.rerun()

        # Tagline Footer
        st.markdown(
            f"""
            <div style="margin-top: 24px; padding-top: 12px; border-top: 1px solid {THEME['border']}; text-align: center;">
                <div style="font-size: 0.75rem; font-weight: 600; color: {THEME['text_muted']};">
                    "Travel smarter, not harder."
                </div>
                <div style="font-size: 0.68rem; color: #94A3B8; margin-top: 4px;">
                    FlyBuddy v1.0 • Recruitment Demo
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    return selected_id
