"""
FlyBuddy - Stepped Loading Screen Component
-------------------------------------------
Renders a progressive, realistic analysis loading sequence after trip submission.
"""

import time
import streamlit as st
from app.components.theme import THEME

def render_analysis_loading(source_city, dest_city):
    """
    Show intentional multi-step loading sequence that quickly progresses to results.
    """
    steps = [
        "Checking historical flight data...",
        "Analyzing route price patterns & distribution...",
        "Identifying primary cost drivers...",
        "Calculating optimal historical booking lead-time window...",
        "Preparing explainable flight recommendations..."
    ]

    st.markdown(
        f"""
        <div style="text-align: center; margin: 40px 0 20px 0;">
            <div style="font-size: 2.2rem; font-weight: 800; color: {THEME['deep_navy']};">
                ✈ FlyBuddy is Analyzing Your Trip
            </div>
            <div style="font-size: 1.1rem; color: {THEME['primary_cyan']}; font-weight: 600; margin-top: 6px;">
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
            f"<div style='font-size: 0.95rem; color: {THEME['success'] if i <= idx else THEME['text_muted']}; margin: 6px 0;'>"
            f"{'✓' if i <= idx else '○'} {s}</div>"
            for i, s in enumerate(steps)
        ])
        
        status_container.markdown(
            f"""
            <div class="fb-card" style="max-width: 600px; margin: 0 auto 30px auto; padding: 24px;">
                {status_html}
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(0.12)  # Swift, realistic transition
