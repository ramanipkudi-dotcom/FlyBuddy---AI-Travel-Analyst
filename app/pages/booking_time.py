"""
FlyBuddy - Best Time to Book Page (Part 3)
------------------------------------------
Empirical lead-time booking window analysis with real historical distributions.
"""

import streamlit as st
import pandas as pd
from app.components.theme import THEME
from app.components.header import render_header
from app.components.cards import render_kpi_card, render_insight_card
from app.components.charts import plot_lead_time_curve, get_base_layout
from src.booking_analysis import calculate_booking_lead_time_stats
import plotly.graph_objects as go

def render_booking_time_page(df):
    render_header(
        title="Best Time to Book",
        subtitle="When should you book for historically favorable prices?",
        badge_text="📅 Part 3 Priority"
    )

    with st.container():
        st.markdown('<div class="fb-card" style="padding: 16px 20px;">', unsafe_allow_html=True)
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
        <div class="fb-hero-card" style="background: linear-gradient(135deg, {THEME['surface']} 0%, {THEME['primary_light']} 100%);">
            <div style="font-size: 0.8rem; font-weight: 700; color: {THEME['primary_cyan']}; text-transform: uppercase;">
                Historically Favorable Booking Window ({sel_src} → {sel_dst})
            </div>
            <div style="font-size: 2.2rem; font-weight: 800; color: {THEME['deep_navy']}; margin: 6px 0;">
                {cheapest_window}
            </div>
            <div style="font-size: 1.05rem; color: {THEME['text_muted']};">
                Historically, median fares in this window were <b>₹{cheapest_price:,.0f}</b> (~<b>{savings_pct}% lower</b> than overall median of ₹{overall_median:,.0f}).
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"<h3 style='color: {THEME['deep_navy']}; font-weight: 800; font-size: 1.25rem;'>📊 Price vs. Booking Lead-Time</h3>", unsafe_allow_html=True)
    
    st.markdown('<div class="fb-card">', unsafe_allow_html=True)
    window_df = stats['window_stats_df']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=window_df['Window_Bin'].astype(str),
        y=window_df['median_price'],
        marker=dict(
            color=[THEME['success'] if str(w) == cheapest_window else THEME['secondary_blue'] for w in window_df['Window_Bin']]
        ),
        hovertemplate="Window: %{x}<br>Median Price: ₹%{y:,.0f}<extra></extra>"
    ))
    fig.update_layout(get_base_layout(title=f"Median Fare Across Booking Windows ({sel_src} → {sel_dst})", x_title="Booking Window", y_title="Median Price (₹)"))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col_w1, col_w2 = st.columns(2)
    with col_w1:
        render_insight_card(
            icon="💡",
            title="Why does this window show lower prices?",
            explanation="Airlines open initial booking inventory with promotional allocations. When departures are 22-35 days away, carriers balance seat fill-rate goals against revenue maximization before raising prices on the final remaining seats.",
            badge_text="Airline Economics",
            badge_type="good"
        )
    with col_w2:
        render_insight_card(
            icon="⚠️",
            title="Important Limitations & Disclaimer",
            explanation=stats['disclaimer'],
            badge_text="Analytical Notice",
            badge_type="high"
        )
