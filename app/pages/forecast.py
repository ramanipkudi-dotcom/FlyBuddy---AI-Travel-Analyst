"""
FlyBuddy - Price Forecast Page
------------------------------
Interactive fare prediction estimator based on trained ML models and route features.
"""

import streamlit as st
import pandas as pd
import numpy as np
from app.components.theme import THEME
from app.components.header import render_header
from app.components.cards import render_kpi_card, render_insight_card
from app.components.charts import get_base_layout
from src.model import predict_flight_price
import plotly.graph_objects as go

def render_forecast_page(df, model_pipeline, metrics):
    render_header(
        title="Price Forecast & Lead-Time Curve",
        subtitle="Estimate flight prices and explore lead-time curves based on historical machine learning models.",
        badge_text="Price Forecast"
    )

    with st.container():
        st.markdown('<div class="fb-glass-card" style="padding: 16px 22px;">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        sources = sorted([str(x) for x in df['Source'].dropna().unique()])
        dests = sorted([str(x) for x in df['Destination'].dropna().unique()])
        airlines = sorted([str(x) for x in df['Airline'].dropna().unique()])
        classes = ['Economy', 'Premium Economy', 'Business', 'First']

        default_from_idx = sources.index(st.session_state.get('active_source', 'Chennai')) if st.session_state.get('active_source', 'Chennai') in sources else 0
        default_to_idx = dests.index(st.session_state.get('active_dest', 'Mumbai')) if st.session_state.get('active_dest', 'Mumbai') in dests else 0
        default_class_idx = classes.index(st.session_state.get('active_class', 'Economy')) if st.session_state.get('active_class', 'Economy') in classes else 0

        with col1:
            sel_src = st.selectbox("Origin", sources, index=default_from_idx, key="fc_src")
        with col2:
            sel_dst = st.selectbox("Destination", dests, index=default_to_idx, key="fc_dst")
        with col3:
            sel_airline = st.selectbox("Airline", airlines, index=0, key="fc_airline")
        with col4:
            sel_class = st.selectbox("Travel Class", classes, index=default_class_idx, key="fc_class")

        col5, col6, col7, col8 = st.columns(4)
        with col5:
            sel_stops = st.selectbox("Stops", [0, 1, 2], index=0, key="fc_stops", format_func=lambda x: "Non-stop" if x==0 else f"{x} Stop(s)")
        with col6:
            sel_season = st.selectbox("Season", ['Summer', 'Monsoon', 'Autumn', 'Winter', 'Spring'], index=0, key="fc_season")
        with col7:
            sel_day = st.selectbox("Day of Week", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], index=2, key="fc_day")
        with col8:
            sel_days_before = st.slider("Days Before Departure", min_value=1, max_value=60, value=25, key="fc_days")

        st.markdown('</div>', unsafe_allow_html=True)

    # Route Distance & Duration Lookup
    route_subset = df[(df['Source'] == sel_src) & (df['Destination'] == sel_dst)]
    est_distance = route_subset['Distance_km_numeric'].median() if not route_subset.empty else 1000.0
    est_duration = route_subset['Duration_minutes'].median() if not route_subset.empty else 120.0
    if sel_stops > 0:
        est_duration += sel_stops * 90.0

    flight_input = {
        'Airline': sel_airline,
        'Source': sel_src,
        'Destination': sel_dst,
        'Travel_Class': sel_class,
        'Total_Stops': str(sel_stops),
        'Total_Stops_num': sel_stops,
        'Duration_minutes': est_duration,
        'Distance_km_numeric': est_distance,
        'Days_Before_Departure_numeric': sel_days_before,
        'Season': sel_season,
        'Weekday': sel_day,
        'Booking_Channel': 'Online Travel Agency (OTA)',
        'Aircraft_Type': 'Boeing 737'
    }

    pred_res = predict_flight_price(model_pipeline, flight_input)
    predicted_price = pred_res['predicted_price'] if isinstance(pred_res, dict) else float(pred_res)
    
    mae = metrics.get('mae', 650.0) if metrics else 650.0
    min_expected = max(1000.0, predicted_price - mae)
    max_expected = predicted_price + mae

    # Key KPI Forecast Cards
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        render_kpi_card("Estimated Fare", f"₹{predicted_price:,.0f}", f"Expected Range: ₹{min_expected:,.0f} - ₹{max_expected:,.0f}")
    with f_col2:
        route_typical = route_subset['Price_clean'].median() if not route_subset.empty else predicted_price
        diff = ((predicted_price - route_typical) / route_typical) * 100 if route_typical > 0 else 0
        diff_str = f"{abs(diff):.1f}% {'higher' if diff > 0 else 'lower'} than route median"
        render_kpi_card("Route Comparison", f"₹{route_typical:,.0f}", diff_str)
    with f_col3:
        mae_pct = (mae / predicted_price) * 100 if predicted_price > 0 else 5.0
        render_kpi_card("Model Confidence", f"±₹{mae:,.0f}", f"Approx ±{mae_pct:.1f}% historical variance")

    # Interactive Lead Time Advance Curve
    st.markdown('<div class="fb-glass-card" style="margin-top: 18px;">', unsafe_allow_html=True)
    days_range = list(range(1, 61, 2))
    curve_prices = []
    for d in days_range:
        inp = flight_input.copy()
        inp['Days_Before_Departure_numeric'] = d
        p_val = predict_flight_price(model_pipeline, inp)
        curve_prices.append(p_val['predicted_price'] if isinstance(p_val, dict) else float(p_val))

    fig_curve = go.Figure()
    fig_curve.add_trace(go.Scatter(
        x=days_range,
        y=curve_prices,
        mode='lines+markers',
        line=dict(color=THEME['primary_cyan'], width=3, shape='spline'),
        marker=dict(size=6, color=THEME['primary_cyan']),
        name='Estimated Fare',
        hovertemplate="Days Before Departure: %{x}d<br>Estimated Fare: ₹%{y:,.0f}<extra></extra>"
    ))
    # Highlight current selected days point
    fig_curve.add_trace(go.Scatter(
        x=[sel_days_before],
        y=[predicted_price],
        mode='markers',
        marker=dict(size=14, color=THEME['secondary_violet'], line=dict(color='#FFFFFF', width=2)),
        name=f'Your Selection ({sel_days_before}d)',
        hovertemplate=f"Selected: {sel_days_before}d<br>Fare: ₹{predicted_price:,.0f}<extra></extra>"
    ))
    fig_curve.update_layout(get_base_layout(
        title=f"Price Forecast vs. Days Before Departure ({sel_src} → {sel_dst}, {sel_class})",
        x_title="Days Before Departure",
        y_title="Estimated Fare (₹)"
    ))
    st.plotly_chart(fig_curve, use_container_width=True)
    st.markdown(f"<p style='font-size: 0.83rem; color: #94A3B8; margin-top: 4px;'><b>What this shows:</b> Advance bookings further away from departure generally yield lower fares compared to last-minute departures.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
