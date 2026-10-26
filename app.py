import requests
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

# 1. Page Configuration & Layout
st.set_page_config(
    page_title="Agricultural Data Platform & Price Prediction",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Agricultural Market Price Prediction & Analytics Platform")
st.markdown("Analyze market trends, weather impacts, and predict crop prices interactively using Machine Learning.")

# 2. Resource Loading (Using CSV for Cloud Compatibility)

@st.cache_resource
def load_data_and_model():
    # Load trained machine learning model
    model = joblib.load('best_crop_price_model.pkl')

    # Load dataset from CSV file (ready for cloud deployment)
    df = pd.read_csv('agricultural_data.csv')
    df['date'] = pd.to_datetime(df['date'])

    # Ensure temp_mean exists
    if 'temp_mean' not in df.columns and 'temp_max' in df.columns and 'temp_min' in df.columns:
        df['temp_mean'] = (df['temp_max'] + df['temp_min']) / 2
        
    return model, df

# Load model and data safely
try:
    model, df_analysis = load_data_and_model()
    st.sidebar.success("Database & ML Model loaded successfully!")
except Exception as e:
    st.sidebar.error(f"Error loading resources: {e}")
    df_analysis = pd.DataFrame()

# ----------------------------------------------------
# 3. Sidebar - Multi-City Live Weather Integration
# ----------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("🌤️ Regional Live Weather")

cities = {
    "Dambulla": "Dambulla,LK",
    "Nuwara Eliya": "Nuwara Eliya,LK",
    "Colombo": "Colombo,LK",
    "Kandy": "Kandy,LK",
    "Anuradhapura": "Anuradhapura,LK",
}

selected_city = st.sidebar.selectbox("Select City", list(cities.keys()))

@st.cache_data(ttl=600)
def get_city_weather(city_query):
    
    api_key = st.secrets["openweathermap_api_key"]
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_query}&appid={api_key}&units=metric"

    try:
        response = requests.get(
            url, 
            params={"q": city_query, "appid": api_key, "units": "metric"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            weather_desc = data["weather"][0]["description"].capitalize()
            wind_speed = data["wind"]["speed"]
            return temp, humidity, weather_desc, wind_speed
        st.sidebar.caption(f"Weather API Error: {response.status_code} - {response.reason}")
    except Exception as e:
        st.sidebar.caption(f"Error request failed: {e}")
    return None, None, None, None


temp, humidity, weather_desc, wind_speed = get_city_weather(
    cities[selected_city]
)

if temp is not None:
    st.sidebar.metric(
        label=f"Temperature ({selected_city})", value=f"{temp}°C"
    )
    st.sidebar.metric(label="Humidity", value=f"{humidity}%")
    st.sidebar.markdown(f"**Conditions:** {weather_desc}")
    st.sidebar.markdown(f"**Wind Speed:** {wind_speed} m/s")
else:
    st.sidebar.warning(
        "Could not fetch weather data. Please check your OpenWeatherMap API Key."
    )

# 3. Sidebar Filters for Interactive Experience
st.sidebar.header("🎛️ Filter Options")

if not df_analysis.empty:
    selected_market = st.sidebar.selectbox("Select Market", df_analysis['market_name'].unique())
    selected_crop = st.sidebar.selectbox("Select Crop", df_analysis['crop_name'].unique())
    
    # Filter dataframe based on user selection
    filtered_df = df_analysis[(df_analysis['market_name'] == selected_market) & (df_analysis['crop_name'] == selected_crop)]
    filtered_df = filtered_df.sort_values('date')

    # Top-level Metric Cards (KPIs)
    if not filtered_df.empty:
        avg_price = filtered_df['price_avg'].mean()
        max_price = filtered_df['price_avg'].max()
        min_price = filtered_df['price_avg'].min()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Price", f"LKR {avg_price:.2f} /kg")
        col2.metric("Highest Price", f"LKR {max_price:.2f} /kg")
        col3.metric("Lowest Price", f"LKR {min_price:.2f} /kg")
        st.divider()

    # 4. Organizing Dashboard into Clean Tabs
    tab1, tab2, tab3 = st.tabs(["📈 Trends & Analytics", "🔮 Real-Time Predictor", "📋 Raw Data & Export"])

    # --- TAB 1: Trends & Analytics (With Creative Visuals) ---
    with tab1:
        st.subheader(f"Price & Weather Trends for {selected_crop} in {selected_market}")
        
        if not filtered_df.empty:
            # 1. Standard Historical Line Chart for Price Trends
            fig_price = px.line(
                filtered_df, x='date', y='price_avg', 
                title=f"Historical Price Trend ({selected_crop})",
                labels={'date': 'Date', 'price_avg': 'Average Price (LKR)'},
                markers=True
            )
            st.plotly_chart(fig_price, use_container_width=True)
            
            st.divider()
            
            # 2. Creative Visual 1: Animated Bubble Chart
            st.markdown("### 🌟 Animated Weather & Price Dynamics")
            st.markdown("This bubble chart demonstrates how price, temperature, and rainfall interact over time. (Press Play ▶ below)")
            
            filtered_df['month_str'] = filtered_df['date'].dt.strftime('%Y-%m')
            
            fig_animated = px.scatter(
                filtered_df, 
                x='temp_mean', 
                y='price_avg', 
                animation_frame='month_str', 
                animation_group='date',
                size='rain_mm', 
                color='humidity',
                hover_name='date',
                range_x=[filtered_df['temp_mean'].min()-2, filtered_df['temp_mean'].max()+2],
                range_y=[filtered_df['price_avg'].min()-50, filtered_df['price_avg'].max()+50],
                title=f"Animated Weather Impact on {selected_crop} Prices (Bubble Size = Rainfall)",
                labels={
                    'temp_mean': 'Mean Temperature (°C)', 
                    'price_avg': 'Average Price (LKR)',
                    'humidity': 'Humidity (%)',
                    'rain_mm': 'Rainfall (mm)'
                },
                color_continuous_scale='Purples'
            )
            fig_animated.update_layout(transition_duration=1000)
            st.plotly_chart(fig_animated, use_container_width=True)
            
            st.divider()
            
            # 3. Creative Visual 2: Radar Chart (Crop Profile)
            st.markdown("### 🕸️ Crop Environmental & Price Profile (Radar Chart)")
            st.markdown("This radar chart highlights the normalized average metrics for the selected crop.")
            
            crop_profile_df = df_analysis[df_analysis['crop_name'] == selected_crop].agg({
                'price_avg': 'mean',
                'temp_mean': 'mean',
                'rain_mm': 'mean',
                'humidity': 'mean'
            }).reset_index()
            crop_profile_df.columns = ['Metric', 'Value']
            
            categories = ['Avg Price (LKR)', 'Mean Temp (°C)', 'Rainfall (mm)', 'Humidity (%)']
            values = [
                crop_profile_df.loc[crop_profile_df['Metric'] == 'price_avg', 'Value'].values[0] / 5,
                crop_profile_df.loc[crop_profile_df['Metric'] == 'temp_mean', 'Value'].values[0],
                crop_profile_df.loc[crop_profile_df['Metric'] == 'rain_mm', 'Value'].values[0] * 2,
                crop_profile_df.loc[crop_profile_df['Metric'] == 'humidity', 'Value'].values[0]
            ]
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=selected_crop,
                line_color='#6c5ce7'
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, max(values) * 1.2])),
                showlegend=True,
                title=f"Multi-Dimensional Profile for {selected_crop}"
            )
            st.plotly_chart(fig_radar, use_container_width=True)
            
            st.divider()
            
            # 4. Creative Visual 3: Correlation Heatmap
            st.markdown("### 🔥 Factor Correlation Heatmap")
            st.markdown("This heatmap displays the statistical correlation between weather metrics and crop prices.")
            
            corr_cols = ['price_avg', 'temp_mean', 'temp_max', 'temp_min', 'rain_mm', 'humidity']
            available_corr_cols = [col for col in corr_cols if col in filtered_df.columns]
            
            if len(available_corr_cols) > 1:
                corr_matrix = filtered_df[available_corr_cols].corr()
                fig_heatmap = px.imshow(
                    corr_matrix,
                    text_auto=True,
                    color_continuous_scale='Purples',
                    title=f"Correlation Matrix for {selected_crop}",
                    labels=dict(color="Correlation Coefficient")
                )
                fig_heatmap.update_layout(xaxis_title="Features", yaxis_title="Features")
                st.plotly_chart(fig_heatmap, use_container_width=True)
            else:
                st.info("Not enough numeric data columns for correlation calculation.")
            
        else:
            st.warning("No data available for the selected combination.")

    # --- TAB 2: Real-Time Predictor ---
    with tab2:
        st.subheader("🔮 ML-Powered Price Prediction")
        st.markdown("Adjust the parameters below to predict future crop prices.")
        
        col_a, col_b = st.columns(2)
        with col_a:
            input_temp = st.slider("Mean Temperature (°C)", 20.0, 40.0, 28.0)
            input_rain = st.slider("Rainfall (mm)", 0.0, 50.0, 5.0)
            input_humidity = st.slider("Humidity (%)", 40.0, 100.0, 75.0)
            input_month = st.slider("Month", 1, 12, 6)
            
        with col_b:
            input_day_of_week = st.slider("Day of Week (0=Mon, 6=Sun)", 0, 6, 2)
            input_day_of_year = st.slider("Day of Year", 1, 365, 150)
            input_lag_1 = st.number_input("Previous Day Price (Lag 1)", value=float(filtered_df['price_avg'].mean() if not filtered_df.empty else 200.0))
            input_lag_7 = st.number_input("Previous Week Price (Lag 7)", value=float(filtered_df['price_avg'].mean() if not filtered_df.empty else 200.0))
            
        input_temp_roll = st.number_input("7-Day Temp Rolling Mean", value=input_temp)
        input_rain_roll = st.number_input("7-Day Rain Rolling Sum", value=input_rain * 7)

        if st.button("Calculate Predicted Price", type="primary"):
            input_data = pd.DataFrame([[
                input_temp, input_rain, input_humidity,
                input_month, input_day_of_week, input_day_of_year,
                input_lag_1, input_lag_7,
                input_temp_roll, input_rain_roll
            ]], columns=[
                'temp_mean', 'rain_mm', 'humidity', 
                'month', 'day_of_week', 'day_of_year', 
                'price_lag_1', 'price_lag_7', 
                'temp_rolling_mean_7', 'rain_rolling_sum_7'
            ])
            
            predicted_price = model.predict(input_data)[0]
            st.success(f"### Estimated Market Price: LKR {predicted_price:.2f} /kg")

    # --- TAB 3: Raw Data & Export ---
    with tab3:
        st.subheader("📋 Filtered Dataset & CSV Export")
        st.dataframe(filtered_df, use_container_width=True)
        
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv_data,
            file_name=f"{selected_crop}_{selected_market}_price_data.csv",
            mime="text/csv"
        )

