import os

# Create figures directory if not exist
os.makedirs("figures", exist_ok=True)


import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load datasets
mobility = pd.read_csv('data/google_mobility.csv')
covid = pd.read_csv('data/owid_covid_data.csv')
sp500 = pd.read_csv('data/sp500_data.csv', parse_dates=['Date'])

# Convert date columns
mobility['date'] = pd.to_datetime(mobility['date'])
covid['date'] = pd.to_datetime(covid['date'])
sp500 = sp500.rename(columns={'Date': 'date'})
sp500['Close'] = pd.to_numeric(sp500['Close'], errors='coerce')  # Coerce invalid entries to NaN

# Sidebar year selector
st.sidebar.title("📅 Year Filter")
selected_year = st.sidebar.slider("Select Year", 2017, 2022, 2020)

# Filter for 2019 only
start_date = "2017-01-01"
end_date = "2022-12-31"


mobility = mobility[(mobility['date'] >= start_date) & (mobility['date'] <= end_date)]
covid = covid[(covid['date'] >= start_date) & (covid['date'] <= end_date)]
sp500 = sp500[(sp500['date'] >= start_date) & (sp500['date'] <= end_date)]

# Filter for United States
usa_mobility = mobility[mobility['country_region'] == 'United States']
usa_covid = covid[covid['location'] == 'United States']

# Resample monthly
usa_covid_monthly = usa_covid.set_index('date').resample('M').sum(numeric_only=True).reset_index()
usa_mobility_monthly = usa_mobility.set_index('date').resample('M').mean(numeric_only=True).reset_index()
sp500_monthly = sp500.set_index('date').resample('M').median(numeric_only=True).reset_index()
sp500_monthly = sp500_monthly.dropna(subset=['Close']) 

# Merge datasets
merged = pd.merge(usa_covid_monthly, usa_mobility_monthly, on='date', how='inner')
merged_all = pd.merge(merged, sp500_monthly[['date', 'Close']], on='date', how='inner')

# Plot S&P 500 monthly close
plt.plot(sp500_monthly['date'], sp500_monthly['Close'])
plt.title("S&P 500 Monthly Close (2019)")
plt.grid(True)
plt.savefig("figures/S&P_500_Monthly_Close_2017_2022.png")
plt.show()

# Combined plot
plt.figure(figsize=(12, 6))
plt.plot(merged_all['date'], merged_all['new_cases'], label="Monthly COVID-19 Cases", color='red', alpha=0.5)
plt.plot(merged_all['date'], merged_all['Close'], label="S&P 500 Close", color='blue')
plt.plot(merged_all['date'], merged_all['workplaces_percent_change_from_baseline'], label="Workplace Mobility", color='green')
plt.title("Monthly COVID-19 Cases, Stock Market & Mobility (US, 2017-2022)")
plt.xlabel("Date")
plt.ylabel("Value")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("figures/combined_plot_2017_2022.png")
plt.show()

# Dual-Axis Plot
fig, ax1 = plt.subplots(figsize=(12, 6))

# Left Y-axis → COVID-19 Cases
ax1.set_xlabel("Date")
ax1.set_ylabel("Monthly COVID-19 Cases", color='red')
ax1.plot(merged_all['date'], merged_all['new_cases'], label="COVID-19 Cases", color='red', alpha=0.6)
ax1.tick_params(axis='y', labelcolor='red')

# Right Y-axis → S&P 500 and Mobility
ax2 = ax1.twinx()
ax2.set_ylabel("S&P 500 Close / Workplace Mobility (%)", color='blue')
ax2.plot(merged_all['date'], merged_all['Close'], label="S&P 500 Close", color='blue')
ax2.plot(merged_all['date'], merged_all['workplaces_percent_change_from_baseline'], label="Mobility Change (%)", color='green')
ax2.tick_params(axis='y', labelcolor='blue')

# Title and Legends
fig.suptitle("Monthly COVID-19 Cases vs. S&P 500 & Mobility (US, 2017-2022)", fontsize=14)
fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
fig.tight_layout()
plt.grid(True)
plt.savefig("figures/dual_axis_plot_2017_2022.png")
plt.show()

# Streamlit Interface

st.title("📊 COVID-19 Impact Analysis (US, 2017–2022)")
st.markdown("This dashboard visualizes the relationship between **COVID-19 cases**, **workplace mobility**, and the **S&P 500 index**.")

# Line chart
st.subheader("📈 Monthly Trends")

fig, ax1 = plt.subplots(figsize=(12, 5))
ax1.set_xlabel("Date")
ax1.set_ylabel("COVID-19 Cases", color='red')
ax1.plot(merged_all['date'], merged_all['new_cases'], color='red', label='COVID-19 Cases')
ax1.tick_params(axis='y', labelcolor='red')

ax2 = ax1.twinx()
ax2.set_ylabel("Mobility / S&P 500", color='blue')
ax2.plot(merged_all['date'], merged_all['workplaces_percent_change_from_baseline'], color='green', label='Mobility Change (%)')
ax2.plot(merged_all['date'], merged_all['Close'], color='blue', label='S&P 500 Close')
ax2.tick_params(axis='y', labelcolor='blue')

fig.tight_layout()
st.pyplot(fig)

# Show data
if st.checkbox("Show merged data table"):
    st.dataframe(merged_all)

# Download merged data
csv = merged_all.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Download Merged CSV", data=csv, file_name='covid_impact_data.csv', mime='text/csv')