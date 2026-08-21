"""
FlyBuddy - Premium Analysis & Loading Experience
------------------------------------------------
Full-page loading screen with dark glassmorphic card,
continuous smooth flight motion animation, and timed stage progression.
"""

import time
import streamlit as st
from app.components.theme import THEME

def render_analysis_loading(source_city, dest_city):
    """
    Renders a dedicated full-page loading screen for ~3.2 seconds.
    Hides sidebar during loading and displays zero raw HTML.
    Features a continuous, smooth CSS-driven flight animation.
    """
    # Hide sidebar while loading
    st.markdown("<style>[data-testid='stSidebar'] { display: none !important; } .main .block-container { max-width: 760px !important; padding-top: 2rem !important; }</style>", unsafe_allow_html=True)

    steps = [
        "Analyzing your journey",
        "Processing historical flight prices",
        "Analyzing booking patterns",
        "Preparing your travel insights"
    ]

    container = st.empty()

    for idx, step_msg in enumerate(steps):
        pct = int(((idx + 1) / len(steps)) * 100)

        # Build Stage Items
        stage_items = []
        for i, s in enumerate(steps):
            if i < idx:
                icon = "✓"
                color = THEME['success']
                bg = "rgba(52, 211, 153, 0.08)"
                border = "rgba(52, 211, 153, 0.25)"
                status_txt = "DONE"
                opacity = "1"
            elif i == idx:
                icon = "✦"
                color = THEME['primary_cyan']
                bg = "rgba(34, 211, 238, 0.12)"
                border = "rgba(34, 211, 238, 0.35)"
                status_txt = "ACTIVE"
                opacity = "1"
            else:
                icon = "○"
                color = THEME['text_secondary']
                bg = "rgba(255, 255, 255, 0.02)"
                border = "rgba(255, 255, 255, 0.04)"
                status_txt = "WAIT"
                opacity = "0.45"

            stage_items.append(f'''<div style="display: flex; align-items: center; justify-content: space-between; padding: 10px 14px; margin-bottom: 8px; border-radius: 12px; background: {bg}; border: 1px solid {border}; opacity: {opacity};">
<div style="display: flex; align-items: center; gap: 12px;">
<span style="color: {color}; font-size: 0.95rem; font-weight: bold; width: 16px; text-align: center;">{icon}</span>
<span style="color: {THEME['text_primary'] if i <= idx else THEME['text_secondary']}; font-size: 0.9rem; font-weight: 600;">{s}</span>
</div>
<span style="font-size: 0.75rem; font-weight: 700; color: {color};">{status_txt}</span>
</div>''')

        stages_block = "\n".join(stage_items)

        html_str = f'''<style>
@keyframes flyAcross {{
    0% {{
        left: 45px;
        transform: translateY(-50%) rotate(0deg);
        opacity: 0.3;
    }}
    5% {{
        opacity: 1;
    }}
    25% {{
        transform: translateY(-70%) rotate(-4deg);
    }}
    50% {{
        transform: translateY(-50%) rotate(0deg);
    }}
    75% {{
        transform: translateY(-30%) rotate(4deg);
    }}
    95% {{
        opacity: 1;
    }}
    100% {{
        left: calc(100% - 75px);
        transform: translateY(-50%) rotate(0deg);
        opacity: 0.3;
    }}
}}
.fb-flying-plane {{
    position: absolute;
    top: 50%;
    animation: flyAcross 3.2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #0A172B;
    border: 1.5px solid {THEME['primary_cyan']};
    box-shadow: 0 0 16px rgba(34, 211, 238, 0.85), -10px 0 22px rgba(34, 211, 238, 0.5), -20px 0 30px rgba(139, 92, 246, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    color: {THEME['primary_cyan']};
    z-index: 3;
}}
</style>
<div style="display: flex; justify-content: center; align-items: center; min-height: 75vh; padding: 10px 0;">
<div style="width: 100%; max-width: 600px; background: linear-gradient(145deg, rgba(12, 24, 46, 0.92) 0%, rgba(6, 14, 28, 0.98) 100%); backdrop-filter: blur(28px); -webkit-backdrop-filter: blur(28px); border: 1.5px solid rgba(255, 255, 255, 0.14); border-top: 1.5px solid rgba(255, 255, 255, 0.3); border-radius: 28px; padding: 36px 34px; box-shadow: 0 24px 70px rgba(0, 0, 0, 0.8), 0 0 35px rgba(34, 211, 238, 0.12); text-align: center;">

<div style="display: inline-flex; align-items: center; gap: 8px; margin-bottom: 20px;">
<div style="width: 34px; height: 34px; border-radius: 9px; background: linear-gradient(135deg, {THEME['primary_cyan']}, {THEME['secondary_violet']}); display: flex; align-items: center; justify-content: center; color: white; font-size: 16px; font-weight: bold; box-shadow: 0 4px 12px rgba(34, 211, 238, 0.35);">✈</div>
<div style="text-align: left;">
<div style="font-size: 1.15rem; font-weight: 800; color: {THEME['text_primary']}; letter-spacing: -0.02em; line-height: 1;">FlyBuddy</div>
<div style="font-size: 0.64rem; font-weight: 700; color: {THEME['primary_cyan']}; letter-spacing: 0.08em; text-transform: uppercase;">TRAVEL ANALYST</div>
</div>
</div>

<div style="position: relative; width: 100%; height: 50px; margin: 6px 0 20px 0; display: flex; align-items: center; justify-content: space-between; padding: 0 16px;">
<div style="text-align: center; z-index: 2;">
<div style="width: 10px; height: 10px; border-radius: 50%; background: {THEME['primary_cyan']}; box-shadow: 0 0 10px {THEME['primary_cyan']}; margin: 0 auto 3px auto;"></div>
<div style="font-size: 0.82rem; font-weight: 700; color: {THEME['text_primary']};">{source_city}</div>
</div>

<div style="position: absolute; left: 50px; right: 50px; height: 2px; background: linear-gradient(90deg, {THEME['primary_cyan']} 0%, {THEME['secondary_violet']} 100%); opacity: 0.35; z-index: 1;"></div>

<div class="fb-flying-plane">✈</div>

<div style="text-align: center; z-index: 2;">
<div style="width: 10px; height: 10px; border-radius: 50%; background: {THEME['secondary_violet']}; box-shadow: 0 0 10px {THEME['secondary_violet']}; margin: 0 auto 3px auto;"></div>
<div style="font-size: 0.82rem; font-weight: 700; color: {THEME['text_primary']};">{dest_city}</div>
</div>
</div>

<div style="font-size: 1.75rem; font-weight: 800; color: {THEME['text_primary']}; letter-spacing: -0.02em; margin-bottom: 6px;">Analyzing your route</div>
<div style="font-size: 0.92rem; color: {THEME['text_secondary']}; max-width: 440px; margin: 0 auto 20px auto; line-height: 1.45;">Comparing historical fares, booking patterns and route trends.</div>

<div style="width: 100%; height: 6px; background: rgba(255, 255, 255, 0.08); border-radius: 9999px; overflow: hidden; margin-bottom: 20px;">
<div style="width: {pct}%; height: 100%; background: linear-gradient(90deg, {THEME['primary_cyan']}, {THEME['secondary_violet']}); border-radius: 9999px; box-shadow: 0 0 14px rgba(34, 211, 238, 0.7);"></div>
</div>

<div style="text-align: left;">
{stages_block}
</div>

</div>
</div>'''

        # Clean all whitespace per line to strictly prevent markdown code block triggers
        cleaned_html = "\n".join(line.strip() for line in html_str.splitlines())
        container.markdown(cleaned_html, unsafe_allow_html=True)
        time.sleep(0.8)

    container.empty()
