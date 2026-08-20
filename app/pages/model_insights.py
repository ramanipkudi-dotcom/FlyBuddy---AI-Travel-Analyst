"""
FlyBuddy - Model Insights Page
------------------------------
Displays full machine learning evaluation results: Baseline (Ridge) vs Random Forest,
MAE, RMSE, R², actual vs predicted scatter plot, and explainability notes for recruiters.
"""

import streamlit as st
import pandas as pd
from app.components.theme import THEME
from app.components.header import render_header
from app.components.cards import render_kpi_card, render_insight_card
from app.components.charts import plot_feature_importance, plot_actual_vs_predicted

def render_model_insights_page(metrics):
    render_header(
        title="Model Insights & Evaluation",
        subtitle="Transparent machine learning architecture, evaluation benchmarks, and explainability metrics.",
        badge_text="🧠 ML Evaluation"
    )

    baseline = metrics.get('baseline', {})
    rf = metrics.get('random_forest', {})
    selected_model = metrics.get('selected_model', 'Random Forest Regressor')
    train_rows = metrics.get('training_rows', 73641)
    test_rows = metrics.get('test_rows', 18411)

    st.markdown(f"<h3 style='color: {THEME['deep_navy']}; font-weight: 800; font-size: 1.25rem;'>📈 Test Set Benchmarks</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_kpi_card("Selected Model", selected_model, "Empirically Best")
    with col2:
        render_kpi_card("Mean Absolute Error (MAE)", f"₹{rf.get('mae', 0):,.0f}", f"Baseline: ₹{baseline.get('mae', 0):,.0f}", delta=f"₹{baseline.get('mae', 0) - rf.get('mae', 0):,.0f} better", delta_positive=True)
    with col3:
        render_kpi_card("Root Mean Squared Error", f"₹{rf.get('rmse', 0):,.0f}", f"Baseline: ₹{baseline.get('rmse', 0):,.0f}")
    with col4:
        render_kpi_card("R² Score (Variance Explained)", f"{rf.get('r2', 0):.4f}", f"Baseline: {baseline.get('r2', 0):.4f}")

    st.markdown('<div class="fb-card" style="margin-top: 16px;">', unsafe_allow_html=True)
    st.markdown(f"<h4 style='color: {THEME['deep_navy']}; font-weight: 700; margin-bottom: 12px;'>Model Comparison: Baseline vs. Main Candidate</h4>", unsafe_allow_html=True)
    
    comp_df = pd.DataFrame([
        {
            "Model": "Ridge Linear Regression (Baseline)",
            "MAE (₹)": f"₹{baseline.get('mae', 0):,.2f}",
            "RMSE (₹)": f"₹{baseline.get('rmse', 0):,.2f}",
            "R² Score": f"{baseline.get('r2', 0):.4f}",
            "Fit Time": f"{baseline.get('fit_time_sec', 0)}s",
            "Selection Status": "Baseline Benchmark"
        },
        {
            "Model": "Random Forest Regressor (Main)",
            "MAE (₹)": f"₹{rf.get('mae', 0):,.2f}",
            "RMSE (₹)": f"₹{rf.get('rmse', 0):,.2f}",
            "R² Score": f"{rf.get('r2', 0):.4f}",
            "Fit Time": f"{rf.get('fit_time_sec', 0)}s",
            "Selection Status": "✓ Selected for Production"
        }
    ])
    st.table(comp_df)
    st.markdown('</div>', unsafe_allow_html=True)

    actual_pred_sample = metrics.get('actual_vs_predicted_sample', {})
    if actual_pred_sample.get('actual') and actual_pred_sample.get('predicted'):
        st.markdown('<div class="fb-card">', unsafe_allow_html=True)
        fig_act_pred = plot_actual_vs_predicted(
            actual_pred_sample['actual'],
            actual_pred_sample['predicted'],
            title="Actual vs. Predicted Flight Prices (Holdout Test Set Sample)"
        )
        st.plotly_chart(fig_act_pred, use_container_width=True)
        st.markdown(f"<p style='font-size: 0.82rem; color: {THEME['text_muted']}; margin: 0;'>Points closer to the red dashed 45-degree line indicate accurate pricing predictions across diverse fare ranges.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    top_importances = metrics.get('top_feature_importances', [])
    if top_importances:
        st.markdown('<div class="fb-card">', unsafe_allow_html=True)
        fig_imp = plot_feature_importance(top_importances, title="Global Feature Importance")
        st.plotly_chart(fig_imp, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"<h3 style='color: {THEME['deep_navy']}; font-weight: 800; font-size: 1.25rem; margin-top: 20px;'>💬 Why this Model? (Interview Defense)</h3>", unsafe_allow_html=True)

    with st.expander("Q: Why start with Linear/Ridge Regression as a baseline?"):
        st.write("Linear Regression provides a simple, highly interpretable baseline. It helps determine whether linear relationships between features (like distance and duration) are sufficient before introducing non-linear ensemble models.")

    with st.expander("Q: Why did Random Forest outperform the baseline?"):
        st.write("Flight pricing has strong non-linear interactions (e.g. Travel Class multipliers behave differently across routes, and Days_Before_Departure price escalation is non-linear). Decision trees naturally segment these multi-attribute splits.")

    with st.expander("Q: How did you prevent data leakage?"):
        st.write("All learned transformations (median imputation for numbers, one-hot encoding for categoricals) are encapsulated in a Scikit-learn Pipeline and fitted exclusively on the 80% training split. The 20% test split is only transformed during evaluation.")
