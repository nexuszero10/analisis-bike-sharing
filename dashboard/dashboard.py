import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set gaya visual
sns.set(style='dark')

# ===============================
# Fungsi-fungsi pengolahan data
# ===============================

def get_total_count_by_hour_df(hour_df):
    return hour_df.groupby("hours").agg({"count_rent": "sum"}).reset_index()

def count_by_day_df(day_df):
    return day_df.query('dteday >= "2011-01-01" and dteday < "2012-12-31"')

def total_registered_df(day_df):
    reg_df = day_df.groupby("dteday").agg({"registered": "sum"}).reset_index()
    reg_df.rename(columns={"registered": "register_sum"}, inplace=True)
    return reg_df

def total_casual_df(day_df):
    cas_df = day_df.groupby("dteday").agg({"casual": "sum"}).reset_index()
    cas_df.rename(columns={"casual": "casual_sum"}, inplace=True)
    return cas_df

def sum_order(hour_df):
    return hour_df.groupby("hours").agg({"count_rent": "sum"}).sort_values(by="count_rent", ascending=False).reset_index()

def sum_of_season(day_df):
    return day_df.groupby("season").agg({"count_rent": "sum"}).reset_index()

def sum_of_weather(day_df):
    return day_df.groupby("weather_situation").agg({"count_rent": "sum"}).reset_index()

# ===============================
# Load dan siapkan data
# ===============================

days_df = pd.read_csv("dashboard/day_clean.csv")
hours_df = pd.read_csv("dashboard/hour_clean.csv")

# Konversi tanggal
for col in ["dteday"]:
    days_df[col] = pd.to_datetime(days_df[col])
    hours_df[col] = pd.to_datetime(hours_df[col])

# Sortir data berdasarkan tanggal
days_df.sort_values("dteday", inplace=True)
hours_df.sort_values("dteday", inplace=True)

# ===============================
# Sidebar - filter tanggal
# ===============================

with st.sidebar:
    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg")

    min_date_days = days_df["dteday"].min()
    max_date_days = days_df["dteday"].max()

    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days]
    )

# ===============================
# Filter data berdasarkan input
# ===============================

main_df_days = days_df[(days_df["dteday"] >= pd.to_datetime(start_date)) & 
                       (days_df["dteday"] <= pd.to_datetime(end_date))]
main_df_hour = hours_df[(hours_df["dteday"] >= pd.to_datetime(start_date)) & 
                        (hours_df["dteday"] <= pd.to_datetime(end_date))]

# ===============================
# Proses data
# ===============================

hour_count_df = get_total_count_by_hour_df(main_df_hour)
day_df_count_2011 = count_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season_df = sum_of_season(main_df_days)
weather_df = sum_of_weather(main_df_days)

# ===============================
# Tampilan utama dashboard
# ===============================

st.header("Bike Sharing :sparkles:")
st.subheader("Daily Rental")

# ===============================
# Kartu informasi utama
# ===============================
col1, col2, col3 = st.columns(3)

with col1:
    total_orders = day_df_count_2011["count_rent"].sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df["register_sum"].sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df["casual_sum"].sum()
    st.metric("Total Casual", value=total_sum)

# ===============================
# Line chart: peminjaman harian
# ===============================
st.subheader("Performa penjualan dalam beberapa tahun terakhir")
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    days_df["dteday"],
    days_df["count_rent"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_ylabel("Jumlah Peminjaman")
ax.set_xlabel("Tanggal")
st.pyplot(fig)

# ===============================
# Bar chart: jam tersibuk dan sepi
# ===============================
st.subheader("Jam paling banyak dan paling sedikit penyewaan")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

# Jam tersibuk
sns.barplot(x="hours", y="count_rent", data=sum_order_items_df.head(5), palette=["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"], ax=ax[0])
ax[0].set_title("Jam dengan Banyak Penyewaan", fontsize=30)
ax[0].set_xlabel("Jam (PM)", fontsize=20)
ax[0].tick_params(axis='x', labelsize=20)
ax[0].tick_params(axis='y', labelsize=25)

# Jam paling sepi
sns.barplot(x="hours", y="count_rent", data=sum_order_items_df.sort_values(by="count_rent", ascending=True).head(5), palette=["#90CAF9"] + ["#D3D3D3"]*4, ax=ax[1])
ax[1].set_title("Jam dengan Sedikit Penyewaan", fontsize=30)
ax[1].set_xlabel("Jam (AM)", fontsize=20)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='x', labelsize=20)
ax[1].tick_params(axis='y', labelsize=25)

st.pyplot(fig)

# ===============================
# Bar chart: musim
# ===============================
st.subheader("Musim dengan Penyewaan Terbanyak")
colors = ["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3"]
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    x="season",
    y="count_rent",
    data=season_df.sort_values(by="season", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Penyewaan Berdasarkan Musim", fontsize=40)
ax.tick_params(axis='x', labelsize=30)
ax.tick_params(axis='y', labelsize=25)
st.pyplot(fig)

# ===============================
# Bar chart: kondisi cuaca
# ===============================
st.subheader("Penyewaan Berdasarkan Kondisi Cuaca")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    x="weather_situation",
    y="count_rent",
    data=weather_df.sort_values(by="count_rent", ascending=False),
    palette="Blues",
    ax=ax
)
ax.set_title("Penyewaan Berdasarkan Cuaca", fontsize=40)
ax.set_xlabel("Kondisi Cuaca", fontsize=25)
ax.set_ylabel("Jumlah Peminjaman", fontsize=25)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

# ===============================
# Pie chart: registered vs casual
# ===============================
st.subheader("Perbandingan Pengguna Registered dan Casual")
labels = 'casual', 'registered'
sizes = [cas_df["casual_sum"].sum(), reg_df["register_sum"].sum()]
explode = (0, 0.1)

fig1, ax1 = plt.subplots()
ax1.pie(
    sizes,
    explode=explode,
    labels=labels,
    autopct='%1.1f%%',
    colors=["#D3D3D3", "#90CAF9"],
    shadow=True,
    startangle=90
)
ax1.axis('equal')
st.pyplot(fig1)
