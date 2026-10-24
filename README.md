# 🌾 Agricultural Data Platform & Price Prediction Dashboard

A Data Science and Machine Learning web application that analyzes agricultural market prices alongside daily weather data, performs correlation analysis, trains a high-accuracy predictive model, and provides interactive real-time price forecasting.

---

## 🚀 Key Features

- **Data Pipeline & Integration:** Merges historical crop market prices with daily weather data (temperature, rainfall, humidity) using PostgreSQL and SQLAlchemy.
- **Exploratory Data Analysis (EDA):** Visualizes feature relationships and correlation heatmaps between weather indicators and crop pricing trends.
- **Machine Learning Model:** Random Forest Regressor built with `scikit-learn`, achieving an **R² score of 0.88** and a low Mean Squared Error (MSE).
- **Interactive Streamlit Dashboard (`app.py`):**
  - Dynamic filters for markets and crops
  - Real-time trend visualization and statistical metrics
  - Weather sliders (temperature, rainfall, humidity) for instant **AI-powered price predictions**

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python |
| Data Analysis | Pandas, NumPy |
| Machine Learning | Scikit-Learn (Random Forest Regressor) |
| Database & ORM | PostgreSQL, SQLAlchemy, Psycopg |
| Visualization | Matplotlib, Seaborn, Streamlit native charts |
| Web Framework | Streamlit |

---

## 📂 Project Structure

```text
Crop-Price-Weather-Platform/
├── notebooks/          # Jupyter notebooks for EDA & ML experimentation
├── app.py              # Main Streamlit dashboard application
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/crop-price-weather-platform.git
cd crop-price-weather-platform
```

### 2. Install dependencies

```bash
pip install streamlit scikit-learn pandas numpy sqlalchemy "psycopg[binary]" seaborn matplotlib
```

Or, using the requirements file:

```bash
pip install -r requirements.txt
```

### 3. Configure the database connection

Open `app.py` and update the PostgreSQL connection string (`DB_URL`) with your credentials:

```python
DB_URL = "postgresql+psycopg://username:password@localhost:5432/your_database"
```

### 4. Run the dashboard

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

## 👨‍💻 Author

Developed as an advanced agricultural analytics and machine learning solution.