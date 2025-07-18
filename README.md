# 📊 COVID-19 Impact Analysis (United States, 2017–2022)

This Streamlit app visualizes the economic and social impact of the COVID-19 pandemic in the United States between 2017 and 2022 using real-world data on:

- 🦠 New COVID-19 cases  
- 🏢 Workplace mobility (Google Mobility Reports)  
- 📈 S&P 500 stock market index

🔗 **Live App:** [covit19-impact-analysis.streamlit.app](https://covit19-impact-analysis-a9mxvwcrgxarlfutoe5ufy.streamlit.app/)

---

## 🎯 Purpose

This project helps visualize how COVID-19 outbreaks and lockdown policies affected:
- Human movement (mobility to workplaces)
- Stock market behavior (S&P 500)
- Public health dynamics (infection waves)

The goal is to support **data-driven storytelling** with simple visual insights for analysts, researchers, and the public.

---

## 📁 Project Structure

Covit19-Impact-Analysis/
│
├── covit19_impact_app.py ← Streamlit app
├── requirements.txt ← Python dependencies
├── README.md ← Project overview (this file)
├── .gitignore ← Ignored files
│
├── data/ ← Raw datasets
│ ├── google_mobility.csv
│ ├── owid_covid_data.csv
│ └── sp500_data.csv
│
├── figures/ ← Auto-generated charts (optional)
├── report/ ← Analysis summary + insights
│ ├── summary.md
│ ├── visual_insights.md
│ └── merged_data_preview.csv 


---

## 📊 Features

- 📅 **Year slider** to explore trends from 2017 to 2022
- 📈 Dual-axis line charts:
  - COVID-19 cases (left Y-axis)
  - Mobility and S&P 500 prices (right Y-axis)
- 📥 Downloadable merged dataset
- 🧾 Toggle full data table preview

