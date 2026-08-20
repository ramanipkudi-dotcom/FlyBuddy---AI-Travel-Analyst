"""
FlyBuddy - Reusable UI Card Components
--------------------------------------
Card templates for KPI metrics, insights, and recommendation summaries.
"""

import streamlit as st
from app.components.theme import THEME

def render_kpi_card(label, value, subtext=None, delta=None, delta_positive=True):
    """
    Render a single metric KPI card.
    """
    delta_html = ""
    if delta:
        color = THEME['success'] if delta_positive else THEME['danger']
        sign = "↓" if delta_positive else "↑"
        delta_html = f"<div style='font-size: 0.8rem; font-weight: 700; color: {color}; margin-top: 4px;'>{sign} {delta}</div>"

    html = f"""
    <div class="fb-kpi-card">
        <div class="fb-kpi-label">{label}</div>
        <div class="fb-kpi-value">{value}</div>
        {f'<div class="fb-kpi-sub">{subtext}</div>' if subtext else ''}
        {delta_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_insight_card(icon, title, explanation, badge_text=None, badge_type='typical'):
    """
    Render an analytical insight callout.
    """
    badge_html = f'<span class="fb-badge fb-badge-{badge_type}" style="float: right;">{badge_text}</span>' if badge_text else ''
    
    html = f"""
    <div class="fb-insight-box">
        <div class="fb-insight-title">
            {icon} {title}
            {badge_html}
        </div>
        <div class="fb-insight-body">{explanation}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_recommendation_card(flight):
    """
    Render an explainable flight card with reason badges.
    """
    chips_html = "".join([f'<span class="fb-badge fb-badge-good" style="margin-right: 6px; margin-bottom: 6px;">✓ {r}</span>' for r in flight.get('reasons', [])])
    
    html = f"""
    <div class="fb-flight-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
            <div>
                <div style="font-size: 1.1rem; font-weight: 800; color: {THEME['deep_navy']};">
                    ✈ {flight.get('airline', 'Airline')}
                </div>
                <div style="font-size: 0.88rem; color: {THEME['text_muted']}; margin-top: 2px;">
                    {flight.get('source')} → {flight.get('destination')} • {flight.get('travel_class', 'Economy')}
                </div>
                <div style="font-size: 0.82rem; color: {THEME['deep_navy']}; font-weight: 600; margin-top: 6px;">
                    🕒 {flight.get('departure_time')} - {flight.get('arrival_time')} ({flight.get('duration_str')}) • {flight.get('stops')} Stop(s)
                </div>
            </div>
            <div style="text-align: right;">
                <div class="fb-flight-price">₹{flight.get('price', 0):,.2f}</div>
                <div style="font-size: 0.75rem; color: {THEME['text_muted']};">Estimated total</div>
            </div>
        </div>
        <div style="margin-top: 14px; padding-top: 10px; border-top: 1px dashed {THEME['border']};">
            <div style="font-size: 0.76rem; font-weight: 700; color: {THEME['text_muted']}; margin-bottom: 6px; text-transform: uppercase;">
                Why FlyBuddy Recommends This:
            </div>
            <div>{chips_html}</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
