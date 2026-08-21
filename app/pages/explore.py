"""
FlyBuddy - Price Explorer Page
------------------------------
Interactive data filtering tool to explore flight prices across routes, airlines, classes, and seasons.
"""

import streamlit as st
import pandas as pd
from app.components.theme import THEME
from app.components.header import render_header
from app.components.cards import render_kpi_card
from app.components.charts import (
    plot_price_distribution, plot_airline_prices, plot_travel_class_prices,
    plot_stops_vs_price, plot_lead_time_curve
)

def render_explore_page(df):
    render_header(
        title="Price Explorer",
        subtitle="Filter and explore historical flight records across multiple dimensions.",
        badge_text="Data Explorer"
    )

    with st.container():
        st.markdown('<div class="fb-glass-card" style="padding: 16px 22px;">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        sources = ['All'] + sorted([str(x) for x in df['Source'].dropna().unique()])
        dests = ['All'] + sorted([str(x) for x in df['Destination'].dropna().unique()])
        airlines = ['All'] + sorted([str(x) for x in df['Airline'].dropna().unique()])
        classes = ['All', 'Economy', 'Premium Economy', 'Business', 'First']

        with col1:
            sel_src = st.selectbox("Origin", sources, index=0, key="exp_src")
        with col2:
            sel_dst = st.selectbox("Destination", dests, index=0, key="exp_dst")
        with col3:
            sel_airline = st.selectbox("Airline", airlines, index=0, key="exp_airline")
        with col4:
            sel_class = st.selectbox("Travel Class", classes, index=0, key="exp_class")

        col5, col6, col7, col8 = st.columns(4)
        seasons = ['All', 'Summer', 'Monsoon', 'Autumn', 'Winter', 'Spring']
        stops_opts = ['All', 'Non-stop', '1 Stop', '2+ Stops']
        channels = ['All'] + sorted([str(x) for x in df['Booking_Channel'].dropna().unique()])

        with col5:
            sel_season = st.selectbox("Season", seasons, index=0, key="exp_season")
        with col6:
            sel_stops = st.selectbox("Stops", stops_opts, index=0, key="exp_stops")
        with col7:
            sel_channel = st.selectbox("Booking Channel", channels, index=0, key="exp_channel")
        with col8:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            def reset_explore_filters():
                st.session_state['exp_src'] = 'All'
                st.session_state['exp_dst'] = 'All'
                st.session_state['exp_airline'] = 'All'
                st.session_state['exp_class'] = 'All'
                st.session_state['exp_season'] = 'All'
                st.session_state['exp_stops'] = 'All'
                st.session_state['exp_channel'] = 'All'

            st.button("Reset Filters", use_container_width=True, on_click=reset_explore_filters)

        st.markdown('</div>', unsafe_allow_html=True)

    # Filter Data
    filtered_df = df.copy()
    if sel_src != 'All':
        filtered_df = filtered_df[filtered_df['Source'] == sel_src]
    if sel_dst != 'All':
        filtered_df = filtered_df[filtered_df['Destination'] == sel_dst]
    if sel_airline != 'All':
        filtered_df = filtered_df[filtered_df['Airline'] == sel_airline]
    if sel_class != 'All':
        filtered_df = filtered_df[filtered_df['Travel_Class'] == sel_class]
    if sel_season != 'All':
        filtered_df = filtered_df[filtered_df['Season'] == sel_season]
    if sel_channel != 'All':
        filtered_df = filtered_df[filtered_df['Booking_Channel'] == sel_channel]
    if sel_stops != 'All':
        if sel_stops == 'Non-stop':
            filtered_df = filtered_df[filtered_df['Total_Stops_num'] == 0]
        elif sel_stops == '1 Stop':
            filtered_df = filtered_df[filtered_df['Total_Stops_num'] == 1]
        elif sel_stops == '2+ Stops':
            filtered_df = filtered_df[filtered_df['Total_Stops_num'] >= 2]

    # Metrics Row
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    total_records = len(filtered_df)
    med_p = filtered_df['Price_clean'].median() if total_records > 0 else 0
    min_p = filtered_df['Price_clean'].min() if total_records > 0 else 0
    max_p = filtered_df['Price_clean'].max() if total_records > 0 else 0

    with m_col1:
        render_kpi_card("Matching Records", f"{total_records:,}", f"{(total_records/len(df)*100):.1f}% of total data")
    with m_col2:
        render_kpi_card("Median Fare", f"₹{med_p:,.0f}", "50th percentile")
    with m_col3:
        render_kpi_card("Lowest Fare", f"₹{min_p:,.0f}", "Minimum observed")
    with m_col4:
        render_kpi_card("Highest Fare", f"₹{max_p:,.0f}", "Maximum observed")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    if total_records == 0:
        st.warning("No flight records match the selected filters. Please adjust your criteria or click 'Reset Filters'.")
        return

    # Visualizations Grid
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="fb-glass-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_price_distribution(filtered_df, title="Price Distribution"), use_container_width=True)
        st.markdown(f"<p style='font-size: 0.83rem; color: var(--fb-text-secondary, #94A3B8); margin-top: 4px;'><b>What this shows:</b> Distribution of fares for the currently filtered set of flights.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="fb-glass-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_lead_time_curve(filtered_df, title="Booking Window vs. Fare"), use_container_width=True)
        st.markdown(f"<p style='font-size: 0.83rem; color: var(--fb-text-secondary, #94A3B8); margin-top: 4px;'><b>What this shows:</b> How advance booking timing relates to typical fares within this filter subset.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="fb-glass-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_airline_prices(filtered_df, title="Airlines vs. Typical Fare"), use_container_width=True)
        st.markdown(f"<p style='font-size: 0.83rem; color: var(--fb-text-secondary, #94A3B8); margin-top: 4px;'><b>What this shows:</b> Price variation between different operating airlines in the selection.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="fb-glass-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_travel_class_prices(filtered_df, title="Cabin Class vs. Typical Fare"), use_container_width=True)
        st.markdown(f"<p style='font-size: 0.83rem; color: var(--fb-text-secondary, #94A3B8); margin-top: 4px;'><b>What this shows:</b> Fare differences across available cabin tiers in the selection.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
