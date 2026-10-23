-- ==========================================================
-- Crop Price & Weather Intelligence Platform - Database Schema
-- ==========================================================

-- 1. වෙළඳපොළ වගුව (Markets Table)
CREATE TABLE IF NOT EXISTS markets (
    market_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    district VARCHAR(50) NOT NULL,
    lat DECIMAL(9, 6),
    lon DECIMAL(9, 6)
);

-- 2. බෝග වගුව (Crops Table)
CREATE TABLE IF NOT EXISTS crops (
    crop_id VARCHAR(50) PRIMARY KEY,
    name_en VARCHAR(100) NOT NULL,
    name_si VARCHAR(100) NOT NULL,
    unit VARCHAR(20) NOT NULL
);

-- 3. මිල දත්ත වගුව (Prices Table)
CREATE TABLE IF NOT EXISTS prices (
    date DATE NOT NULL,
    market_id VARCHAR(50) REFERENCES markets(market_id),
    crop_id VARCHAR(50) REFERENCES crops(crop_id),
    price_min DECIMAL(10, 2),
    price_max DECIMAL(10, 2),
    price_avg DECIMAL(10, 2),
    source VARCHAR(100),
    PRIMARY KEY (date, market_id, crop_id)
);

-- 4. දෛනික කාලගුණ වගුව (Weather Daily Table)
CREATE TABLE IF NOT EXISTS weather_daily (
    date DATE NOT NULL,
    location_id VARCHAR(50) NOT NULL,
    rain_mm DECIMAL(8, 2),
    temp_max DECIMAL(5, 2),
    temp_min DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    PRIMARY KEY (date, location_id)
);

-- 5. අනාවැකි වගුව (Forecasts Table)
CREATE TABLE IF NOT EXISTS forecasts (
    run_date DATE NOT NULL,
    target_date DATE NOT NULL,
    crop_id VARCHAR(50) REFERENCES crops(crop_id),
    market_id VARCHAR(50) REFERENCES markets(market_id),
    yhat DECIMAL(10, 2),
    lower DECIMAL(10, 2),
    upper DECIMAL(10, 2),
    model_name VARCHAR(50)
);

-- 6. මොඩල් ධාවන වාර්තා (Model Runs Table)
CREATE TABLE IF NOT EXISTS model_runs (
    run_id SERIAL PRIMARY KEY,
    model_name VARCHAR(50),
    params TEXT,
    metrics TEXT,
    trained_on_range VARCHAR(100)
);

-- 7. දත්ත ඇතුළත් කිරීමේ ලොගය (Ingestion Log Table)
CREATE TABLE IF NOT EXISTS ingestion_log (
    run_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(100),
    rows_added INT,
    status VARCHAR(50)
);