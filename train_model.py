"""
FlyBuddy - Standalone Model Training & Artifact Generation Script
----------------------------------------------------------------
Executes the end-to-end training pipeline:
1. Loads raw dataset from data/flight_pricing_dataset.csv
2. Cleans data and standardizes formats
3. Creates engineered features
4. Trains Baseline (Ridge) and Main (Random Forest) models
5. Evaluates metrics (MAE, RMSE, R2)
6. Saves models/price_model.joblib and models/metrics.json
"""

import os
import json
import joblib
import pandas as pd
from src.preprocessing import clean_flight_dataframe
from src.feature_engineering import build_engineered_features
from src.model import train_and_evaluate_models

def main():
    print("=" * 60)
    print("FLYBUDDY - Machine Learning Training Pipeline")
    print("=" * 60)

    dataset_path = 'data/flight_pricing_dataset.csv'
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}")
        return

    print(f"1. Loading raw dataset from {dataset_path}...")
    df_raw = pd.read_csv(dataset_path)
    print(f"   Loaded {len(df_raw):,} rows and {len(df_raw.columns)} columns.")

    print("2. Cleaning and standardizing dataset...")
    df_clean = clean_flight_dataframe(df_raw)

    print("3. Engineering predictive features...")
    df_feat = build_engineered_features(df_clean)

    print("4. Training Baseline (Ridge) and Main (Random Forest) models...")
    best_pipeline, evaluation_results = train_and_evaluate_models(df_feat)

    print("\n=== MODEL EVALUATION SUMMARY ===")
    print(f"Training Samples : {evaluation_results['training_rows']:,}")
    print(f"Test Samples     : {evaluation_results['test_rows']:,}")
    print(f"Selected Model   : {evaluation_results['selected_model']}")
    print(f"Baseline (Ridge) : MAE = INR {evaluation_results['baseline']['mae']:,} | RMSE = INR {evaluation_results['baseline']['rmse']:,} | R^2 = {evaluation_results['baseline']['r2']}")
    print(f"Random Forest    : MAE = INR {evaluation_results['random_forest']['mae']:,} | RMSE = INR {evaluation_results['random_forest']['rmse']:,} | R^2 = {evaluation_results['random_forest']['r2']}")

    os.makedirs('models', exist_ok=True)
    model_save_path = 'models/price_model.joblib'
    metrics_save_path = 'models/metrics.json'

    print(f"\n5. Saving best model pipeline to {model_save_path}...")
    joblib.dump(best_pipeline, model_save_path)

    print(f"6. Saving evaluation metrics to {metrics_save_path}...")
    with open(metrics_save_path, 'w', encoding='utf-8') as f:
        json.dump(evaluation_results, f, indent=2)

    print("\nPipeline execution completed successfully!")
    print("=" * 60)

if __name__ == '__main__':
    main()
