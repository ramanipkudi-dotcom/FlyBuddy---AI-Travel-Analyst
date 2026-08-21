"""
FlyBuddy - Stepped Loading Component
------------------------------------
Smooth dark glass animated transition sequence between search and overview.
"""

import time
import streamlit as st
from app.components.theme import THEME

def render_analysis_loading(source_city, dest_city):
    steps = [
        "Preparing your trip...",
        "Analyzing historical flight prices...",
        "Finding favorable booking windows...",
        "Preparing your travel insights..."
    ]

    st.markdown(
        f"""
        <div style="text-align: center; margin: 48px 0 24px 0;">
            <div style="font-size: 1.9rem; font-weight: 800; color: {THEME['text_primary']};">
                Analyzing Your Route
            </div>
            <div style="font-size: 1.1rem; color: {THEME['primary_cyan']}; font-weight: 600; margin-top: 4px;">
                {source_city} → {dest_city}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    progress_bar = st.progress(0)
    status_container = st.empty()

    for idx, step in enumerate(steps):
        pct = int(((idx + 1) / len(steps)) * 100)
        progress_bar.progress(pct)
        
        status_html = "".join([
            f"<div style='font-size: 0.9rem; color: {THEME['success'] if i <= idx else THEME['text_secondary']}; margin: 7px 0;'>"
            f"{'●' if i <= idx else '○'} {s}</div>"
            for i, s in enumerate(steps)
        ])
        
        status_container.markdown(
            f"""
            <div class="fb-glass-card" style="max-width: 500px; margin: 0 auto 24px auto; padding: 24px; border-color: rgba(34, 211, 238, 0.3);">
                {status_html}
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(0.08)
