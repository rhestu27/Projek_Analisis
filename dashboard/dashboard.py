import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os 

sns.set(style='darkgrid')

hourly_data = pd.read_csv(r'..\data\hour.csv')
daily_data = pd.read_csv(r'..\day.csv')

hourly_data['dteday'] = pd.to_datetime(hourly_data['dteday'])
daily_data['dteday'] = pd.to_datetime(daily_data['dteday'])


with st.sidebar:
    st.image(r"..\sepeda.jpg")
    st.header("Filter Data")
    start_date, end_date = st.date_input(
        "Rentang Waktu", 
        value=[daily_data['dteday'].min(), daily_data['dteday'].max()],
        min_value=daily_data['dteday'].min(),
        max_value=daily_data['dteday'].max()
    )

filtered_daily_data = daily_data[(daily_data['dteday'] >= pd.Timestamp(start_date)) & 
                                 (daily_data['dteday'] <= pd.Timestamp(end_date))]

daily_summary = filtered_daily_data[['dteday', 'cnt']]
daily_summary.rename(columns={'cnt': 'total_rentals'}, inplace=True)

daily_fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(daily_summary['dteday'], daily_summary['total_rentals'], marker='o', color="#90CAF9")
ax.set_title("Total Penyewaan Sepeda Harian", fontsize=16)
ax.set_xlabel("Tanggal", fontsize=12)
ax.set_ylabel("Total Penyewaan", fontsize=12)
ax.grid(True)
st.pyplot(daily_fig)

hourly_data['day_type'] = hourly_data['workingday'].apply(lambda x: 'Hari Kerja' if x == 1 else 'Akhir Pekan')
hourly_avg = hourly_data.groupby(['hr', 'day_type'])['cnt'].mean().reset_index()

hourly_fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=hourly_avg, x='hr', y='cnt', hue='day_type', marker='o', ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda per Jam (Hari Kerja vs Akhir Pekan)", fontsize=16)
ax.set_xlabel("Jam", fontsize=12)
ax.set_ylabel("Rata-rata Penyewaan", fontsize=12)
ax.legend(title="Tipe Hari")
st.pyplot(hourly_fig)

season_avg = daily_data.groupby('season')['cnt'].mean().reset_index()
season_avg['season'] = season_avg['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

season_fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=season_avg, x='season', y='cnt', palette='viridis', ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim", fontsize=16)
ax.set_xlabel("Musim", fontsize=12)
ax.set_ylabel("Rata-rata Penyewaan", fontsize=12)
st.pyplot(season_fig)

weather_avg = hourly_data.groupby('weathersit')['cnt'].mean().reset_index()
weather_avg['weathersit'] = weather_avg['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Mist/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Heavy Rain/Snow'
})

weather_fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=weather_avg, x='weathersit', y='cnt', palette='coolwarm', ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca", fontsize=16)
ax.set_xlabel("Kondisi Cuaca", fontsize=12)
ax.set_ylabel("Rata-rata Penyewaan", fontsize=12)
ax.tick_params(axis='x', rotation=15)
st.pyplot(weather_fig)

weekday_avg = daily_data.groupby('weekday')['cnt'].mean().reset_index()
weekday_avg['weekday'] = weekday_avg['weekday'].map({
    0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
    4: 'Thursday', 5: 'Friday', 6: 'Saturday'
})

weekday_fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=weekday_avg, x='weekday', y='cnt', palette='pastel', ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Hari dalam Seminggu", fontsize=16)
ax.set_xlabel("Hari dalam Minggu", fontsize=12)
ax.set_ylabel("Rata-rata Penyewaan", fontsize=12)
ax.tick_params(axis='x', rotation=15)
st.pyplot(weekday_fig)

st.header("Summary Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = filtered_daily_data['cnt'].sum()
    st.metric("Total Rentals", value=total_rentals)

with col2:
    avg_daily_rentals = filtered_daily_data['cnt'].mean()
    st.metric("Average Daily Rentals", value=round(avg_daily_rentals, 2))

with col3:
    peak_hour = hourly_avg.loc[hourly_avg['cnt'].idxmax()]
    st.metric("Peak Hour", value=f"{int(peak_hour['hr'])}:00 ({round(peak_hour['cnt'], 2)} rentals)")

st.caption('Dashboard penyewaan sepeda')
