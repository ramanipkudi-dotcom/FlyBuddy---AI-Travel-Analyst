"""
FlyBuddy - Price Explorer Page
------------------------------
Interactive multi-attribute data exploration tool with real-time filtering.
"""

import streamlit as st
import pandas as pd
from app.components.theme import THEME
from app.components.header import render_header
from app.components.charts import (
    plot_price_distribution, plot_airline_prices, plot_travel_class_prices,
    plot_stops_vs_price, plot_lead_time_curve, get_base_layout
)
import plotly.express as px

def render_explore_page(df):
    render_header(
        title="Price Explorer",
        subtitle="Discover what drives airfare across routes, airlines, seasons, and booking channels.",
        badge_text="🔍 Interactive Exploration"
    )

    with st.container():
        st.markdown('<div class="fb-card" style="padding: 16px 20px;">', unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 0.82rem; font-weight: 700; color: {THEME['text_muted']}; text-transform: uppercase; margin-bottom: 10px;'>Filter Dataset</div>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        sources = ['All'] + sorted([str(x) for x in df['Source'].dropna().unique()])
        dests = ['All'] + sorted([str(x) for x in df['Destination'].dropna().unique()])
        airlines = ['All'] + sorted([str(x) for x in df['Airline'].dropna().unique()])
        classes = ['All'] + sorted([str(x) for x in df['Travel_Class'].dropna().unique()])

        with col1:
            selected_source = st.selectbox("Origin", sources, index=0)
        with col2:
            selected_dest = st.selectbox("Destination", dests, index=0)
        with col3:
            selected_airline = st.selectbox("Airline", airlines, index=0)
        with col4:
            selected_class = st.selectbox("Travel Class", classes, index=0)

        col5, col6, col7, col8 = st.columns(4)
        seasons = ['All'] + sorted([str(x) for x in df['Season'].dropna().unique()])
        stops = ['All', '0 (Non-stop)', '1 Stop', '2 Stops']
        channels = ['All'] + sorted([str(x) for x in df['Booking_Channel'].dropna().unique()])

        with col5:
            selected_season = st.selectbox("Season", seasons, index=0)
        with col6:
            selected_stop = st.selectbox("Stops", stops, index=0)
        with col7:
            selected_channel = st.selectbox("Booking Channel", channels, index=0)
        with col8:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("Reset Filters", use_container_width=True):
                st.rerun()

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

    st.markdown(f"<p style='color: {THEME['text_muted']}; font-size: 0.9rem;'>Displaying <b>{len(filtered_df):,}</b> matching flights out of 100,000.</p>", unsafe_allow_html=True)

    if filtered_df.empty:
        st.warning("No flights match the selected combination of filters. Please broaden your selection.")
        return

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.markdown('<div class="fb-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_price_distribution(filtered_df, "Filtered Flight Price Distribution"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row1_col2:
        st.markdown('<div class="fb-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_airline_prices(filtered_df, "Airline Median Prices (Filtered)"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.markdown('<div class="fb-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_lead_time_curve(filtered_df, "Days Before Departure vs. Price"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row2_col2:
        st.markdown('<div class="fb-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_travel_class_prices(filtered_df, "Travel Class Median Prices"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="fb-card">', unsafe_allow_html=True)
    sample_size = min(1500, len(filtered_df))
    sample_df = filtered_df.sample(sample_size, random_state=42)
    
    fig_dist = px.scatter(
        sample_df,
        x='Distance_km_numeric',
        y='Price_clean',
        color='Travel_Class',
        opacity=0.6,
        labels={'Distance_km_numeric': 'Flight Distance (km)', 'Price_clean': 'Price (₹)', 'Travel_Class': 'Class'},
        title="<b>Flight Distance (km) vs. Price (₹) by Travel Class</b>",
        color_discrete_map={
            'Economy': THEME['primary_cyan'],
            'Premium Economy': '#38BDF8',
            'Business': THEME['secondary_blue'],
            'First': THEME['deep_navy']
        }
    )
    fig_dist.update_layout(get_base_layout(x_title="Distance (km)", y_title="Price (₹)"))
    st.plotly_chart(fig_dist, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
