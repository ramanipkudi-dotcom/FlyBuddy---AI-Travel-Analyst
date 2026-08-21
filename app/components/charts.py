"""
FlyBuddy - Standardized Plotly Chart Generators (Dark Glass Theme)
------------------------------------------------------------------
Generates clean Plotly charts matching the dark glassmorphism aesthetic.
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np
from app.components.theme import THEME

def get_base_layout(title=None, x_title=None, y_title=None, height=330):
    """
    Standard dark glass layout template for all FlyBuddy Plotly charts.
    """
    layout = dict(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(family="Inter, sans-serif", size=13.5, color=THEME['text_primary']),
            x=0.01,
            y=0.96
        ),
        font=dict(family="Inter, sans-serif", size=11, color=THEME['text_secondary']),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=35, r=15, t=42, b=36),
        height=height,
        xaxis=dict(
            title=dict(text=x_title, font=dict(size=11, color=THEME['text_secondary'])) if x_title else None,
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.06)',
            zeroline=False,
            showline=True,
            linecolor='rgba(255, 255, 255, 0.08)'
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(size=11, color=THEME['text_secondary'])) if y_title else None,
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.06)',
            zeroline=False,
            showline=True,
            linecolor='rgba(255, 255, 255, 0.08)'
        ),
        hoverlabel=dict(
            bgcolor='#0F172A',
            bordercolor=THEME['primary_cyan'],
            font_size=11,
            font_family="Inter, sans-serif",
            font_color='#FFFFFF'
        )
    )
    return layout

def plot_price_distribution(df, title="Flight Price Distribution"):
    prices = df['Price_clean'].dropna()
    q99 = prices.quantile(0.99)
    vis_prices = prices[prices <= q99]
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=vis_prices,
        nbinsx=35,
        marker=dict(
            color=THEME['primary_cyan'],
            line=dict(color='rgba(255,255,255,0.2)', width=0.5)
        ),
        opacity=0.85,
        hovertemplate="Price Range: ₹%{x:,.0f}<br>Flights: %{y:,}<extra></extra>"
    ))
    
    median_val = prices.median()
    fig.add_vline(
        x=median_val,
        line_width=1.5,
        line_dash="dash",
        line_color=THEME['secondary_violet'],
        annotation_text=f"Median: ₹{median_val:,.0f}",
        annotation_position="top right",
        annotation_font=dict(color=THEME['secondary_violet'])
    )

    layout = get_base_layout(title=title, x_title="Price (₹)", y_title="Number of Flights")
    fig.update_layout(layout)
    return fig

def plot_airline_prices(df, title="Airline vs. Typical Price"):
    airline_stats = df.groupby('Airline', observed=False)['Price_clean'].agg(['median', 'count']).reset_index()
    airline_stats = airline_stats[airline_stats['count'] >= 5].sort_values(by='median', ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=airline_stats['Airline'],
        x=airline_stats['median'],
        orientation='h',
        marker=dict(
            color=THEME['primary_cyan'],
            line=dict(color='rgba(255,255,255,0.15)', width=0.5)
        ),
        hovertemplate="Airline: %{y}<br>Typical Fare: ₹%{x:,.0f}<extra></extra>"
    ))

    layout = get_base_layout(title=title, x_title="Typical Fare (₹)", y_title="Airline", height=340)
    fig.update_layout(layout)
    return fig

def plot_lead_time_curve(df, title="Days Before Departure vs. Price"):
    lead_stats = df.groupby('Days_Before_Departure_numeric', observed=False)['Price_clean'].median().reset_index()
    lead_stats = lead_stats.sort_values(by='Days_Before_Departure_numeric')

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=lead_stats['Days_Before_Departure_numeric'],
        y=lead_stats['Price_clean'],
        mode='lines+markers',
        line=dict(color=THEME['primary_cyan'], width=2.5),
        marker=dict(size=5, color=THEME['secondary_violet']),
        hovertemplate="Days Before Departure: %{x}<br>Typical Fare: ₹%{y:,.0f}<extra></extra>"
    ))

    layout = get_base_layout(title=title, x_title="Days Before Departure", y_title="Typical Fare (₹)")
    fig.update_layout(layout)
    return fig

def plot_travel_class_prices(df, title="Travel Class vs. Price"):
    class_order = ['Economy', 'Premium Economy', 'Business', 'First']
    class_stats = df.groupby('Travel_Class', observed=False)['Price_clean'].median().reindex(class_order).dropna().reset_index()
    colors = [THEME['primary_cyan'], '#38BDF8', THEME['secondary_violet'], '#C084FC']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=class_stats['Travel_Class'],
        y=class_stats['Price_clean'],
        marker=dict(color=colors[:len(class_stats)]),
        hovertemplate="Class: %{x}<br>Typical Fare: ₹%{y:,.0f}<extra></extra>"
    ))

    layout = get_base_layout(title=title, x_title="Travel Class", y_title="Typical Fare (₹)")
    fig.update_layout(layout)
    return fig

def plot_stops_vs_price(df, title="Stops vs. Typical Price"):
    stops_stats = df.groupby('Total_Stops_num', observed=False)['Price_clean'].median().reset_index()
    stops_labels = {0.0: 'Non-Stop', 1.0: '1 Stop', 2.0: '2 Stops', 3.0: '3 Stops'}
    stops_stats['label'] = stops_stats['Total_Stops_num'].map(stops_labels).fillna(stops_stats['Total_Stops_num'].astype(str))

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=stops_stats['label'],
        y=stops_stats['Price_clean'],
        marker=dict(color=['#34D399', THEME['primary_cyan'], THEME['secondary_violet'], '#FBBF24'][:len(stops_stats)]),
        hovertemplate="Stops: %{x}<br>Typical Fare: ₹%{y:,.0f}<extra></extra>"
    ))

    layout = get_base_layout(title=title, x_title="Number of Stops", y_title="Typical Fare (₹)")
    fig.update_layout(layout)
    return fig

def plot_feature_importance(importance_list, title="What affects flight prices?"):
    friendly_map = {
        'Duration_minutes': 'Flight duration',
        'Distance_km_numeric': 'Flight distance',
        'Travel_Class': 'Travel class',
        'Days_Before_Departure_numeric': 'Days before departure',
        'Airline': 'Operating airline',
        'Weekday': 'Day of week',
        'Destination': 'Destination',
        'Source': 'Origin',
        'Aircraft_Type': 'Aircraft type',
        'Booking_Channel': 'Booking channel',
        'Passenger_Count_numeric': 'Passenger count',
        'Total_Stops_num': 'Number of stops',
        'Season': 'Season'
    }

    df_imp = pd.DataFrame(importance_list).copy()
    df_imp['feature_label'] = df_imp['feature'].map(friendly_map).fillna(df_imp['feature'])
    df_imp = df_imp.sort_values(by='importance', ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_imp['feature_label'],
        x=df_imp['importance'] * 100,
        orientation='h',
        marker=dict(
            color=THEME['primary_cyan'],
            line=dict(color='rgba(255,255,255,0.15)', width=0.5)
        ),
        hovertemplate="Factor: %{y}<br>Relative Influence: %{x:.1f}%<extra></extra>"
    ))

    layout = get_base_layout(title=title, x_title="Relative Influence on Price (%)", y_title="Price Factor", height=320)
    fig.update_layout(layout)
    return fig
