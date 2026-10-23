import os
import pandas as pd
import requests
from datetime import datetime

# 1. අපේ ප්‍රධාන වෙළඳපොළවල් 5 ක අක්ෂාංශ සහ දේශාංශ (Lat / Lon)
MARKET_LOCATIONS = {
    "mkt_01_dambulla": {"lat": 7.8557, "lon": 80.6517, "name": "Dambulla"},
    "mkt_02_colombo": {"lat": 6.9271, "lon": 79.8612, "name": "Colombo"},
    "mkt_03_meegoda": {"lat": 6.8778, "lon": 80.0396, "name": "Meegoda"},
    "mkt_04_keppetipola": {"lat": 6.9065, "lon": 80.7937, "name": "Keppetipola"},
    "mkt_05_matara": {"lat": 5.9549, "lon": 80.5550, "name": "Matara"}
}

def fetch_historical_weather(lat, lon, start_date="2021-01-01", end_date=None):
    if not end_date:
        end_date = datetime.today().strftime('%Y-%m-%d')
        
    url = "https://archive-api.open-meteo.com/v1/archive"
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "relative_humidity_2m_mean"],
        "timezone": "Asia/Colombo"
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        daily_data = data.get("daily", {})
        
        df = pd.DataFrame({
            "date": daily_data.get("time"),
            "temp_max": daily_data.get("temperature_2m_max"),
            "temp_min": daily_data.get("temperature_2m_min"),
            "rain_mm": daily_data.get("precipitation_sum"),
            "humidity": daily_data.get("relative_humidity_2m_mean")
        })
        return df
    else:
        print(f"Error fetching data: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    # data/ ෆෝල්ඩරය නැත්නම් එය සාදා ගැනීම
    os.makedirs("data", exist_ok=True)
    
    for mkt_id, info in MARKET_LOCATIONS.items():
        print(f"Fetching weather data for {info['name']} ({mkt_id})...")
        df_weather = fetch_historical_weather(info["lat"], info["lon"], start_date="2021-01-01")
        
        if df_weather is not None:
            df_weather["location_id"] = mkt_id
            file_path = f"data/weather_{mkt_id}.csv"
            
            # CSV ලෙස සේව් කිරීම (මෙතන comment එක ඉවත් කර ඇත)
            df_weather.to_csv(file_path, index=False)
            
            print(f"Successfully saved {len(df_weather)} rows to {file_path}.")
            print("-" * 40)