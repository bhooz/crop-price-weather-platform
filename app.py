import requests
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from fpdf import FPDF

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
    
    api_key = st.secrets["OPENWEATHER_API_KEY"]
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
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📈 Trends & Analytics", "🔮 Real-Time Predictor", "📋 Raw Data & Export", "⚖️ Market Comparison", "📅 Multi-Day Forecast", "⚠️ Weather Advisory & Risks", "📄 PDF Report Generator"])

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
    # --- TAB 4: Market-to-Market Price Comparison ---
    with tab4:
        st.subheader(f"⚖️ Cross-Market Price Comparison for {selected_crop}")
        st.markdown(
            "Compare price variations across different economic centers to identify market arbitrage and price gaps."
        )

        # 1. Filter data for the selected crop across ALL markets
        crop_all_markets_df = df_analysis[
            df_analysis["crop_name"] == selected_crop
        ]

        if not crop_all_markets_df.empty:
            # Group by Market and calculate Average Price
            market_avg_df = (
                crop_all_markets_df.groupby("market_name")["price_avg"]
                .mean()
                .reset_index()
            )
            market_avg_df = market_avg_df.sort_values(
                by="price_avg", ascending=False
            )

            # Display Bar Chart Comparison
            fig_market_comp = px.bar(
                market_avg_df,
                x="market_name",
                y="price_avg",
                color="market_name",
                text_auto=".2f",
                title=f"Average Market Price Comparison: {selected_crop} (LKR/kg)",
                labels={
                    "market_name": "Economic Center / Market",
                    "price_avg": "Average Price (LKR)",
                },
                color_discrete_sequence=px.colors.qualitative.Plotly,
            )
            fig_market_comp.update_layout(showlegend=False)
            st.plotly_chart(fig_market_comp, use_container_width=True)

            st.divider()

            # Time Series Comparison Chart across Markets
            st.markdown("### 📈 Price Trend Comparison Over Time")
            fig_line_comp = px.line(
                crop_all_markets_df,
                x="date",
                y="price_avg",
                color="market_name",
                markers=True,
                title=f"Historical Price Trends Across All Markets for {selected_crop}",
                labels={
                    "date": "Date",
                    "price_avg": "Price (LKR)",
                    "market_name": "Market",
                },
            )
            st.plotly_chart(fig_line_comp, use_container_width=True)

            # Quick Highlights (Highest & Lowest Market)
            highest_mkt = market_avg_df.iloc[0]
            lowest_mkt = market_avg_df.iloc[-1]
            diff_price = highest_mkt["price_avg"] - lowest_mkt["price_avg"]

            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric(
                "Highest Priced Market",
                highest_mkt["market_name"],
                f"LKR {highest_mkt['price_avg']:.2f}",
            )
            col_m2.metric(
                "Lowest Priced Market",
                lowest_mkt["market_name"],
                f"LKR {lowest_mkt['price_avg']:.2f}",
            )
            col_m3.metric("Maximum Price Gap", f"LKR {diff_price:.2f} /kg")
        else:
            st.warning("No market data available for the selected crop.")

    # --- TAB 5: Multi-Day Price Forecasting ---
with tab5:
    st.subheader(
        f"📅 Multi-Day Price Forecasting for {selected_crop} ({selected_market})"
    )
    st.markdown(
        "Forecast future crop prices for the next few days using recursive machine learning projection based on historical lags and trends."
    )

    forecast_days = st.slider(
        "Select Forecast Horizon (Days)", min_value=3, max_value=14, value=7
    )

    if st.button("Generate Multi-Day Forecast", type="primary"):
        if not filtered_df.empty:
            # Get the latest row as starting point
            last_row = filtered_df.iloc[-1].copy()
            last_date = last_row["date"]

            # We need historical prices for lags
            recent_prices = filtered_df["price_avg"].tolist()

            forecast_results = []
            current_date = last_date

            # Get current weather from live weather or last row
            base_temp = (
                temp if temp is not None else last_row.get("temp_mean", 28.0)
            )
            base_humidity = (
                humidity if humidity is not None else last_row.get("humidity", 75.0)
            )
            base_rain = last_row.get("rain_mm", 5.0)

            for i in range(1, forecast_days + 1):
                current_date += pd.Timedelta(days=1)

                # Lags calculation
                lag_1 = recent_prices[-1]
                lag_7 = (
                    recent_prices[-7]
                    if len(recent_prices) >= 7
                    else recent_prices[0]
                )

                # Feature vector matching model training columns
                input_features = pd.DataFrame(
                    [[
                        base_temp,
                        base_rain,
                        base_humidity,
                        current_date.month,
                        current_date.dayofweek,
                        current_date.dayofyear,
                        lag_1,
                        lag_7,
                        base_temp,
                        base_rain * 7,
                    ]],
                    columns=[
                        "temp_mean",
                        "rain_mm",
                        "humidity",
                        "month",
                        "day_of_week",
                        "day_of_year",
                        "price_lag_1",
                        "price_lag_7",
                        "temp_rolling_mean_7",
                        "rain_rolling_sum_7",
                    ],
                )

                pred_price = model.predict(input_features)[0]
                recent_prices.append(pred_price)

                forecast_results.append({
                    "date": current_date,
                    "predicted_price (LKR)": round(pred_price, 2),
                    "market_name": selected_market,
                    "crop_name": selected_crop,
                })

            forecast_df = pd.DataFrame(forecast_results)

            # Display Forecast Table
            st.success(
                f"Successfully generated {forecast_days}-day price forecast!"
            )
            st.dataframe(forecast_df, use_container_width=True)

            # Plot Combined Historical (Last 10 days) + Forecast
            historical_subset = filtered_df.tail(10)[
                ["date", "price_avg", "market_name", "crop_name"]
            ].rename(columns={"price_avg": "predicted_price (LKR)"})
            historical_subset["Type"] = "Historical"

            forecast_plot_df = forecast_df.copy()
            forecast_plot_df["Type"] = "Forecast"

            combined_plot_df = pd.concat(
                [historical_subset, forecast_plot_df], ignore_index=True
            )

            fig_forecast = px.line(
                combined_plot_df,
                x="date",
                y="predicted_price (LKR)",
                color="Type",
                markers=True,
                title=f"{forecast_days}-Day Price Trend & Forecast for {selected_crop} ({selected_market})",
                labels={
                    "date": "Date",
                    "predicted_price (LKR)": "Price (LKR / kg)",
                },
                color_discrete_map={
                    "Historical": "#6c5ce7",
                    "Forecast": "#00b894",
                },
            )
            st.plotly_chart(fig_forecast, use_container_width=True)
        else:
            st.warning("No data available for forecasting.")

    # --- TAB 6: Weather Advisory & Risk Alert System ---
