"""
FlyBuddy - Standardized Plotly Chart Generators
------------------------------------------------
Generates interactive, accessible Plotly visualizations adhering strictly to
the FlyBuddy Light Blue + Cyan design palette.

Why this matters for interviews:
- Every chart is purposeful and directly answers a specific traveler/analyst question.
- Avoids generic unstyled defaults: consistent typography, grid lines, and tooltips.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from app.components.theme import THEME

def get_base_layout(title=None, x_title=None, y_title=None, height=360):
    """
    Standard layout template for all FlyBuddy Plotly charts.
    """
    layout = dict(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(family="Inter, sans-serif", size=15, color=THEME['deep_navy']),
            x=0.01,
            y=0.96
        ),
        font=dict(family="Inter, sans-serif", size=12, color=THEME['text_muted']),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=20, t=50, b=40),
        height=height,
        xaxis=dict(
            title=dict(text=x_title, font=dict(size=12, color=THEME['text_muted'])) if x_title else None,
            showgrid=True,
            gridcolor=THEME['border'],
            zeroline=False,
            showline=True,
            linecolor=THEME['border']
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(size=12, color=THEME['text_muted'])) if y_title else None,
            showgrid=True,
            gridcolor=THEME['border'],
            zeroline=False,
            showline=True,
            linecolor=THEME['border']
        ),
        hoverlabel=dict(
            bgcolor=THEME['deep_navy'],
            font_size=12,
            font_family="Inter, sans-serif"
        )
    )
    return layout

def plot_price_distribution(df, title="Flight Price Distribution"):
    """
    Chart 1: What does the typical fare distribution look like?
    """
    prices = df['Price_clean'].dropna()
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=prices,
        nbinsx=40,
        marker=dict(
            color=THEME['primary_cyan'],
            line=dict(color='#0891B2', width=1)
        ),
        opacity=0.85,
        hovertemplate="Price Range: ₹%{x:,.0f}<br>Count: %{y:,}<extra></extra>"
    ))
    
    # Add median line
    median_val = prices.median()
    fig.add_vline(
        x=median_val,
        line_width=2,
        line_dash="dash",
        line_color=THEME['secondary_blue'],
        annotation_text=f"Median: ₹{median_val:,.0f}",
        annotation_position="top right"
    )

    layout = get_base_layout(title=title, x_title="Price (₹)", y_title="Number of Flights")
    fig.update_layout(layout)
    return fig

def plot_airline_prices(df, title="Airline vs. Median Price"):
    """
    Chart 2: How do typical prices differ between airlines?
    """
    airline_stats = df.groupby('Airline', observed=False)['Price_clean'].agg(['median', 'count']).reset_index()
    airline_stats = airline_stats[airline_stats['count'] >= 5].sort_values(by='median', ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=airline_stats['Airline'],
        x=airline_stats['median'],
        orientation='h',
        marker=dict(
            color=THEME['secondary_blue'],
            line=dict(color=THEME['deep_navy'], width=0.5)
        ),
        hovertemplate="Airline: %{y}<br>Median Price: ₹%{x:,.0f}<extra></extra>"
    ))

    layout = get_base_layout(title=title, x_title="Median Price (₹)", y_title="Airline", height=380)
    fig.update_layout(layout)
    return fig

def plot_lead_time_curve(df, title="Days Before Departure vs. Price"):
    """
    Chart 3: How does booking lead time relate to historical prices?
    """
    lead_stats = df.groupby('Days_Before_Departure_numeric', observed=False)['Price_clean'].median().reset_index()
    lead_stats = lead_stats.sort_values(by='Days_Before_Departure_numeric')

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=lead_stats['Days_Before_Departure_numeric'],
        y=lead_stats['Price_clean'],
        mode='lines+markers',
        line=dict(color=THEME['primary_cyan'], width=3),
        marker=dict(size=6, color=THEME['deep_navy']),
        hovertemplate="Days Before Departure: %{x}<br>Median Price: ₹%{y:,.0f}<extra></extra>"
    ))

    layout = get_base_layout(title=title, x_title="Days Before Departure", y_title="Median Price (₹)")
    fig.update_layout(layout)
    return fig

def plot_travel_class_prices(df, title="Travel Class vs. Price"):
    """
    Chart 4: How does travel class affect flight prices?
    """
    class_order = ['Economy', 'Premium Economy', 'Business', 'First']
    class_stats = df.groupby('Travel_Class', observed=False)['Price_clean'].median().reindex(class_order).dropna().reset_index()

    colors = [THEME['primary_cyan'], '#38BDF8', THEME['secondary_blue'], THEME['deep_navy']]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=class_stats['Travel_Class'],
        y=class_stats['Price_clean'],
        marker=dict(color=colors[:len(class_stats)]),
        hovertemplate="Class: %{x}<br>Median Price: ₹%{y:,.0f}<extra></extra>"
    ))

    layout = get_base_layout(title=title, x_title="Travel Class", y_title="Median Price (₹)")
    fig.update_layout(layout)
    return fig

def plot_stops_vs_price(df, title="Total Stops vs. Median Price"):
    """
    Chart 5: How does the number of stops relate to price?
    """
    stops_stats = df.groupby('Total_Stops_num', observed=False)['Price_clean'].median().reset_index()
    stops_labels = {0.0: 'Non-Stop (0)', 1.0: '1 Stop', 2.0: '2 Stops', 3.0: '3 Stops'}
    stops_stats['label'] = stops_stats['Total_Stops_num'].map(stops_labels).fillna(stops_stats['Total_Stops_num'].astype(str))

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=stops_stats['label'],
        y=stops_stats['Price_clean'],
        marker=dict(color=['#10B981', THEME['primary_cyan'], THEME['secondary_blue'], THEME['deep_navy']][:len(stops_stats)]),
        hovertemplate="Stops: %{x}<br>Median Price: ₹%{y:,.0f}<extra></extra>"
    ))

    layout = get_base_layout(title=title, x_title="Flight Stops", y_title="Median Price (₹)")
    fig.update_layout(layout)
    return fig

def plot_feature_importance(importance_list, title="Top Price Drivers (Feature Importance)"):
    """
    Chart for ML Model Insights: Feature Importance
    """
    df_imp = pd.DataFrame(importance_list).sort_values(by='importance', ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_imp['feature'],
        x=df_imp['importance'] * 100,
        orientation='h',
        marker=dict(color=THEME['primary_cyan']),
        hovertemplate="Feature: %{y}<br>Relative Importance: %{x:.1f}%<extra></extra>"
    ))

    layout = get_base_layout(title=title, x_title="Relative Importance (%)", y_title="Feature", height=350)
    fig.update_layout(layout)
    return fig

def plot_actual_vs_predicted(actual_vals, pred_vals, title="Actual vs. Predicted Flight Prices (Test Set)"):
    """
    Chart for ML Model Insights: Actual vs Predicted Scatter Plot
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=actual_vals,
        y=pred_vals,
        mode='markers',
        marker=dict(
            color=THEME['secondary_blue'],
            size=5,
            opacity=0.55
        ),
        name="Predictions",
        hovertemplate="Actual: ₹%{x:,.0f}<br>Predicted: ₹%{y:,.0f}<extra></extra>"
    ))

    # Add 45-degree perfect prediction reference line
    max_val = max(max(actual_vals), max(pred_vals))
    fig.add_trace(go.Scatter(
        x=[0, max_val],
        y=[0, max_val],
        mode='lines',
        line=dict(color=THEME['danger'], width=2, dash='dash'),
        name="Perfect Prediction Line"
    ))

    layout = get_base_layout(title=title, x_title="Actual Price (₹)", y_title="Predicted Price (₹)", height=420)
    fig.update_layout(layout)
    return fig
