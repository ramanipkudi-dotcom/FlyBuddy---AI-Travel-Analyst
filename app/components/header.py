"""
FlyBuddy - Content Header Component
-----------------------------------
Renders the top bar for each page without excessive top padding.
"""

import streamlit as st
from app.components.theme import THEME

def render_header(title, subtitle=None, badge_text=None):
    """
    Render clean top bar with page title, subtitle, and optional status chip.
    """
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(
            f"""
            <div style="margin-bottom: 14px;">
                <h1 style="font-size: 1.75rem; font-weight: 800; color: {THEME['text_primary']}; margin: 0; padding: 0; letter-spacing: -0.02em;">
                    {title}
                </h1>
                {f'<p style="font-size: 0.92rem; color: {THEME["text_secondary"]}; margin: 4px 0 0 0;">{subtitle}</p>' if subtitle else ''}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        if badge_text:
            st.markdown(
                f"""
                <div style="text-align: right; padding-top: 4px;">
                    <span class="fb-badge fb-badge-typical">
                        {badge_text}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
