# Crop Price & Weather Intelligence Platform for Sri Lankan Farmers

An end-to-end data engineering, analytics, and software project designed to help smallholder farmers and agricultural stakeholders make informed decisions by combining market prices, weather data, and short-term forecasting[cite: 1, 2].

## 🚀 Project Overview
Smallholder farmers often lack timely, trustworthy information on market prices and weather, leading them to sell at suboptimal times or markets while middlemen capture the margins[cite: 2]. This platform bridges that gap through automated data pipelines, exploratory analysis, time-series forecasting, and a bilingual (Sinhala/English) web dashboard[cite: 1, 2].

## 🛠️ Core Tech Stack
* **Language:** Python[cite: 3]
* **Database:** PostgreSQL[cite: 3]
* **Backend API:** FastAPI[cite: 3]
* **Frontend / Dashboard:** Next.js or Streamlit[cite: 3]
* **Modeling:** statsmodels, Prophet, LightGBM / scikit-learn[cite: 3]

## 📁 Repository Structure
crop-price-platform/
│
├── data/           # Raw and processed datasets (gitignored if large)[cite: 5]
├── ingestion/      # Data collection and scraping scripts[cite: 5]
├── pipeline/       # Cleaning and database loading pipelines[cite: 5]
├── notebooks/      # Exploratory Data Analysis (EDA) Jupyter notebooks[cite: 5]
├── models/         # Forecasting models and evaluation scripts[cite: 5]
├── api/            # FastAPI backend application[cite: 5]
├── dashboard/      # Next.js or Streamlit frontend application[cite: 5]
├── tests/          # Unit and integration tests[cite: 5]
├── docs/           # Project documentation and case study[cite: 5]
├── docker-compose.yml
└── README.md
