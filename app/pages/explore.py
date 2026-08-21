"""
FlyBuddy - Price Explorer Page
------------------------------
Interactive multi-attribute data exploration tool with real-time single-click filtering and reset.
"""

import streamlit as st
import pandas as pd
from app.components.theme import THEME
from app.components.header import render_header
from app.components.charts import (
    plot_price_distribution, plot_airline_prices, plot_travel_class_prices,
    plot_stops_vs_price, plot_lead_time_curve
)

def render_explore_page(df):
    render_header(
        title="Price Explorer",
        subtitle="Explore flight prices across routes, airlines, cabin classes, and booking conditions.",
        badge_text="Exploration Tool"
    )

    # Initialize keys if missing
    for k in ['exp_src', 'exp_dst', 'exp_air', 'exp_cls', 'exp_sea', 'exp_stp', 'exp_chn']:
        if k not in st.session_state:
            st.session_state[k] = 'All'

    # Single-Click Reset Callback
    def reset_explore_filters():
        st.session_state['exp_src'] = 'All'
        st.session_state['exp_dst'] = 'All'
        st.session_state['exp_air'] = 'All'
        st.session_state['exp_cls'] = 'All'
        st.session_state['exp_sea'] = 'All'
        st.session_state['exp_stp'] = 'All'
        st.session_state['exp_chn'] = 'All'

    with st.container():
        st.markdown('<div class="fb-glass-card" style="padding: 18px 22px;">', unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 0.78rem; font-weight: 700; color: {THEME['primary_cyan']}; text-transform: uppercase; margin-bottom: 10px; letter-spacing: 0.05em;'>Filter Flight Data</div>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        sources = ['All'] + sorted([str(x) for x in df['Source'].dropna().unique()])
        dests = ['All'] + sorted([str(x) for x in df['Destination'].dropna().unique()])
        airlines = ['All'] + sorted([str(x) for x in df['Airline'].dropna().unique()])
        classes = ['All'] + sorted([str(x) for x in df['Travel_Class'].dropna().unique()])

        with col1:
            selected_source = st.selectbox("Origin", sources, key="exp_src")
        with col2:
            selected_dest = st.selectbox("Destination", dests, key="exp_dst")
        with col3:
            selected_airline = st.selectbox("Airline", airlines, key="exp_air")
        with col4:
            selected_class = st.selectbox("Travel Class", classes, key="exp_cls")

        col5, col6, col7, col8 = st.columns(4)
        seasons = ['All'] + sorted([str(x) for x in df['Season'].dropna().unique()])
        stops = ['All', '0 (Non-stop)', '1 Stop', '2 Stops']
        channels = ['All'] + sorted([str(x) for x in df['Booking_Channel'].dropna().unique()])

        with col5:
            selected_season = st.selectbox("Season", seasons, key="exp_sea")
        with col6:
            selected_stop = st.selectbox("Stops", stops, key="exp_stp")
        with col7:
            selected_channel = st.selectbox("Booking Channel", channels, key="exp_chn")
        with col8:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            st.button("Reset Filters", use_container_width=True, on_click=reset_explore_filters)

        st.markdown('</div>', unsafe_allow_html=True)

    filtered_df = df[df['Price_clean'].notnull() & (df['Price_clean'] > 0)].copy()

    if selected_source != 'All':
        filtered_df = filtered_df[filtered_df['Source'] == selected_source]
    if selected_dest != 'All':
        filtered_df = filtered_df[filtered_df['Destination'] == selected_dest]
    if selected_airline != 'All':
        filtered_df = filtered_df[filtered_df['Airline'] == selected_airline]
    if selected_class != 'All':
        filtered_df = filtered_df[filtered_df['Travel_Class'] == selected_class]
    if selected_season != 'All':
        filtered_df = filtered_df[filtered_df['Season'] == selected_season]
    if selected_stop == '0 (Non-stop)':
        filtered_df = filtered_df[filtered_df['Total_Stops_num'] == 0]
    elif selected_stop == '1 Stop':
        filtered_df = filtered_df[filtered_df['Total_Stops_num'] == 1]
    elif selected_stop == '2 Stops':
        filtered_df = filtered_df[filtered_df['Total_Stops_num'] == 2]
    if selected_channel != 'All':
        filtered_df = filtered_df[filtered_df['Booking_Channel'] == selected_channel]

    st.markdown(f"<p style='color: {THEME['text_secondary']}; font-size: 0.9rem;'>Showing <b>{len(filtered_df):,}</b> flights matching selected criteria.</p>", unsafe_allow_html=True)

    if filtered_df.empty:
        st.warning("No flights match the selected combination of filters. Please broaden your selection.")
        return

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.markdown('<div class="fb-glass-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_price_distribution(filtered_df, "Price Distribution"), use_container_width=True)
        st.markdown(f"<p style='font-size: 0.83rem; color: {THEME['text_secondary']}; margin-top: 4px;'><b>What this shows:</b> Fare dispersion across filtered flights reveals price density and outliers.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row1_col2:
        st.markdown('<div class="fb-glass-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_airline_prices(filtered_df, "Airline Typical Fares"), use_container_width=True)
        st.markdown(f"<p style='font-size: 0.83rem; color: {THEME['text_secondary']}; margin-top: 4px;'><b>What this shows:</b> Relative typical fare differences between operating carriers.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.markdown('<div class="fb-glass-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_lead_time_curve(filtered_df, "Days Before Departure vs. Price"), use_container_width=True)
        st.markdown(f"<p style='font-size: 0.83rem; color: {THEME['text_secondary']}; margin-top: 4px;'><b>What this shows:</b> Advance booking window impact on typical ticket prices.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row2_col2:
        st.markdown('<div class="fb-glass-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_travel_class_prices(filtered_df, "Travel Class Typical Fares"), use_container_width=True)
        st.markdown(f"<p style='font-size: 0.83rem; color: {THEME['text_secondary']}; margin-top: 4px;'><b>What this shows:</b> Price multipliers associated with premium cabin seating.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
