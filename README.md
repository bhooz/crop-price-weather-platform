# 🌾 Agricultural Data Platform & Price Prediction Dashboard

A Data Science and Machine Learning web application that analyzes agricultural market prices alongside daily weather data, performs correlation analysis, trains a high-accuracy predictive model, and provides interactive real-time price forecasting.

## 🌐 Live Demo

Access the live deployed application here: [Streamlit Cloud App Link](https://crop-price-weather-platform-hvn6dzcn4uthrmmfwjq899.streamlit.app/)

---

## 🚀 Key Features & Dashboard Modules

The platform is structured into **11 interactive and advanced modules (tabs)**:

1. **📈 Trends & Analytics:** Explore historical price trends, moving averages, and market behaviors for various crops.
2. **🔮 Real-Time Predictor:** Predict future crop prices instantly using a trained Machine Learning model (`RandomForestRegressor`) combined with live weather inputs.
3. **📋 Raw Data & Export:** View raw dataset records, filter by date ranges, and export processed data.
4. **⚖️ Market Comparison:** Compare average prices side-by-side across major economic centers (Dambulla, Narahenpita, Manning Market, Kandy, Nuwara Eliya).
5. **📅 Multi-Day Forecast:** Generate recursive multi-day price projections based on historical lags and environmental trends.
6. **⚠️ Weather Advisory & Risks:** Automated risk assessment based on live temperature, humidity, and rainfall to flag fungal risks or price volatility.
7. **📄 PDF Report Generator:** Export comprehensive, professionally styled PDF analytical reports directly from the dashboard.
8. **💰 Profitability Calculator:** Estimate gross revenue, total cultivation costs, net profit, and ROI based on farm size and expected yield.
9. **🗓️ Monthly Seasonality Heatmap:** Visualize historical monthly price variations across markets to identify peak selling seasons.
10. **🤖 ML Performance & Features:** Inspect model evaluation metrics (R² score, RMSE, MAE) and Feature Importance rankings.
11. **🚨 Smart Price Alerts:** Simulate automated volatility triggers and notification feeds based on custom safety thresholds.

---

## 🛠️ Tech Stack & Libraries

| Category | Tools |
|---|---|
| Language | Python |
| Frontend & UI | Streamlit |
| Data Processing & Analysis | Pandas, NumPy |
| Machine Learning | Scikit-Learn (`RandomForestRegressor`) |
| Database & ORM | PostgreSQL, SQLAlchemy, Psycopg |
| Data Visualization | Plotly (interactive charts, heatmaps, bar/line graphs), Matplotlib, Seaborn |
| API Integration | OpenWeatherMap API (live meteorological data) |
| Reporting | FPDF2 (automated PDF generation) |

---

## 📂 Project Structure

```text
Crop-Price-Weather-Platform/
│
├── .streamlit/
│   └── secrets.toml          # API keys configuration
├── data/                     # Raw/Market CSV data files
├── database/                 # SQL schema and seed files
├── docs/                     # Documentation and data inventory
├── ingestion/                # Data ingestion scripts
├── notebooks/                # Jupyter notebooks for EDA
├── pipeline/                 # Database loading & validation scripts
├── app.py                    # Main Streamlit application
├── agricultural_data.csv     # Combined master dataset
├── best_crop_price_model.pkl # Trained Machine Learning model
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/bhooz/crop-price-weather-platform.git
cd crop-price-weather-platform
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install streamlit scikit-learn pandas numpy plotly fpdf2 sqlalchemy "psycopg[binary]" seaborn matplotlib
```

### 3. Configure the database connection

Open `app.py` and update the PostgreSQL connection string (`DB_URL`) with your credentials:

```python
DB_URL = "postgresql+psycopg://username:password@localhost:5432/your_database"
```

### 4. Add your OpenWeatherMap API key

Create `.streamlit/secrets.toml` and add your key:

```toml
OPENWEATHER_API_KEY = "your_api_key_here"
```

### 5. Run the dashboard

```bash
python -m streamlit run app.py
```

---

## 📊 Model Performance

| Metric | Value |
|---|---|
| Algorithm | Random Forest Regressor (`n_estimators=100`) |
| R² Score | 0.88 |
| Mean Squared Error (MSE) | 248.54 |

---

## 👤 Author

* **Kaveesha Gayanjana**
* GitHub: [@bhooz](https://github.com/bhooz)