with tab6:
    st.subheader(
        f"⚠️ Smart Weather Advisory & Risk Alert System for {selected_crop}"
    )
    st.markdown(
        "Real-time risk assessment and agricultural advisory based on current live weather conditions and market trends."
    )

    if temp is not None:
        # Display Current Weather Card for context
        col_w1, col_w2, col_w3 = st.columns(3)
        col_w1.metric(
            f"Live Temp ({selected_city})",
            f"{temp}°C",
            delta="Normal" if 20 <= temp <= 32 else "Extreme",
        )
        col_w2.metric(f"Live Humidity", f"{humidity}%")
        col_w3.metric(f"Weather Condition", f"{weather_desc}")

        st.divider()

        # Risk Analysis Logic based on Weather & Crop Type
        st.markdown("### 🔍 Automated Risk & Price Impact Analysis")

        risk_score = 0
        risk_messages = []
        advisory_tips = []

        # Temperature Risks
        if temp > 33:
            risk_score += 2
            risk_messages.append(
                "🔥 **High Temperature Alert:** Excessive heat may cause crop stress, rapid moisture loss, and potential supply shortages, pushing market prices upward."
            )
            advisory_tips.append(
                "Ensure adequate irrigation schedules during early morning or late evening."
            )
        elif temp < 18:
            risk_score += 1
            risk_messages.append(
                "❄️ **Low Temperature / Upcountry Chill:** Unseasonable cold can slow down ripening or harvesting schedules."
            )
            advisory_tips.append(
                "Monitor for frost or cold-induced growth stunting in sensitive crops."
            )
        else:
            risk_messages.append(
                "✅ **Temperature Status:** Favorable temperature range for normal crop growth."
            )

        # Humidity / Rain Risks
        if humidity > 85:
            risk_score += 2
            risk_messages.append(
                "💧 **High Humidity / Fungal Risk:** High moisture levels significantly increase the risk of fungal infections (e.g., blight, root rot) and post-harvest spoilage during transport."
            )
            advisory_tips.append(
                "Apply preventive organic fungicides if necessary and ensure well-ventilated storage."
            )
        else:
            risk_messages.append(
                "✅ **Humidity Status:** Humidity levels are within acceptable operational limits."
            )

        # Display Alerts based on Risk Score
        if risk_score >= 3:
            st.error(
                "🚨 **HIGH RISK ALERT:** Current weather conditions pose a significant threat to crop yield or transport logistics. Expect price volatility!"
            )
        elif risk_score == 1 or risk_score == 2:
            st.warning(
                "⚠️ **MODERATE ADVISORY:** Minor weather anomalies detected. Keep a close eye on market price fluctuations."
            )
        else:
            st.success(
                "✨ **OPTIMAL CONDITIONS:** Current weather conditions are highly favorable for stable agricultural supply and pricing."
            )

        # Show detailed messages
        st.markdown("#### 📋 Weather Impact Details:")
        for msg in risk_messages:
            st.markdown(f"- {msg}")

        st.markdown("---")
        st.markdown(
            "#### 💡 Expert Recommendations & Actionable Advisory Tips:"
        )
        if advisory_tips:
            for tip in advisory_tips:
                st.info(f"💡 {tip}")
        else:
            st.success(
                "💡 Standard farming and storage practices are sufficient under current conditions."
            )

        # Price volatility warning based on historical average
        if not filtered_df.empty:
            avg_historical = filtered_df["price_avg"].mean()
            st.markdown("---")
            st.markdown("### 📊 Market Price Context")
            st.markdown(
                f"The historical average price for **{selected_crop}** in **{selected_market}** is **LKR {avg_historical:.2f} /kg**. Given the current weather conditions in **{selected_city}**, short-term price fluctuations of $\\pm 5\\%-10\\%$ may occur."
            )
    else:
        st.warning(
            "⚠️ Live weather data could not be fetched. Please verify your OpenWeatherMap API key in the sidebar configuration to enable live risk advisories."
        )

    # --- TAB 7: Automated PDF Report Generator ---
    with tab7:
        st.subheader("📄 Automated PDF Report Generator")
        st.markdown(
            "Generate and download an official summary report including price metrics, market comparisons, live weather, and predictions."
        )
    
        def create_pdf_report(
            crop, market, avg_p, max_p, min_p, city_name, city_temp, city_hum
        ):
            pdf = FPDF()
            pdf.add_page()
    
            # Header Title
            pdf.set_font("Arial", "B", 16)
            pdf.set_text_color(108, 92, 231)
            pdf.cell(
                0,
                10,
                "Sri Lanka Agricultural Market & Weather Analytics Report",
                ln=True,
                align="C",
            )
            pdf.set_font("Arial", "I", 10)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(
                0,
                10,
                "Generated via Agricultural Data Platform",
                ln=True,
                align="C",
            )
            pdf.ln(5)
    
            # Target Crop & Market Summary
            pdf.set_font("Arial", "B", 12)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 8, "1. Target Selection Summary", ln=True)
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 6, f" - Selected Crop: {crop}", ln=True)
            pdf.cell(0, 6, f" - Selected Market Center: {market}", ln=True)
            pdf.cell(0, 6, f" - Weather Region: {city_name}", ln=True)
            pdf.ln(4)
    
            # Historical Price Key Indicators
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "2. Historical Price Indicators (LKR/kg)", ln=True)
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 6, f" - Average Price: LKR {avg_p:.2f}", ln=True)
            pdf.cell(0, 6, f" - Highest Recorded Price: LKR {max_p:.2f}", ln=True)
            pdf.cell(0, 6, f" - Lowest Recorded Price: LKR {min_p:.2f}", ln=True)
            pdf.ln(4)
    
            # Live Regional Weather Summary
            pdf.set_font("Arial", "B", 12)
            pdf.cell(
                0, 8, f"3. Live Regional Weather Context ({city_name})", ln=True
            )
            pdf.set_font("Arial", "", 10)
            if city_temp is not None:
                pdf.cell(0, 6, f" - Temperature: {city_temp}°C", ln=True)
                pdf.cell(0, 6, f" - Humidity: {city_hum}%", ln=True)
            else:
                pdf.cell(
                    0,
                    6,
                    " - Live Weather Data: Not Available / API Offline",
                    ln=True,
                )
            pdf.ln(4)
    
                # Multi-Day Forecast Table (If Available)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "4. Multi-Day Forecast Summary", ln=True)
            pdf.set_font("Arial", "", 10)
    
            if "latest_forecast_df" in st.session_state:
                f_df = st.session_state["latest_forecast_df"]
                pdf.cell(
                    0,
                    6,
                    f"Showing generated {len(f_df)}-day forecasted prices:",
                    ln=True,
                )
                pdf.ln(2)
    
                # Table Header
                pdf.set_font("Arial", "B", 9)
                pdf.cell(50, 6, "Date", border=1)
                pdf.cell(50, 6, "Forecasted Price (LKR)", border=1, ln=True)
    
                pdf.set_font("Arial", "", 9)
                for idx, row in f_df.iterrows():
                    pdf.cell(50, 6, str(row["date"]), border=1)
                    pdf.cell(
                        50,
                        6,
                        f"LKR {row['predicted_price (LKR)']:.2f}",
                        border=1,
                        ln=True,
                    )
            else:
                pdf.cell(
                    0,
                    6,
                    " - Note: Generate a Multi-Day Forecast in Tab 5 to include prediction table.",
                    ln=True,
                )
    
            pdf.ln(10)
            pdf.set_font("Arial", "I", 8)
            pdf.cell(
                0,
                5,
                "Confidential Agricultural Analytics Report - Developed for Decision Support.",
                align="C",
            )
    
            # Return bytes output safely
            return bytes(pdf.output())
    
        # Generate & Download Trigger
        if not filtered_df.empty:
            avg_p_val = filtered_df["price_avg"].mean()
            max_p_val = filtered_df["price_avg"].max()
            min_p_val = filtered_df["price_avg"].min()
    
            pdf_bytes = create_pdf_report(
                selected_crop,
                selected_market,
                avg_p_val,
                max_p_val,
                min_p_val,
                selected_city,
                temp,
                humidity,
            )
    
            st.download_button(
                label="📥 Download Official Analytics PDF Report",
                data=pdf_bytes,
                file_name=f"{selected_crop}_{selected_market}_Analytics_Report.pdf",
                mime="application/pdf",
                type="primary",
            )
        else:
            st.warning("Please select a crop and market with available data.")












