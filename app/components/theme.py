"""
FlyBuddy - Premium Real Glassmorphism Design System
---------------------------------------------------
Provides color tokens, atmospheric aviation gradients, real glassmorphism styling,
high-contrast inputs, and Dribbble-inspired frame layout.
"""

import streamlit as st

THEME = {
    'bg_deep': '#050C18',
    'bg_surface': '#0A1628',
    'sidebar_bg': '#07101E',
    'glass_card': 'rgba(10, 22, 40, 0.72)',
    'glass_floating': 'linear-gradient(145deg, rgba(12, 24, 44, 0.88) 0%, rgba(18, 34, 60, 0.72) 100%)',
    'primary_cyan': '#22D3EE',
    'secondary_violet': '#8B5CF6',
    'accent_blue': '#38BDF8',
    'text_primary': '#F8FAFC',
    'text_secondary': '#94A3B8',
    'text_muted': '#64748B',
    'border_subtle': 'rgba(255, 255, 255, 0.1)',
    'border_cyan': 'rgba(34, 211, 238, 0.3)',
    'success': '#34D399',
    'success_bg': 'rgba(52, 211, 153, 0.14)',
    'warning': '#FBBF24',
    'warning_bg': 'rgba(251, 191, 36, 0.14)',
    'card_radius': '20px',
    'card_shadow': '0 16px 40px rgba(0, 0, 0, 0.5)'
}

