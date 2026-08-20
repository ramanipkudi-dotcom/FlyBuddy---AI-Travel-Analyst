"""
FlyBuddy - Main Content Header Component
-----------------------------------------
Renders the top bar for each page with title, subtitle, and live analytics status chip.
"""

import streamlit as st
from app.components.theme import THEME

def render_header(title, subtitle=None, badge_text=None):
    """
    Render clean top bar with page title and live system status badge.
    """
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(
            f"""
            <div style="margin-bottom: 16px;">
                <h1 style="font-size: 1.85rem; font-weight: 800; color: {THEME['deep_navy']}; margin: 0; padding: 0; letter-spacing: -0.02em;">
                    {title}
                </h1>
                {f'<p style="font-size: 0.95rem; color: {THEME["text_muted"]}; margin: 4px 0 0 0;">{subtitle}</p>' if subtitle else ''}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        status_text = badge_text if badge_text else "🟢 100k Records Live"
        st.markdown(
            f"""
            <div style="text-align: right; padding-top: 6px;">
                <span class="fb-badge fb-badge-typical" style="font-size: 0.78rem;">
                    {status_text}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
