import os
import glob
import pandas as pd
from sqlalchemy import create_engine

# ඩේටාබේස් කනෙක්ෂන් යූආර්එල් එක (ඔයාගේ යූසර්නේම් සහ පාස්වර්ඩ් එක මෙතනට දෙන්න)
# උදාහරණයක් ලෙස: postgresql+psycopg2://postgres:password@localhost:5432/cropPriceWeather_db
DB_USER = "postgres"
DB_PASSWORD = "admin123"  # ඔයාගේ පාස්වර්ඩ් එක මෙතනට දාන්න
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "cropPriceWeather_db"

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def load_weather_data():
    engine = create_engine(DATABASE_URL)
    
    # data/ ෆෝල්ඩරයේ ඇති සියලුම weather CSV ෆයිල් සොයා ගැනීම
    csv_files = glob.glob("data/weather_*.csv")
    
    if not csv_files:
        print("No weather CSV files found in 'data/' folder!")
        return

    for file_path in csv_files:
        print(f"Processing {file_path}...")
        df = pd.read_csv(file_path)
        
        # දත්ත ඩේටාබේස් එකට ඇතුළත් කිරීම (weather_daily වගුවට)
        try:
            df.to_sql('weather_daily', con=engine, if_exists='append', index=False)
            print(f"Successfully loaded {file_path} into database.")
        except Exception as e:
            print(f"Error loading {file_path}: {e}")

if __name__ == "__main__":
    load_weather_data()