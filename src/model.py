"""
FlyBuddy - Machine Learning Model Module
----------------------------------------
Builds Scikit-learn Pipelines, trains baseline and candidate models,
computes evaluation metrics, and handles price inference.

Why this matters for interviews:
- Baseline (Ridge) provides a simple, interpretable linear benchmark.
- Random Forest captures non-linear interactions (e.g. route + class + booking lead time).
- Preprocessing (Imputation & One-Hot Encoding) is encapsulated in a Pipeline
  to prevent data leakage between train and test splits.
"""

import time
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

NUMERIC_FEATURES = [
    'Duration_minutes',
    'Total_Stops_num',
    'Distance_km_numeric',
    'Days_Before_Departure_numeric',
    'Passenger_Count_numeric'
]

CATEGORICAL_FEATURES = [
    'Airline',
    'Source',
    'Destination',
    'Travel_Class',
    'Season',
    'Weekday',
    'Aircraft_Type',
    'Booking_Channel'
]

def build_preprocessing_pipeline():
    """
    Construct a reusable ColumnTransformer for numeric and categorical features.
    """
    numeric_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='median'))
    ])
    categorical_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, NUMERIC_FEATURES),
            ('cat', categorical_transformer, CATEGORICAL_FEATURES)
        ]
    )
    return preprocessor

def train_and_evaluate_models(df):
    """
    Train Baseline (Ridge) and Main (Random Forest) models.
    Compare their test-set MAE, RMSE, and R2.
    Returns metrics dictionary, trained best pipeline, and sample test evaluation points.
    """
    valid_df = df[df['Price_clean'].notnull() & (df['Price_clean'] > 0)].copy()

    X = valid_df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = valid_df['Price_clean'].astype(float)

    # 80/20 Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    preprocessor = build_preprocessing_pipeline()

    # 1. Baseline Model: Ridge Linear Regression
    baseline_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', Ridge(alpha=1.0))
    ])
    t0 = time.time()
    baseline_pipeline.fit(X_train, y_train)
    baseline_fit_time = round(time.time() - t0, 2)
    baseline_preds = baseline_pipeline.predict(X_test)

    baseline_metrics = {
        'model_name': 'Ridge Linear Regression (Baseline)',
        'mae': round(float(mean_absolute_error(y_test, baseline_preds)), 2),
        'rmse': round(float(np.sqrt(mean_squared_error(y_test, baseline_preds))), 2),
        'r2': round(float(r2_score(y_test, baseline_preds)), 4),
        'fit_time_sec': baseline_fit_time
    }

    # 2. Main Model: Random Forest Regressor
    rf_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=50, max_depth=16, random_state=42, n_jobs=-1))
    ])
    t0 = time.time()
    rf_pipeline.fit(X_train, y_train)
    rf_fit_time = round(time.time() - t0, 2)
    rf_preds = rf_pipeline.predict(X_test)

    rf_metrics = {
        'model_name': 'Random Forest Regressor (Main)',
        'mae': round(float(mean_absolute_error(y_test, rf_preds)), 2),
        'rmse': round(float(np.sqrt(mean_squared_error(y_test, rf_preds))), 2),
        'r2': round(float(r2_score(y_test, rf_preds)), 4),
        'fit_time_sec': rf_fit_time
    }

    # Extract Feature Importances from Random Forest
    rf_model = rf_pipeline.named_steps['regressor']
    cat_encoder = rf_pipeline.named_steps['preprocessor'].named_transformers_['cat'].named_steps['encoder']
    cat_feature_names = cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES).tolist()
    all_feature_names = NUMERIC_FEATURES + cat_feature_names

    importances = rf_model.feature_importances_
    importance_df = pd.DataFrame({
        'feature': all_feature_names,
        'importance': importances
    }).sort_values(by='importance', ascending=False)

    # Group importances by parent feature for clean display
    parent_importance = {}
    for _, row in importance_df.iterrows():
        feat = row['feature']
        imp = row['importance']
        parent = feat
        for cat in CATEGORICAL_FEATURES:
            if feat.startswith(cat + '_'):
                parent = cat
                break
        parent_importance[parent] = parent_importance.get(parent, 0.0) + imp

    parent_importance_df = pd.DataFrame(
        list(parent_importance.items()), columns=['feature', 'importance']
    ).sort_values(by='importance', ascending=False)

    # Select the better model empirically based on lower test MAE / higher R2
    if rf_metrics['mae'] < baseline_metrics['mae']:
        best_pipeline = rf_pipeline
        selected_model_name = 'Random Forest Regressor'
    else:
        best_pipeline = baseline_pipeline
        selected_model_name = 'Ridge Linear Regression'

    sample_indices = np.random.RandomState(42).choice(len(y_test), size=min(1000, len(y_test)), replace=False)
    actual_sample = y_test.iloc[sample_indices].tolist()
    predicted_sample = [round(float(p), 2) for p in rf_preds[sample_indices]]

    evaluation_results = {
        'training_rows': int(len(X_train)),
        'test_rows': int(len(X_test)),
        'selected_model': selected_model_name,
        'baseline': baseline_metrics,
        'random_forest': rf_metrics,
        'top_feature_importances': parent_importance_df.head(10).to_dict(orient='records'),
        'actual_vs_predicted_sample': {
            'actual': actual_sample,
            'predicted': predicted_sample
        }
    }

    return best_pipeline, evaluation_results

def predict_flight_price(pipeline, flight_dict, historical_route_median=None):
    """
    Generate price prediction and contextual comparison for a single flight query.
    """
    input_df = pd.DataFrame([flight_dict])
    
    for col in NUMERIC_FEATURES:
        if col not in input_df.columns:
            input_df[col] = np.nan
    for col in CATEGORICAL_FEATURES:
        if col not in input_df.columns:
            input_df[col] = 'Unknown'

    predicted_price = float(pipeline.predict(input_df[NUMERIC_FEATURES + CATEGORICAL_FEATURES])[0])
    predicted_price = max(500.0, round(predicted_price, 2))

    if historical_route_median and historical_route_median > 0:
        ratio = predicted_price / historical_route_median
        if ratio < 0.85:
            status = 'Lower than typical'
            badge_type = 'good'
        elif ratio > 1.15:
            status = 'Higher than typical'
            badge_type = 'high'
        else:
            status = 'Around typical'
            badge_type = 'typical'
    else:
        status = 'Estimated Market Rate'
        badge_type = 'typical'

    return {
        'predicted_price': predicted_price,
        'price_status': status,
        'badge_type': badge_type
    }
