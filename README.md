# FlyBuddy: Travel Analyst
> *"Travel smarter, not harder."*

FlyBuddy is a modern flight price analytics platform built with Python, Pandas, Scikit-learn, Plotly, and Streamlit. It analyzes real historical flight pricing data (~100,000 records) to uncover cost drivers, identify favorable booking windows, provide explainable recommendations, and estimate airfares.

---

## 1. Product Features & Workflow

```
[ PLAN YOUR NEXT FLIGHT SMARTER ] (Origin, Destination, Travel Class, Date, Passengers)
                 ↓
   [ ANALYSIS LOADING TRANSITION ] (Progressive check of patterns, factors & windows)
                 ↓
    [ PERSONALIZED ROUTE DASHBOARD ] (Typical fare, lowest fare, charts, insights)
                 ↓
    [ PERSISTENT LEFT NAVIGATION ]
    ├── Overview (Key fare indicators, distribution, airline & class comparisons)
    ├── Price Explorer (Multi-attribute reactive filtering)
    ├── Price Factors (What affects your fare?)
    ├── Best Time to Book (When should you book?)
    ├── Price Forecast (Data-driven fare estimate calculator & price trend curve)
    └── Recommendations (Explainable flight ranking)
```

---

## 2. Core Capabilities

1. **Flight Price Overview**: Real-time distributions, typical fares, carrier comparisons, cabin tier breakdowns, and concise graph interpretations.
2. **Price Explorer**: Multi-attribute filtering across airlines, classes, stops, seasons, and channels.
3. **Price Factors**: Clear ranking of what influences flight prices (Duration, Distance, Class, Timing, Airline, Stops) and seasonal heatmap.
4. **Best Time to Book**: Empirical lead-time window analysis showing favorable historical booking periods.
5. **Price Forecast**: Real data-driven fare estimation powered by the trained regression pipeline, expected price ranges, and advance-days fare trend curves.
6. **Recommendations**: Personalized flight options ranked by Best Value, Lowest Price, Fastest, and Fewest Stops.

---

## 3. How to Run

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Launch the Web Application
```bash
python -m streamlit run main.py
```
Open **`http://localhost:8501`** in your browser.