def apply_custom_theme():
    """
    Inject clean, real glassmorphism CSS, high-contrast input styles, and top padding fix.
    """
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* Global Aviation Dark Canvas with Atmospheric Lighting */
    html, body, [class*="css"], .stApp {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background-color: {THEME['bg_deep']} !important;
        background-image: 
            radial-gradient(circle at 10% 15%, rgba(34, 211, 238, 0.12) 0%, transparent 45%),
            radial-gradient(circle at 85% 75%, rgba(139, 92, 246, 0.13) 0%, transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(10, 22, 40, 0.6) 0%, transparent 100%) !important;
        background-attachment: fixed !important;
        color: {THEME['text_primary']} !important;
    }}

    /* Streamlit Chrome & Viewport Padding */
    header[data-testid="stHeader"] {{
        background: transparent !important;
        height: 1.2rem !important;
        z-index: 10 !important;
    }}
    header[data-testid="stHeader"] [data-testid="stToolbar"] {{
        top: 0.2rem !important;
        right: 1rem !important;
    }}
    
    .main .block-container {{
        padding-top: 0.8rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 1.8rem !important;
        padding-right: 1.8rem !important;
        max-width: 1260px !important;
    }}

    /* Dribbble-Inspired Large Rounded Outer Frame */
    .fb-hero-frame {{
        background: linear-gradient(150deg, rgba(10, 22, 40, 0.85) 0%, rgba(6, 14, 26, 0.95) 100%);
        backdrop-filter: blur(28px);
        -webkit-backdrop-filter: blur(28px);
        border: 1.5px solid rgba(255, 255, 255, 0.16);
        border-top: 1.5px solid rgba(255, 255, 255, 0.28);
        border-radius: 36px;
        padding: 32px 38px 36px 38px;
        box-shadow: 0 24px 70px rgba(0, 0, 0, 0.65), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }}

    /* Floating Flight Search Glass Card (Right Column) */
    .fb-floating-card {{
        background: {THEME['glass_floating']};
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-top: 1px solid rgba(255, 255, 255, 0.24);
        border-radius: 24px;
        padding: 24px 26px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.65), 0 0 25px rgba(34, 211, 238, 0.08);
    }}

    /* Distinct Sidebar Background */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #091322 0%, #040913 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 6px 0 28px rgba(0, 0, 0, 0.5) !important;
    }}
    [data-testid="stSidebar"] > div:first-child {{
        padding-top: 1.25rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }}

    /* Sidebar Navigation Items with Animated Glass Hover */
    [data-testid="stSidebar"] div.stRadio > div {{
        gap: 5px !important;
    }}
    [data-testid="stSidebar"] div.stRadio > div > label {{
        background: rgba(15, 23, 42, 0.4) !important;
        backdrop-filter: blur(8px) !important;
        padding: 9px 14px !important;
        border-radius: 12px !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        color: {THEME['text_secondary']} !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
    }}
    [data-testid="stSidebar"] div.stRadio > div > label:hover {{
        background: rgba(34, 211, 238, 0.1) !important;
        color: {THEME['primary_cyan']} !important;
        border-color: rgba(34, 211, 238, 0.25) !important;
        transform: translateX(3px) !important;
    }}
    [data-testid="stSidebar"] div.stRadio > div > label > div:first-child {{
        display: none !important;
    }}

    /* HIGH-CONTRAST Form Controls (Light & Dark Mode Safe) */
    div[data-baseweb="select"] > div {{
        background-color: #0B1728 !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 12px !important;
        color: #F8FAFC !important;
    }}
    div[data-baseweb="select"] span {{
        color: #F8FAFC !important;
        font-weight: 500 !important;
    }}
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] {{
        background-color: #0B1728 !important;
        border: 1px solid rgba(34, 211, 238, 0.3) !important;
        border-radius: 12px !important;
    }}
    li[data-baseweb="menu-item"] {{
        color: #F8FAFC !important;
        font-weight: 500 !important;
    }}
    li[data-baseweb="menu-item"]:hover {{
        background-color: rgba(34, 211, 238, 0.18) !important;
        color: #22D3EE !important;
    }}
    div[data-baseweb="input"] > div {{
        background-color: #0B1728 !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 12px !important;
        color: #F8FAFC !important;
    }}
    input {{
        color: #F8FAFC !important;
    }}
    label, [data-testid="stWidgetLabel"] p {{
        color: {THEME['text_secondary']} !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
    }}

    /* Real Glassmorphism Cards */
    .fb-glass-card {{
        background: {THEME['glass_card']};
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid {THEME['border_subtle']};
        border-top: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: {THEME['card_radius']};
        padding: 22px 26px;
        box-shadow: {THEME['card_shadow']};
        margin-bottom: 20px;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }}
    .fb-glass-card:hover {{
        border-color: rgba(34, 211, 238, 0.25);
        box-shadow: 0 16px 44px rgba(0, 0, 0, 0.55), 0 0 20px rgba(34, 211, 238, 0.08);
    }}

    /* KPI Metric Cards */
    .fb-kpi-card {{
        background: {THEME['glass_card']};
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid {THEME['border_subtle']};
        border-top: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: {THEME['card_shadow']};
        height: 100%;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}
    .fb-kpi-card:hover {{
        border-color: rgba(34, 211, 238, 0.3);
        transform: translateY(-2px);
    }}
    .fb-kpi-label {{
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {THEME['text_secondary']};
        margin-bottom: 4px;
    }}
    .fb-kpi-value {{
        font-size: 1.8rem;
        font-weight: 800;
        color: {THEME['text_primary']};
        line-height: 1.2;
    }}
    .fb-kpi-sub {{
        font-size: 0.82rem;
        color: {THEME['text_secondary']};
        margin-top: 4px;
    }}

    /* Badges */
    .fb-badge {{
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
    }}
    .fb-badge-good {{
        background-color: {THEME['success_bg']};
        color: {THEME['success']};
        border: 1px solid rgba(52, 211, 153, 0.3);
    }}
    .fb-badge-typical {{
        background-color: rgba(34, 211, 238, 0.12);
        color: {THEME['primary_cyan']};
        border: 1px solid rgba(34, 211, 238, 0.3);
    }}
    .fb-badge-violet {{
        background-color: rgba(139, 92, 246, 0.12);
        color: {THEME['secondary_violet']};
        border: 1px solid rgba(139, 92, 246, 0.3);
    }}

    /* Animated Pill CTA Button (✦ Analyze My Trip) */
    div[data-testid="stButton"] > button {{
        background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 50%, #8B5CF6 100%) !important;
        background-size: 200% 200% !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.35) !important;
        border-radius: 9999px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 4px 24px rgba(34, 211, 238, 0.4), 0 0 16px rgba(139, 92, 246, 0.3) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4) !important;
    }}
    div[data-testid="stButton"] > button:hover {{
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 32px rgba(34, 211, 238, 0.6), 0 0 28px rgba(139, 92, 246, 0.45) !important;
        border-color: rgba(255, 255, 255, 0.6) !important;
    }}
    div[data-testid="stButton"] > button:active {{
        transform: translateY(0px) scale(0.99) !important;
    }}

    /* Insight Box */
    .fb-insight-box {{
        background: {THEME['glass_card']};
        backdrop-filter: blur(14px);
        border: 1px solid {THEME['border_subtle']};
        border-left: 4px solid {THEME['primary_cyan']};
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 14px;
    }}
    .fb-insight-title {{
        font-weight: 700;
        font-size: 0.96rem;
        color: {THEME['text_primary']};
        margin-bottom: 4px;
    }}
    .fb-insight-body {{
        font-size: 0.88rem;
        color: {THEME['text_secondary']};
        line-height: 1.5;
    }}

    /* Flight Recommendation Card */
    .fb-flight-card {{
        background: {THEME['glass_card']};
        backdrop-filter: blur(16px);
        border: 1px solid {THEME['border_subtle']};
        border-top: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 14px;
        box-shadow: {THEME['card_shadow']};
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}
    .fb-flight-card:hover {{
        border-color: rgba(34, 211, 238, 0.3);
        transform: translateY(-2px);
    }}
    .fb-flight-price {{
        font-size: 1.6rem;
        font-weight: 800;
        color: {THEME['primary_cyan']};
        text-shadow: 0 0 14px rgba(34, 211, 238, 0.3);
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
