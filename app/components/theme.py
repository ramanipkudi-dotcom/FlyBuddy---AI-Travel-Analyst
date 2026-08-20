"""
FlyBuddy - Centralized Theme & Design System
--------------------------------------------
Provides theme tokens and custom CSS styling for the FlyBuddy Streamlit application.

Why this matters for interviews:
- Centralizes colors and styling tokens so switching themes (or adding Dark Mode)
  requires updating variables in ONE place rather than hunting through 50 files.
"""

import streamlit as st

# Color Palette: Light Blue + Cyan Palette
THEME = {
    'primary_cyan': '#12B8D4',
    'primary_light': '#E6F9FC',
    'secondary_blue': '#3B82F6',
    'deep_navy': '#0F2742',
    'background': '#F7FBFC',
    'surface': '#FFFFFF',
    'border': '#DCEAF0',
    'text_primary': '#0F2742',
    'text_muted': '#64748B',
    'success': '#16A34A',
    'success_light': '#DCFCE7',
    'warning': '#F59E0B',
    'warning_light': '#FEF3C7',
    'danger': '#EF4444',
    'danger_light': '#FEE2E2',
    'card_radius': '14px',
    'card_shadow': '0 2px 10px rgba(15, 39, 66, 0.04)'
}

def apply_custom_theme():
    """
    Inject custom CSS to create a modern SaaS analytics look for Streamlit.
    """
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background-color: {THEME['background']};
        color: {THEME['text_primary']};
    }}

    /* Top Padding & App Layout */
    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1240px;
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: {THEME['surface']};
        border-right: 1px solid {THEME['border']};
    }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
        font-size: 0.92rem;
    }}

    /* Custom Cards */
    .fb-card {{
        background: {THEME['surface']};
        border: 1px solid {THEME['border']};
        border-radius: {THEME['card_radius']};
        padding: 20px 24px;
        box-shadow: {THEME['card_shadow']};
        margin-bottom: 20px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    .fb-card:hover {{
        box-shadow: 0 6px 18px rgba(18, 184, 212, 0.08);
    }}

    /* Hero / Trip Input Card */
    .fb-hero-card {{
        background: linear-gradient(135deg, #FFFFFF 0%, {THEME['primary_light']} 100%);
        border: 1px solid {THEME['border']};
        border-radius: 18px;
        padding: 28px 32px;
        box-shadow: 0 8px 24px rgba(18, 184, 212, 0.08);
        margin-bottom: 24px;
    }}

    /* KPI Metric Box */
    .fb-kpi-card {{
        background: {THEME['surface']};
        border: 1px solid {THEME['border']};
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: {THEME['card_shadow']};
        height: 100%;
    }}
    .fb-kpi-label {{
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {THEME['text_muted']};
        margin-bottom: 6px;
    }}
    .fb-kpi-value {{
        font-size: 1.75rem;
        font-weight: 800;
        color: {THEME['deep_navy']};
        line-height: 1.2;
    }}
    .fb-kpi-sub {{
        font-size: 0.8rem;
        color: {THEME['text_muted']};
        margin-top: 4px;
    }}

    /* Badges */
    .fb-badge {{
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
    }}
    .fb-badge-good {{
        background-color: {THEME['success_light']};
        color: {THEME['success']};
        border: 1px solid rgba(22, 163, 74, 0.2);
    }}
    .fb-badge-typical {{
        background-color: {THEME['primary_light']};
        color: #0284C7;
        border: 1px solid rgba(2, 132, 199, 0.2);
    }}
    .fb-badge-high {{
        background-color: {THEME['warning_light']};
        color: {THEME['warning']};
        border: 1px solid rgba(245, 158, 11, 0.2);
    }}

    /* Custom Streamlit Buttons */
    div.stButton > button {{
        background-color: {THEME['primary_cyan']};
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.55rem 1.4rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 6px rgba(18, 184, 212, 0.25);
    }}
    div.stButton > button:hover {{
        background-color: #0ea5e9;
        box-shadow: 0 4px 12px rgba(18, 184, 212, 0.35);
        color: #FFFFFF;
    }}
    div.stButton > button:active {{
        transform: translateY(1px);
    }}

    /* Insight Callout */
    .fb-insight-box {{
        background: #F8FAFC;
        border-left: 4px solid {THEME['primary_cyan']};
        border-radius: 0 10px 10px 0;
        padding: 14px 18px;
        margin-bottom: 12px;
    }}
    .fb-insight-title {{
        font-weight: 700;
        font-size: 0.92rem;
        color: {THEME['deep_navy']};
        margin-bottom: 4px;
    }}
    .fb-insight-body {{
        font-size: 0.85rem;
        color: {THEME['text_muted']};
        line-height: 1.45;
    }}

    /* Recommendation Flight Card */
    .fb-flight-card {{
        background: {THEME['surface']};
        border: 1px solid {THEME['border']};
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 14px;
        box-shadow: {THEME['card_shadow']};
    }}
    .fb-flight-price {{
        font-size: 1.5rem;
        font-weight: 800;
        color: {THEME['deep_navy']};
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
