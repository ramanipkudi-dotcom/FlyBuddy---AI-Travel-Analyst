"""
FlyBuddy - Best Time to Book Page
---------------------------------
Explore how historical fares change based on how far in advance the flight was booked.
"""

import streamlit as st
import pandas as pd
from app.components.theme import THEME
from app.components.header import render_header
from app.components.cards import render_kpi_card, render_insight_card
from app.components.charts import get_base_layout
from src.booking_analysis import calculate_booking_lead_time_stats
import plotly.graph_objects as go

def render_booking_time_page(df):
    render_header(
        title="When should you book?",
        subtitle="Explore how historical fares change based on how far in advance the flight was booked.",
        badge_text="Booking Timing"
    )

    with st.container():
        st.markdown('<div class="fb-glass-card" style="padding: 16px 22px;">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        sources = sorted([str(x) for x in df['Source'].dropna().unique()])
        dests = sorted([str(x) for x in df['Destination'].dropna().unique()])
        classes = ['All Classes', 'Economy', 'Premium Economy', 'Business', 'First']

        default_from_idx = sources.index(st.session_state.get('active_source', 'Chennai')) if st.session_state.get('active_source', 'Chennai') in sources else 0
        default_to_idx = dests.index(st.session_state.get('active_dest', 'Mumbai')) if st.session_state.get('active_dest', 'Mumbai') in dests else 0

        with col1:
            sel_src = st.selectbox("Origin", sources, index=default_from_idx, key="bt_src")
        with col2:
            sel_dst = st.selectbox("Destination", dests, index=default_to_idx, key="bt_dst")
        with col3:
            sel_class = st.selectbox("Travel Class", classes, index=0, key="bt_class")

        st.markdown('</div>', unsafe_allow_html=True)

    stats = calculate_booking_lead_time_stats(df, source=sel_src, destination=sel_dst, travel_class=sel_class)
    if not stats:
        stats = calculate_booking_lead_time_stats(df, travel_class=sel_class)

    cheapest_window = stats['cheapest_window']
    cheapest_price = stats['cheapest_median_price']
    overall_median = stats['overall_median_price']
    savings_pct = stats['potential_savings_pct']

    st.markdown(
        f"""
        <div class="fb-hero-card">
            <div style="font-size: 0.78rem; font-weight: 700; color: {THEME['primary_cyan']}; text-transform: uppercase; letter-spacing: 0.05em;">
                Historically Favorable Booking Window ({sel_src} → {sel_dst})
            </div>
            <div style="font-size: 2.2rem; font-weight: 800; color: {THEME['text_primary']}; margin: 6px 0;">
                {cheapest_window}
            </div>
            <div style="font-size: 1rem; color: {THEME['text_secondary']};">
                Historically, fares were lower around this booking window, with a median price of <b style="color: {THEME['primary_cyan']};">₹{cheapest_price:,.0f}</b> (~<b style="color: {THEME['success']};">{savings_pct}% lower</b> than the route median of ₹{overall_median:,.0f}).
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"<h3 style='color: {THEME['text_primary']}; font-weight: 700; font-size: 1.2rem;'>Typical Prices by Booking Time</h3>", unsafe_allow_html=True)
    
    st.markdown('<div class="fb-glass-card">', unsafe_allow_html=True)
    window_df = stats['window_stats_df']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=window_df['Window_Bin'].astype(str),
        y=window_df['median_price'],
        marker=dict(
            color=[THEME['success'] if str(w) == cheapest_window else THEME['primary_cyan'] for w in window_df['Window_Bin']],
            line=dict(color='rgba(255,255,255,0.15)', width=0.5)
        ),
        hovertemplate="Booking Window: %{x}<br>Typical Fare: ₹%{y:,.0f}<extra></extra>"
    ))
    fig.update_layout(get_base_layout(title=f"Typical Fares Across Booking Windows ({sel_src} → {sel_dst})", x_title="Booking Timing", y_title="Typical Fare (₹)"))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"<p style='font-size: 0.83rem; color: {THEME['text_secondary']}; margin-top: 4px;'><b>What this shows:</b> Fares are generally more favorable when booked during the historically lower-price booking window ({cheapest_window}).</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col_w1, col_w2 = st.columns(2)
    with col_w1:
        render_insight_card(
            title="Why are fares lower in this window?",
            explanation=f"Airlines balance seat fill rates with revenue management during the <b>{cheapest_window}</b> window, offering competitive inventory before raising prices on remaining seats.",
            badge_text="Booking Behavior",
            badge_type="good"
        )
    with col_w2:
        render_insight_card(
            title="Important Note",
            explanation="These insights are based on historical flight pricing patterns and do not guarantee future prices. Seasonal demand and holidays can alter fare timing.",
            badge_text="Notice",
            badge_type="high"
        )
