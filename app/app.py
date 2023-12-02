import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def create_daily_weather_df(df):
    df['dteday'] = pd.to_datetime(df['dteday'])
    df.set_index('dteday', inplace=True)

    daily_weather_df = df.resample(rule='D').agg({
        "cnt_y": "sum",
        "weathersit_x": "mean"
    })
    daily_weather_df.rename(columns={
        "cnt_y": "total_borrowers",
        "weathersit_x": "average_weather"
    }, inplace=True)

    return daily_weather_df.reset_index()

def create_hourly_trend_df(df):
    hourly_trend_df = df.groupby("hr").agg({
        "cnt_y": "mean"
    }).reset_index()
    hourly_trend_df.rename(columns={
        "hr": "hour",
        "cnt_y": "average_borrowers"
    }, inplace=True)

    return hourly_trend_df

data = pd.read_csv("dicoding_data.csv")

with st.sidebar:
    st.subheader('Filter Cuaca')
    selected_weather = st.selectbox('Pilih Kondisi Cuaca', data['weathersit_x'].unique())

    st.subheader('Filter Jam')
    selected_hour = st.slider('Pilih Jam', min_value=0, max_value=23, step=1)

main_df_filtered = data[(data["weathersit_x"] == selected_weather) & (data["hr"] == selected_hour)]

# Pertanyaan 1: Pengaruh Cuaca terhadap Jumlah Peminjam Sepeda
st.subheader('Pertanyaan 1: Pengaruh Cuaca terhadap Jumlah Peminjam Sepeda')
daily_weather_df = create_daily_weather_df(data)
daily_weather_df_filtered = daily_weather_df[daily_weather_df['average_weather'] == selected_weather]
fig_weather, ax_weather = plt.subplots(figsize=(16, 8))
ax_weather.plot(
    daily_weather_df_filtered["dteday"],
    daily_weather_df_filtered["total_borrowers"],
    marker='o',
    linewidth=2,
    color="#FFA07A"  
)
ax_weather.tick_params(axis='y', labelsize=20)
ax_weather.tick_params(axis='x', labelsize=15)
ax_weather.set_title('Jumlah Peminjam Sepeda Harian berdasarkan Cuaca', fontsize=20)
ax_weather.set_xlabel('Tanggal', fontsize=15)
ax_weather.set_ylabel('Jumlah Peminjam Sepeda', fontsize=15)

# Pertanyaan 2: Tren Penggunaan Sepeda berdasarkan Jam
st.subheader('Pertanyaan 2: Tren Penggunaan Sepeda berdasarkan Jam')
hourly_trend_df = create_hourly_trend_df(data)
fig_hourly, ax_hourly = plt.subplots(figsize=(16, 8))
sns.barplot(
    x="hour",
    y="average_borrowers",
    data=hourly_trend_df,
    color="#87CEFA"
)
ax_hourly.tick_params(axis='y', labelsize=15)
ax_hourly.tick_params(axis='x', labelsize=12)
ax_hourly.set_title('Tren Penggunaan Sepeda berdasarkan Jam', fontsize=20)
ax_hourly.set_xlabel('Jam', fontsize=15)
ax_hourly.set_ylabel('Rata-rata Jumlah Peminjam Sepeda', fontsize=15)

# Pertanyaan 3: Bagaimana distribusi kelembapan (hum_y) selama beberapa bulan terakhir?
st.subheader('Pertanyaan 3: Bagaimana distribusi kelembapan (hum_y) selama beberapa bulan terakhir?')
fig_humidity, ax_humidity = plt.subplots(figsize=(16, 8))
sns.histplot(data['hum_y'], bins=20, kde=True, color="#6A5ACD")
ax_humidity.set_title('Distribusi Rata-rata Kelembapan', fontsize=20)
ax_humidity.set_xlabel('Kelembapan', fontsize=15)
ax_humidity.set_ylabel('Jumlah', fontsize=15)

# Menampilkan semua plot
st.pyplot(fig_weather)
st.pyplot(fig_hourly)
st.pyplot(fig_humidity)
