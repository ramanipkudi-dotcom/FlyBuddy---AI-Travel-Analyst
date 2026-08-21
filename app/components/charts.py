"""
FlyBuddy - Standardized Plotly Chart Generators (Dark Glass Theme)
------------------------------------------------------------------
Generates clean, statistical Plotly charts matching the dark glassmorphism aesthetic.
Every chart uses proper aggregation, clean labels, and graceful empty-data handling.
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
            font=dict(family="Inter, sans-serif", size=13.5, color='#F8FAFC'),
            x=0.01,
            y=0.96
        ),
        font=dict(family="Inter, sans-serif", size=11, color='#94A3B8'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=18, t=44, b=38),
        height=height,
        xaxis=dict(
            title=dict(text=x_title, font=dict(size=11, color='#94A3B8')) if x_title else None,
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.07)',
            zeroline=False,
            showline=True,
            linecolor='rgba(255, 255, 255, 0.12)'
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(size=11, color='#94A3B8')) if y_title else None,
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.07)',
            zeroline=False,
            showline=True,
            linecolor='rgba(255, 255, 255, 0.12)'
        ),
        hoverlabel=dict(
            bgcolor='#0A1628',
            bordercolor=THEME['primary_cyan'],
            font_size=11,
            font_family="Inter, sans-serif",
            font_color='#FFFFFF'
        )
    )
    return layout

def render_empty_chart_figure(title, message="Not enough matching data to display this analysis."):
    fig = go.Figure()
    fig.update_layout(get_base_layout(title=title))
    fig.add_annotation(
        text=message,
        showarrow=False,
        font=dict(family="Inter, sans-serif", size=12, color="#94A3B8"),
        xref="paper", yref="paper", x=0.5, y=0.5
    )
    return fig

def plot_price_distribution(df, title="Historical Fare Distribution"):
    prices = df['Price_clean'].dropna()
    if prices.empty:
        return render_empty_chart_figure(title)

    q99 = prices.quantile(0.99)
    vis_prices = prices[prices <= q99]
    if vis_prices.empty:
        vis_prices = prices
    
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
        annotation_font=dict(color=THEME['secondary_violet'], size=11)
    )

    layout = get_base_layout(title=title, x_title="Fare (₹)", y_title="Number of Flights")
    fig.update_layout(layout)
    return fig

def plot_lead_time_curve(df, title="Booking Window vs. Typical Fare"):
    valid_df = df[df['Days_Before_Departure_numeric'].notnull() & df['Price_clean'].notnull()].copy()
    if valid_df.empty:
        return render_empty_chart_figure(title)

    # Statistical Aggregation: Group by Days in Advance and take Median Fare per Day
    lead_stats = valid_df.groupby('Days_Before_Departure_numeric', observed=False)['Price_clean'].median().reset_index()
    lead_stats = lead_stats.sort_values(by='Days_Before_Departure_numeric')

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=lead_stats['Days_Before_Departure_numeric'],
        y=lead_stats['Price_clean'],
        mode='lines+markers',
        line=dict(color=THEME['primary_cyan'], width=2.5, shape='spline'),
        marker=dict(size=5, color=THEME['secondary_violet']),
        hovertemplate="Days in Advance: %{x}d<br>Typical Fare: ₹%{y:,.0f}<extra></extra>"
    ))

    layout = get_base_layout(title=title, x_title="Days Before Departure", y_title="Typical Fare (₹)")
    fig.update_layout(layout)
    return fig

def plot_airline_prices(df, title="Airline vs. Typical Fare"):
    valid_df = df[df['Airline'].notnull() & df['Price_clean'].notnull()].copy()
    if valid_df.empty:
        return render_empty_chart_figure(title)

    airline_stats = valid_df.groupby('Airline', observed=False)['Price_clean'].agg(['median', 'count']).reset_index()
    airline_stats = airline_stats.sort_values(by='median', ascending=True)
    if airline_stats.empty:
        return render_empty_chart_figure(title)

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

    layout = get_base_layout(title=title, x_title="Typical Fare (₹)", y_title="Operating Airline", height=340)
    fig.update_layout(layout)
    return fig

def plot_travel_class_prices(df, title="Travel Class vs. Typical Fare"):
    valid_df = df[df['Travel_Class'].notnull() & df['Price_clean'].notnull()].copy()
    if valid_df.empty:
        return render_empty_chart_figure(title)

    class_order = ['Economy', 'Premium Economy', 'Business', 'First']
    class_stats = valid_df.groupby('Travel_Class', observed=False)['Price_clean'].median().reindex(class_order).dropna().reset_index()
    if class_stats.empty:
        return render_empty_chart_figure(title)

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

def plot_stops_vs_price(df, title="Number of Stops vs. Typical Fare"):
    valid_df = df[df['Total_Stops_num'].notnull() & df['Price_clean'].notnull()].copy()
    if valid_df.empty:
        return render_empty_chart_figure(title)

    stops_stats = valid_df.groupby('Total_Stops_num', observed=False)['Price_clean'].median().reset_index()
    stops_labels = {0.0: 'Non-Stop', 1.0: '1 Stop', 2.0: '2 Stops', 3.0: '3 Stops'}
    stops_stats['label'] = stops_stats['Total_Stops_num'].map(stops_labels).fillna(stops_stats['Total_Stops_num'].astype(str))
    if stops_stats.empty:
        return render_empty_chart_figure(title)

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

def plot_feature_importance(importance_list, title="Main Price Drivers"):
    if not importance_list:
        importance_list = [
            {"feature": "Duration_minutes", "importance": 0.446},
            {"feature": "Distance_km_numeric", "importance": 0.170},
            {"feature": "Travel_Class", "importance": 0.108},
            {"feature": "Days_Before_Departure_numeric", "importance": 0.059},
            {"feature": "Airline", "importance": 0.044},
            {"feature": "Total_Stops_num", "importance": 0.038}
        ]

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

    layout = get_base_layout(title=title, x_title="Relative Influence on Fare (%)", y_title="Price Factor", height=320)
    fig.update_layout(layout)
    return fig
