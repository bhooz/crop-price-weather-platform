-- 1. වෙළඳපොළ 5 සඳහා දත්ත ඇතුළත් කිරීම (Markets Seed Data)
INSERT INTO markets (market_id, name, district, lat, lon) VALUES
('mkt_01_dambulla', 'Dambulla Dedicated Economic Centre', 'Matale', 7.8557, 80.6517),
('mkt_02_colombo', 'Colombo Manning Market / Narahenpita', 'Colombo', 6.9271, 79.8612),
('mkt_03_meegoda', 'Meegoda Dedicated Economic Centre', 'Colombo', 6.8778, 80.0396),
('mkt_04_keppetipola', 'Keppetipola Dedicated Economic Centre', 'Badulla', 6.9065, 80.7937),
('mkt_05_matara', 'Thambuttegama / Matara Economic Hub', 'Matara', 5.9549, 80.5550)
ON CONFLICT (market_id) DO NOTHING;

-- 2. බෝග 10 සඳහා දත්ත ඇතුළත් කිරීම (Crops Seed Data)
INSERT INTO crops (crop_id, name_en, name_si, unit) VALUES
('crop_01', 'Tomato', 'තක්කාලි', 'Kg'),
('crop_02', 'Brinjal / Eggplant', 'බටු', 'Kg'),
('crop_03', 'Carrot', 'කැරට්', 'Kg'),
('crop_04', 'Green Beans', 'බෝංචි', 'Kg'),
('crop_05', 'Big Onion', 'ලොකු ලූණු', 'Kg'),
('crop_06', 'Potato', 'අර්තාපල්', 'Kg'),
('crop_07', 'Red Onion', 'රතු ලූණු', 'Kg'),
('crop_08', 'Green Chilli', 'අමු මිරිස්', 'Kg'),
('crop_09', 'Pumpkin', 'වට්ටක්කා', 'Kg'),
('crop_10', 'Rice (Nadu / Samba)', 'සහල් (නාඩු / සම්බා)', 'Kg')
ON CONFLICT (crop_id) DO NOTHING;