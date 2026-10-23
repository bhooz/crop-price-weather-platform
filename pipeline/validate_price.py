import pandas as pd
import numpy as np

def validate_and_clean_prices(df):
    """
    මිල දත්ත පිරිසිදු කිරීම සහ Data Quality Rules පරීක්ෂා කිරීම.
    """
    print("Starting data quality checks...")
    
    # 1. අත්‍යවශ්‍ය කඳවුරු (Columns) තියෙනවද බැලීම
    required_cols = ['date', 'market_id', 'crop_id', 'price_min', 'price_max', 'price_avg']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
            
    initial_count = len(df)
    
    # 2. අස්ථානගත හෝ හිස් අගයන් (Missing Values) ඉවත් කිරීම හෝ පිරවීම
    df = df.dropna(subset=['date', 'market_id', 'crop_id', 'price_avg'])
    
    # 3. වැරදි දත්ත හෝ අසාමාන්‍ය අගයන් (Outliers / Negative Prices) ඉවත් කිරීම
    df = df[(df['price_min'] > 0) & (df['price_max'] > 0) & (df['price_avg'] > 0)]
    df = df[df['price_min'] <= df['price_max']] # අවම මිල උපරිම මිලට වඩා වැඩි විය නොහැක
    
    # 4. දින ආකෘතිය (Date Format) නිවැරදි කිරීම
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    
    final_count = len(df)
    print(f"Data Cleaning Complete. Rows processed: {initial_count}, Validated rows: {final_count}")
    
    return df

# උදාහරණයක් ලෙස පරීක්ෂා කිරීම
if __name__ == "__main__":
    # නියැදි දත්ත (Sample Data frame)
    sample_data = pd.DataFrame({
        'date': ['2026-01-01', '2026-01-02', '2026-01-03'],
        'market_id': ['mkt_01_dambulla', 'mkt_02_colombo', 'mkt_01_dambulla'],
        'crop_id': ['crop_01', 'crop_01', 'crop_05'],
        'price_min': [150.0, 200.0, 300.0],
        'price_max': [180.0, 240.0, 350.0],
        'price_avg': [165.0, 220.0, 325.0]
    })
    
    cleaned_df = validate_and_clean_prices(sample_data)
    print(cleaned_df)