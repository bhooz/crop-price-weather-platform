# Crop Price & Weather Intelligence Platform - Data Inventory

This document tracks all candidate data sources, target crops, wholesale market hubs, and data specifications for the **Crop Price & Weather Intelligence Platform for Sri Lankan Farmers**.

---

## 1. Target Crop Varieties (10 Crops)

The selected crops cover key vegetable classifications, field crops, tubers, and staple grains representing Sri Lanka's agricultural supply chain.

| Crop ID | Crop Name (English) | Crop Name (Sinhala) | Category | Typical Production / Market Dynamics |
| :--- | :--- | :--- | :--- | :--- |
| `crop_01` | Tomato | තක්කාලි | Upcountry / Lowcountry Vegetable | Highly perishable, high price volatility, daily trade volume |
| `crop_02` | Brinjal / Eggplant | බටු | Lowcountry Vegetable | Widespread production and demand across all provinces |
| `crop_03` | Carrot | කැරට් | Upcountry Vegetable | Central highlands supply chain (Nuwara Eliya, Badulla) |
| `crop_04` | Green Beans | බෝංචි | Upcountry Vegetable | High urban consumer market demand, short harvest cycle |
| `crop_05` | Big Onion | ලොකු ලූණු | Field Crop / Import Sensitive | Local Yala season harvest vs. import tariffs and market flow |
| `crop_06` | Potato | අර්තාපල් | Field Crop / Tuber | Key commercial cash crop in Nuwara Eliya and Badulla |
| `crop_07` | Red Onion | රතු ලූණු | Field Crop | Major production in Northern (Jaffna) and Eastern provinces |
| `crop_08` | Green Chilli | අමු මිරිස් | Field Crop / Spice | Highly sensitive to rainfall/weather fluctuations and localized supply |
| `crop_09` | Pumpkin | වට්ටක්කා | Lowcountry Vegetable | Long shelf-life, transported across long-distance distribution routes |
| `crop_10` | Rice (Nadu / Samba) | සහල් (නාඩු / සම්බා) | Staple Grain | Primary staple crop reflecting national food policy and price caps |

---

## 2. Target Wholesale Markets (5 Key Economic Hubs)

These primary economic hubs represent major collection points in production zones and primary retail/wholesale distribution centers across the island.

| Market ID | Market Name | District / Province | Role & Geographical Scope | Target Data Frequency |
| :--- | :--- | :--- | :--- | :--- |
| `mkt_01` | Dambulla Dedicated Economic Centre | Matale (Central) | Primary national wholesale and redistribution hub for all island regions | Daily / Weekly |
| `mkt_02` | Colombo Manning Market / Narahenpita | Colombo (Western) | Main urban consumer demand center and wholesale trade terminus | Daily / Weekly |
| `mkt_03` | Meegoda Dedicated Economic Centre | Colombo / Kalutara | Major distribution hub servicing Western and Southern coastal markets | Daily / Weekly |
| `mkt_04` | Keppetipola Dedicated Economic Centre | Badulla (Uva) | Primary highland vegetable collection and dispatch hub | Daily / Weekly |
| `mkt_05` | Thambuttegama / Matara Economic Hub | Anuradhapura / Matara | Key regional collection and retail distribution point | Daily / Weekly |

---

## 3. Data Sources & Specifications

| Data Domain | Candidate Sources | Available Format | Target Historical Span | Ingestion Frequency | Access / License Terms |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Market Wholesale Prices** | Hector Kobbekaduwa Agrarian Research and Training Institute (HARTI), Department of Agriculture bulletins, Central Bank reports | PDF bulletins, HTML tables | 3+ Years (2021 – 2026) | Daily / Weekly | Public Domain / Open Educational Access |
| **Daily Weather Indicators** | Open-Meteo API, NASA POWER | REST API (JSON / CSV) | 3+ Years (2021 – 2026) | Daily | Open Access (CC-BY 4.0) |
| **Production & Seasonal Context** | Department of Census & Statistics, Department of Agriculture | PDF / Excel reports | Bi-annual (Maha / Yala seasons) | Seasonal | Public Domain |
| **Calendar & Event Features** | National Holiday Calendars, Festive Seasons | JSON / Static CSV | 3+ Years | Annual static update | Public Domain |

---

## 4. Initial Data Validation & Quality Rules

1. **Unit Standardization:** Standardize all price records to Price per Kilogram ($\text{LKR/kg}$). Convert wholesale bag/sack weights ($10\text{kg}$, $50\text{kg}$) accordingly.
2. **Missing Data Handling:** Apply forward-fill or linear interpolation for missing daily prices up to 3 consecutive days; flag gaps longer than 3 days.
3. **Outlier Detection:** Flag price jumps $> 50\%$ day-over-day for manual/secondary source verification.
4. **Weather Alignment:** Map weather metrics (rainfall in $\text{mm}$, max/min temperature in $^\circ\text{C}$, relative humidity in $\%$) using the latitude and longitude coordinates of each economic center's district.