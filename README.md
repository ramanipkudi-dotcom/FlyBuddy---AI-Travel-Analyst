# FlyBuddy — AI Travel Analyst

> *"Travel smarter, not harder."*

FlyBuddy is a data-driven flight price analytics platform built with **Python**, **Pandas**, **Scikit-learn**, **Plotly**, and **Streamlit**. It processes and analyzes **100,000 historical flight records** across 18 major domestic and international hubs to identify historical pricing drivers, compute empirical booking lead-time windows, generate explainable itinerary recommendations, and estimate expected fares via machine learning regression models.

---

## Table of Contents
1. [Overview & Problem Statement](#overview--problem-statement)
2. [Key Features](#key-features)
3. [Architecture & Data Flow](#architecture--data-flow)
4. [Dataset & Data Preprocessing](#dataset--data-preprocessing)
5. [Machine Learning Pipeline](#machine-learning-pipeline)
6. [Feature Calculation Methodology](#feature-calculation-methodology)
7. [Visualizations & Insights](#visualizations--insights)
8. [Technical Stack](#technical-stack)
9. [Project Directory Structure](#project-directory-structure)
10. [Installation & Setup](#installation--setup)
11. [Running the Application](#running-the-application)
12. [Live Demo](#live-demo)
13. [Limitations](#limitations)
14. [Future Improvements](#future-improvements)

---

## Overview & Problem Statement

Flight ticket pricing is notoriously volatile and opaque. Fares fluctuate continuously based on flight duration, route distance, cabin tier, booking lead time, carrier operating models, seasonal periods, and routing stop counts. 

**FlyBuddy** solves this problem by transforming historical flight pricing data into structured, transparent travel intelligence. It enables travelers and analysts to:
- Understand the primary factors influencing ticket prices on specific routes.
- Identify data-backed booking lead-time windows that historically offered lower fares.
- Filter and explore multidimensional flight fare distributions in real time.
- Obtain explainable itinerary recommendations prioritized by value, lowest price, duration, or fewest stops.
- Calculate estimated fares and view advance-days price trend curves using a trained machine learning pipeline.

---

## Key Features

The application is structured into a streamlined landing flow and 7 core analytical sections:

| Feature Section | Primary Purpose & Analytical Deliverables |
| :--- | :--- |
| **Landing Hero** | Flight search parameters (Origin, Destination, Cabin Class, Date, Guests), stats badge, and animated trip analysis initiation. |
| **Overview** | Route-specific summary KPIs (Typical Fare, Lowest Historical Fare, Best Booking Window, Flights Analyzed), 5 core distribution and comparison charts, 3 key takeaway cards, and price factor rankings. |
| **Price Explorer** | Interactive multi-attribute filtering across Origin, Destination, Airline, Class, Season, Stops, and Booking Channel with 1-click filter resetting and real-time chart synchronization. |
| **Price Factors** | Empirical feature importance breakdown derived from the Random Forest model and a full-width Season vs. Weekday Fare Matrix heatmap. |
| **Best Time to Book** | Route- and class-specific empirical lead-time window calculator comparing median fares across 6 discrete booking windows (0–7d, 8–14d, 15–21d, 22–35d, 36–50d, 50d+) with calculated percentage savings. |
| **Price Forecast** | Machine learning fare estimation based on user-selected journey attributes, expected fare uncertainty ranges (±MAE), route median comparison, and an interactive 1–60 day advance price trend curve. |
| **Recommendations** | Explainable flight ranking algorithm evaluating historical flights across *Best Value*, *Lowest Price*, *Fastest Option*, and *Fewest Stops* with transparent reason badges. |
| **About** | Concise methodology documentation detailing data pipelines, calculations, and chart interpretation rules. |

---

## Architecture & Data Flow

```
[ Raw Dataset: flight_pricing_dataset.csv (100,000 rows) ]
                         │
                         ▼
[ Preprocessing: clean_flight_dataframe() (src/preprocessing.py) ]
  • Standardizes airport codes & canonical city names
  • Normalizes durations to minutes & stops to integers
  • Converts dates, numeric types & filters missing records
                         │
                         ▼
[ Feature Engineering: build_engineered_features() (src/feature_engineering.py) ]
  • Constructs composite Route strings (Source -> Destination)
  • Extracts Departure Hour, Minute & Time-of-Day categories
  • Generates Weekend indicators & Lead-Time buckets
                         │
        ┌────────────────┴────────────────────────┐
        ▼                                         ▼
[ Machine Learning Pipeline ]           [ Statistical Aggregation ]
  • ColumnTransformer (Impute + OHE)      • Lead-time window analysis (src/booking_analysis.py)
  • Random Forest Regressor (src/model.py) • Multi-attribute filtering (app/pages/explore.py)
  • Models saved in models/price_model.joblib • Explainable rankings (src/recommendation.py)
        └────────────────┬────────────────────────┘
                         │
                         ▼
[ Interactive UI Presentation Layer (Streamlit + Plotly) ]
  • Visible Glassmorphism & Pure Dark Aviation Theme
  • Interactive Client-Side Background Network & Cursor Trail
  • Synchronized Plotly Charts with 1-line "What this shows:" insights
```

---

## Dataset & Data Preprocessing

### Dataset Overview
The project uses `data/flight_pricing_dataset.csv`, consisting of **100,000 flight observations** covering domestic and international routes across 18 major hubs (e.g., Mumbai, Delhi, Bangalore, Chennai, Kolkata, Hyderabad, Pune, Ahmedabad, Jaipur, Goa, Dubai, Singapore, Bangkok, Doha, London, Frankfurt, New York, Sydney).

### Raw Attributes Used
- `Flight_ID`: Unique flight record identifier.
- `Airline`: Operating air carrier (e.g., IndiGo, Air India, SpiceJet, Vistara, Emirates, etc.).
- `Source` & `Destination`: Origin and destination airport names/IATA codes.
- `Departure_Date` & `Departure_Time`: Scheduled flight departure timestamp.
- `Arrival_Time`: Scheduled flight arrival timestamp.
- `Duration`: Flight duration in mixed text/numerical formats (e.g., `'2h 15m'`, `'135 min'`, `'2.25'`).
- `Total_Stops`: Stop category representation (`'non-stop'`, `'1 stop'`, `'2 stops'`).
- `Distance_km`: Estimated flight distance between city pairs in kilometers.
- `Travel_Class`: Cabin class tier (`Economy`, `Premium Economy`, `Business`, `First`).
- `Days_Before_Departure`: Advance booking lead time in days.
- `Season`: Seasonal classification (`Summer`, `Monsoon`, `Autumn`, `Winter`, `Spring`).
- `Weekday`: Day of the week of scheduled departure.
- `Aircraft_Type`: Equipment classification (e.g., Boeing 737, Airbus A320, Boeing 777).
- `Booking_Channel`: Booking platform category (e.g., Airline Website, OTA, Travel Agent).
- `Passenger_Count`: Number of passengers on the booking record.
- `Price`: Observed ticket price in Indian Rupees (INR / ₹).

### Preprocessing Operations (`src/preprocessing.py`)
1. **City Canonicalization**: Standardizes mixed IATA codes (`BOM`, `DEL`, `BLR`, `MAA`, `CCU`, etc.) and airport strings (`'Mumbai Airport'`) to standard canonical city names.
2. **Duration Normalization**: Parses regex patterns (`(\d+)h (\d+)m`, `(\d+) min`, decimal hours) into continuous floating-point minutes (`Duration_minutes`).
3. **Stop Count Standardisation**: Converts text representations (`'non-stop'`, `'0'`, `'1 stop'`, `'2 stops'`) to integer counts (`0`, `1`, `2`, `3`).
4. **Numeric Coercion**: Casts `Price`, `Days_Before_Departure`, `Distance_km`, and `Passenger_Count` to clean numeric representations, discarding non-positive prices.

---

## Machine Learning Pipeline

### Problem Formulation
- **Task**: Supervised tabular regression to estimate ticket prices based on journey attributes.
- **Target Variable (y)**: `Price_clean` (Continuous fare in INR).
- **Features (X)**:
  - *Numeric Features* (5): `Duration_minutes`, `Total_Stops_num`, `Distance_km_numeric`, `Days_Before_Departure_numeric`, `Passenger_Count_numeric`.
  - *Categorical Features* (8): `Airline`, `Source`, `Destination`, `Travel_Class`, `Season`, `Weekday`, `Aircraft_Type`, `Booking_Channel`.

### Architecture & Preprocessing
Feature transformations are encapsulated inside a Scikit-learn `Pipeline` utilizing a `ColumnTransformer` to guarantee zero data leakage between train and test folds:
- **Numeric Pipeline**: `SimpleImputer(strategy='median')`.
- **Categorical Pipeline**: `SimpleImputer(strategy='most_frequent')` followed by `OneHotEncoder(handle_unknown='ignore', sparse_output=False)`.

### Models Trained & Evaluated (`src/model.py`)
Training was conducted on an 80/20 train/test split (73,641 training samples, 18,411 test samples) using a fixed random seed (`random_state=42`):

| Model Candidate | Model Architecture & Hyperparameters | Test MAE (₹) | Test RMSE (₹) | Test R² Score | Fit Time |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Baseline Benchmark** | `Ridge(alpha=1.0)` | ₹23,807.49 | ₹51,719.56 | 0.5607 | 4.27s |
| **Main ML Model** | `RandomForestRegressor(n_estimators=50, max_depth=16, random_state=42, n_jobs=-1)` | **₹15,441.43** | **₹48,333.92** | **0.6164** | 26.80s |

The **Random Forest Regressor** demonstrated superior predictive performance (reducing MAE by ₹8,366 and increasing R² to 0.6164) due to its capacity to capture non-linear interactions between cabin class tiers, route distances, and advance booking timing.

### Relative Feature Importances
1. **Flight Duration (`Duration_minutes`)**: 44.64%
2. **Route Distance (`Distance_km_numeric`)**: 16.99%
3. **Cabin Class (`Travel_Class`)**: 10.85%
4. **Days Before Departure (`Days_Before_Departure_numeric`)**: 5.89%
5. **Operating Airline (`Airline`)**: 4.41%
6. **Total Stops (`Total_Stops_num`)**: 3.78%
7. **Day of Week (`Weekday`)**: 3.21%
8. **Destination Airport (`Destination`)**: 3.02%
9. **Origin Airport (`Source`)**: 2.89%
10. **Aircraft Type (`Aircraft_Type`)**: 2.01%
11. **Booking Channel (`Booking_Channel`)**: 1.83%

---

## Feature Calculation Methodology

### 1. Route Overview Metrics
- **Typical Fare**: Computed as the statistical **median** (P50) of observed fares for the selected origin, destination, and cabin class. Medians are preferred over arithmetic means to prevent skew from extreme cabin fares.
- **Lowest Historical Fare**: Minimum observed fare within the route-class subset.
- **Flights Analyzed**: Total count of empirical flight observations matching the selected route and class.

### 2. Best Time to Book Lead-Time Analysis (`src/booking_analysis.py`)
Flights for the selected route and cabin class are categorized into 6 empirical advance-booking lead-time bins:
- `Last Minute (0–7d)`
- `Short Notice (8–14d)`
- `Moderate (15–21d)`
- `Advance (22–35d)`
- `Early Bird (36–50d)`
- `Far Advance (50d+)`

For each bin with at least 5 observations, the median price is calculated. The bin with the lowest median price is designated as the **cheapest booking window**, and the potential savings percentage is computed against the overall route median:
$$\text{Savings \%} = \frac{\text{Overall Median Fare} - \text{Window Median Fare}}{\text{Overall Median Fare}} \times 100$$

*Example Empirical Findings*:
- `Chennai → Mumbai (Economy)`: **`Early Bird (36–50d)`** (Median fare: ₹4,497 vs. overall ₹5,600, ~19.7% savings).
- `Delhi → Bangalore (Economy)`: **`Far Advance (50d+)`** (Median fare: ₹6,996 vs. overall ₹9,678, ~27.7% savings).

### 3. Explainable Flight Recommendations (`src/recommendation.py`)
Historical flight options on the selected route are evaluated and ranked based on 4 distinct user priorities:
- **Best Value**: Composite score minimizing a weighted sum of normalized price (50%), normalized duration (30%), and stop count penalty (20%):
  $$\text{Score} = 0.5 \times \frac{\text{Price}}{\max(\text{Price})} + 0.3 \times \frac{\text{Duration}}{\max(\text{Duration})} + 0.2 \times \frac{\text{Stops}}{\max(\text{Stops})}$$
- **Lowest Price**: Ranked in ascending order of `Price_clean`.
- **Fastest Option**: Ranked in ascending order of `Duration_minutes`.
- **Fewest Stops**: Ranked in ascending order of `Total_Stops_num`, breaking ties by price.

---

## Visualizations & Insights

Every chart in FlyBuddy is built with Plotly and features a standardized 1-line **"What this shows:"** takeaway explaining the data:

1. **Historical Fare Distribution**: Histogram showing price density and median threshold marker.
2. **Booking Window vs. Typical Fare**: Aggregated line chart plotting advance days against median fare to reveal lead-time savings curves without axis distortion.
3. **Operating Airline vs. Typical Fare**: Horizontal bar chart comparing typical fares across budget and full-service carriers.
4. **Travel Class vs. Typical Fare**: Bar chart quantifying price multipliers across Economy, Premium Economy, Business, and First class.
5. **Number of Stops vs. Typical Fare**: Bar chart comparing Non-stop vs 1-Stop and 2-Stop itineraries.
6. **Main Price Drivers**: Horizontal bar chart displaying the top relative feature importances from the Random Forest model.
7. **Season vs. Weekday Fare Matrix**: Full-width heatmap showing median prices across days of the week and seasons.
8. **Price Forecast Curve**: Interactive spline curve showing estimated fares from 1 to 60 days before departure with the user's selected lead time highlighted.

---

## Technical Stack

- **Core Language**: Python 3.10+ (tested on Python 3.13)
- **Frontend / Application Framework**: Streamlit (v1.30+)
- **Data Manipulation & Analysis**: Pandas (v2.0+), NumPy (v1.24+)
- **Machine Learning & Pipeline Modeling**: Scikit-learn (v1.3+), Joblib (v1.3+)
- **Interactive Visualizations**: Plotly (v5.15+)
- **Design System**: Dark Glassmorphism, CSS3 Custom Properties, SVG & Canvas Client-Side Engine

---

## Project Directory Structure

```
MIC - AI Travel Analyst/
├── README.md                          # Master technical documentation
├── requirements.txt                   # Project Python dependencies
├── main.py                            # Streamlit entry point and router
├── train_model.py                     # Offline ML model training script
├── .streamlit/
│   └── config.toml                    # Pure dark theme configuration
├── data/
│   └── flight_pricing_dataset.csv     # 100,000-record flight pricing dataset
├── models/
│   ├── price_model.joblib             # Serialized trained Random Forest pipeline
│   └── metrics.json                   # Evaluation metrics & feature importances
├── src/
│   ├── preprocessing.py               # Data cleaning & type normalization
│   ├── feature_engineering.py         # Route, time, and temporal feature extraction
│   ├── model.py                       # ML pipelines, training & inference routines
│   ├── booking_analysis.py            # Empirical lead-time window calculations
│   └── recommendation.py              # Multi-criteria flight ranking algorithms
└── app/
    ├── components/
    │   ├── theme.py                   # Dark glassmorphism CSS & client-side canvas
    │   ├── sidebar.py                 # Clean text sidebar navigation & route card
    │   ├── header.py                  # Standardized content header component
    │   ├── cards.py                   # KPI metrics, insights & recommendation cards
    │   ├── charts.py                  # Plotly chart templates with dark styling
    │   └── loading.py                 # Full-page smooth flight animation loader
    └── pages/
        ├── landing.py                 # Hero landing page & flight search form
        ├── overview.py                # Route overview KPIs, charts & takeaways
        ├── explore.py                 # Multidimensional data explorer with reset
        ├── price_factors.py           # Price drivers ranking & seasonal heatmap
        ├── booking_time.py            # Empirical booking lead-time window analysis
        ├── forecast.py                # ML price estimation & advance curve
        ├── recommendations.py         # Explainable flight ranking cards
        └── about.py                   # How FlyBuddy Works methodology guide
```

---

## Installation & Setup

### Prerequisites
- Python 3.10, 3.11, 3.12, or 3.13 installed.
- `pip` package manager.

### 1. Clone the Repository
```bash
git clone https://github.com/ramanipkudi-dotcom/FlyBuddy---AI-Travel-Analyst.git
cd "FlyBuddy---AI-Travel-Analyst"
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Application

### Launch the Streamlit Web App
```bash
python -m streamlit run main.py
```
Open your browser and navigate to **`http://localhost:8501`**.

### Retrain the Machine Learning Model (Optional)
To retrain the Random Forest and Ridge baseline models from scratch and update `models/price_model.joblib` and `models/metrics.json`:
```bash
python train_model.py
```

---

## Live Demo

- **Hosted URL**: `https://flybuddy-travel-analyst.streamlit.app` *(or your deployed Streamlit Community Cloud URL)*
- **Local URL**: `http://localhost:8501`

---

## Limitations

1. **Observational Historical Data**: All insights, booking windows, and price estimations are derived from historical flight observations. They represent historical pricing distributions and correlations, not financial guarantees of future fares.
2. **No Real-Time GDS/API Integration**: FlyBuddy does not connect to live airline Global Distribution Systems (GDS) or airline reservation APIs. It does not perform live booking execution.
3. **Statistical Aggregation over Raw Extremes**: On long-haul international routes with first-class multi-leg itineraries, raw maximum fares can be high. FlyBuddy relies on median aggregations (P50) to provide realistic estimates and prevent outlier distortion.

---

## Future Improvements

- **Live Flight API Integration**: Ingest real-time airline pricing feeds (e.g., Amadeus, Skyscanner APIs) to compare live spot prices against historical baselines.
- **Multi-City & Round-Trip Optimization**: Extend the recommendation and lead-time analysis engine to complex multi-city and round-trip itineraries.
- **Ancillary Fee Modeling**: Include baggage allowance, seat selection, and meal fees into total cost modeling.
- **Fare Alert Notification System**: Allow users to set target price alerts based on predicted booking windows.

---

## Project Information

- **Project**: FlyBuddy — AI Travel Analyst
- **Author**: Rama Nipakudi
- **License**: MIT License
- **Framework**: Streamlit & Scikit-learn
