import streamlit as st
import pandas as pd
import numpy as np
import seaborn as plt
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# 1. ඩේටාබේස් කනෙක්ෂන් එක (ඔයා පාවිච්චි කරන DB URL එක මෙතැනට දෙන්න)
# උදා: postgresql://username:password@localhost:5432/dbname
DB_URL = "postgresql://postgres:admin123@localhost:5432/cropPriceWeather_db" 
engine = create_engine(DB_URL)

st.set_page_config(page_title="Agricultural Price Prediction Dashboard", layout="wide")

st.title("🌾 Agricultural Data Platform & Price Prediction Dashboard")
st.write("කාලගුණ දත්ත සහ වෙළඳපළ මිල ගණන් විශ්ලේෂණය කරමින් අනාගත බෝග මිල පුරෝකථනය කිරීම.")

# 2. ඩේටා ලෝඩ් කරගැනීම
@st.cache_data
def load_data():
    query = """
        SELECT 
            p.date, 
            p.price_avg, 
            w.temp_max, 
            w.temp_min, 
            w.rain_mm, 
            w.humidity, 
            c.name_en AS crop_name, 
            m.name AS market_name
        FROM prices p
        JOIN markets m ON p.market_id = m.market_id
        JOIN crops c ON p.crop_id = c.crop_id
        JOIN weather_daily w ON p.date = w.date AND 
            w.location_id = 'mkt_0' || m.market_id || '_' || LOWER(m.name);
    """
    df = pd.read_sql(query, con=engine)
    df['temp_mean'] = (df['temp_max'] + df['temp_min']) / 2
    return df

df_analysis = load_data()

if df_analysis.empty:
    st.warning("ඩේටාබේස් එකේ මර්ජ් වූ ඩේටා නොමැත. කරුණාකර ඩේටා පරීක්ෂා කරන්න.")
else:
    # 3. Sidebar ෆिल्ටර්ස්
    st.sidebar.header("🔍 පාලක පුවරුව (Filters)")
    selected_market = st.sidebar.selectbox("වෙළඳපළ තෝරන්න (Market)", df_analysis['market_name'].unique())
    selected_crop = st.sidebar.selectbox("බෝගය තෝරන්න (Crop)", df_analysis['crop_name'].unique())

    filtered_df = df_analysis[(df_analysis['market_name'] == selected_market) & (df_analysis['crop_name'] == selected_crop)]

    # 4. ප්‍රධාන තිරයේ දත්ත පෙන්වීම
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(filtered_df))
    col2.metric("Average Price (LKR)", f"Rs. {filtered_df['price_avg'].mean():.2f}" if not filtered_df.empty else "0.00")
    col3.metric("Max Temperature (°C)", f"{filtered_df['temp_max'].mean():.1f}" if not filtered_df.empty else "0.00")

    st.subheader(f"📊 {selected_crop} මිල සහ කාලගුණ ප්‍රවණතා ({selected_market})")
    if not filtered_df.empty:
        st.line_chart(filtered_df.set_index('date')['price_avg'])
    else:
        st.info("මෙම තේරීමට අදාළ දත්ත නොමැත.")

    # 5. Machine Learning Model Training & Prediction
    st.divider()
    st.subheader("🤖 මිල පුරෝකථන ආකෘතිය (Price Prediction Model)")

    # Model preparation
    df_model = pd.get_dummies(df_analysis[['temp_mean', 'rain_mm', 'humidity', 'crop_name', 'market_name', 'price_avg']], drop_first=True)
    X = df_model.drop('price_avg', axis=1)
    y = df_model['price_avg']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # User Inputs for Prediction
    st.write("අනාගත කාලගුණ තත්ත්වයන් ඇතුළත් කර අපේක්ෂිත මිල ගණන් ලබා ගන්න:")
    col_i1, col_i2, col_i3 = st.columns(3)
    input_temp = col_i1.slider("සාමාන්‍ය උෂ්ණත්වය (Temp Mean °C)", float(df_analysis['temp_mean'].min()), float(df_analysis['temp_mean'].max()), 28.0)
    input_rain = col_i2.slider("වැස්ස (Rain mm)", float(df_analysis['rain_mm'].min()), float(df_analysis['rain_mm'].max()), 0.0)
    input_hum = col_i3.slider("ආර්ද්‍රතාවය (Humidity %)", float(df_analysis['humidity'].min()), float(df_analysis['humidity'].max()), 75.0)

    if st.button("මිල පුරෝකථනය කරන්න (Predict Price)"):
        # Create a dummy input row matching the training columns structure
        input_data = pd.DataFrame(0, index=[0], columns=X.columns)
        if 'temp_mean' in input_data.columns: input_data['temp_mean'] = input_temp
        if 'rain_mm' in input_data.columns: input_data['rain_mm'] = input_rain
        if 'humidity' in input_data.columns: input_data['humidity'] = input_hum
        
        # Set categorical columns if present in X columns
        crop_col = f"crop_name_{selected_crop}"
        market_col = f"market_name_{selected_market}"
        if crop_col in input_data.columns: input_data[crop_col] = 1
        if market_col in input_data.columns: input_data[market_col] = 1

        predicted_price = rf_model.predict(input_data)[0]
        st.success(f"💡 අපේක්ෂිත පුරෝකථනය කළ මිල ({selected_crop} - {selected_market}): **Rs. {predicted_price:.2f}**")