import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ===============================
# Set gaya visual dan tema
# ===============================
sns.set(style='dark')
st.set_page_config(layout="wide")

# ===============================
# Fungsi bantu
# ===============================
def format_ribuan(n):
    return f"{n:,}".replace(",", ".")

# ===============================
# Fungsi pemrosesan data
# ===============================
def get_total_count_by_hour_df(hour_df):
    return hour_df.groupby("hours").agg({"count_rent": "sum"}).reset_index()

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

days_df["dteday"] = pd.to_datetime(days_df["dteday"])
hours_df["dteday"] = pd.to_datetime(hours_df["dteday"])

days_df.sort_values("dteday", inplace=True)
hours_df.sort_values("dteday", inplace=True)

# Mapping kategori
season_order = ["Spring", "Summer", "Fall", "Winter"]
season_colors = {
    "Spring": "#AED581", "Summer": "#FFEE58", "Fall": "#FF8A65", "Winter": "#90CAF9"
}
weather_order = ["Clear", "Mist", "Light_Rainsnow", "Heavy_Rainsnow"]
weather_colors = {
    "Clear": "#FFD54F", "Mist": "#B0BEC5", "Light_Rainsnow": "#81D4FA", "Heavy_Rainsnow": "#455A64"
}
day_colors = {"weekday": "#455A64", "weekend": "#1D2122"}

# ===============================
# Sidebar - Filter Tanggal
# ===============================
with st.sidebar:
    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg")
    start_date, end_date = st.date_input("Rentang Tanggal", [days_df["dteday"].min(), days_df["dteday"].max()])

main_df_days = days_df[(days_df["dteday"] >= pd.to_datetime(start_date)) & (days_df["dteday"] <= pd.to_datetime(end_date))]
main_df_hour = hours_df[(hours_df["dteday"] >= pd.to_datetime(start_date)) & (hours_df["dteday"] <= pd.to_datetime(end_date))]

# ===============================
# Header Dashboard
# ===============================
st.title("📊 Bike Sharing Dashboard")
st.markdown("Analisis peminjaman sepeda berdasarkan musim, cuaca, jam, dan perilaku pengguna.")

# ===============================
# Informasi Ringkasan
# ===============================
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Peminjaman", format_ribuan(main_df_days["count_rent"].sum()))
with col2:
    st.metric("Total Registered", format_ribuan(main_df_days["registered"].sum()))
with col3:
    st.metric("Total Casual", format_ribuan(main_df_days["casual"].sum()))

# ===============================
# Bar chart: Musim
# ===============================
st.subheader("🎨 Tren Peminjaman Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    data=main_df_days,
    x="season",
    y="count_rent",
    hue="season",
    palette=season_colors,
    order=season_order,
    legend=False,
    ax=ax
)
ax.set_title("Peminjaman Sepeda per Musim", fontsize=35, fontweight='bold')
ax.set_xlabel("Musim", fontsize=20)
ax.set_ylabel("Jumlah Peminjaman", fontsize=20)
plt.tight_layout()
st.pyplot(fig)

# ===============================
# Bar chart: Cuaca
# ===============================
st.subheader("☁️ Tren Peminjaman Berdasarkan Cuaca")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    data=main_df_days,
    x="weather_situation",
    y="count_rent",
    hue="weather_situation",
    palette=weather_colors,
    order=weather_order,
    legend=False,
    ax=ax
)
ax.set_title("Peminjaman Sepeda per Kondisi Cuaca", fontsize=35, fontweight='bold')
ax.set_xlabel("Cuaca (Clear, Mist, Light Rain/Snow, Heavy Rain/Snow)", fontsize=20)
ax.set_ylabel("Jumlah Peminjaman", fontsize=20)
plt.tight_layout()
st.pyplot(fig)

# ===============================
# Pointplot: Jam per Hari
# ===============================
st.subheader("⏰ Peminjaman per Jam (Weekday vs Weekend)")
fig, ax = plt.subplots(figsize=(20, 10))
sns.pointplot(data=main_df_hour, x="hours", y="count_rent", hue="category_days", palette="Set1", ax=ax)
ax.set_title("Peminjaman Sepeda Berdasarkan Kategori Hari", fontsize=35)
ax.set_xlabel("Jam", fontsize=20)
ax.set_ylabel("Jumlah Peminjaman", fontsize=20)
ax.set_xticks(range(0, 24))
ax.set_xticklabels([f"{i}:00" for i in range(24)], rotation=45)
plt.tight_layout()
st.pyplot(fig)

# ===============================
# Bar chart: Weekday vs Weekend
# ===============================
st.subheader("📅 Peminjaman Berdasarkan Jenis Hari")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(data=main_df_days, x="category_days", y="count_rent", palette=day_colors, ax=ax)
ax.set_title("Jumlah Peminjaman Weekday vs Weekend", fontsize=35)
ax.set_xlabel("Jenis Hari", fontsize=20)
ax.set_ylabel("Jumlah Peminjaman", fontsize=20)
plt.tight_layout()
st.pyplot(fig)

# ===============================
# Pie Chart: Registered vs Casual
# ===============================
st.subheader("👥 Perbandingan Registered dan Casual")
fig, ax = plt.subplots()
data = [main_df_days["casual"].sum(), main_df_days["registered"].sum()]
labels = ["Casual", "Registered"]
ax.pie(data, labels=labels, autopct='%1.1f%%', colors=["#D3D3D3", "#72BCD4"], startangle=90)
ax.set_title("Distribusi Pengguna: Casual vs Registered", fontsize=20)
ax.axis("equal")
st.pyplot(fig)

# ===============================
# Korelasi Humidity dan Peminjaman
# ===============================
st.subheader("💧 Pengaruh Kelembapan terhadap Peminjaman")
fig, ax = plt.subplots(figsize=(18, 10))
sns.regplot(data=main_df_days, x="humidity", y="count_rent", scatter_kws={"color": "#42A5F5"}, line_kws={"color": "red"}, ax=ax)
ax.set_title("Korelasi Humidity dan Jumlah Peminjaman", fontsize=25)
plt.tight_layout()
st.pyplot(fig)

# ===============================
# Tren Peminjaman per Hari
# ===============================
st.subheader("📈 Tren Peminjaman Sepanjang Waktu")
fig, ax = plt.subplots(figsize=(24, 6))
ax.plot(main_df_days["dteday"], main_df_days["count_rent"], color="#90CAF9", linewidth=2)
ax.scatter(main_df_days["dteday"], main_df_days["count_rent"], s=10, color="#90CAF9")
ax.set_xlabel("Tanggal", fontsize=15)
ax.set_ylabel("Jumlah Peminjaman", fontsize=15)
ax.set_title("Tren Peminjaman Sepeda Harian", fontsize=25)
plt.tight_layout()
st.pyplot(fig)

# ===============================
# Segmentasi RFM
# ===============================
st.subheader("📊 Segmentasi Pengguna Berdasarkan RFM")

main_df_hour["dteday"] = pd.to_datetime(main_df_hour["dteday"])
current_date = main_df_hour['dteday'].max()

rfm_df = main_df_hour.groupby('registered').agg({
    'dteday': lambda x: (current_date - x.max()).days,
    'instant': 'count',
    'count_rent': 'sum'
}).reset_index()

rfm_df.columns = ['registered', 'Recency', 'Frequency', 'Monetary']
rfm_df['R_Score'] = pd.qcut(rfm_df['Recency'], 3, labels=[3, 2, 1]).astype(int)
rfm_df['F_Score'] = pd.qcut(rfm_df['Frequency'].rank(method='first'), 3, labels=[1, 2, 3]).astype(int)
rfm_df['M_Score'] = pd.qcut(rfm_df['Monetary'].rank(method='first'), 3, labels=[1, 2, 3]).astype(int)
rfm_df['RFM_Score'] = rfm_df['R_Score'].astype(str) + rfm_df['F_Score'].astype(str) + rfm_df['M_Score'].astype(str)

def segment(row):
    if row['RFM_Score'] == '333':
        return 'Top Customer'
    elif row['R_Score'] == 3:
        return 'Loyal'
    elif row['R_Score'] == 1 and row['F_Score'] <= 2:
        return 'At Risk'
    else:
        return 'Others'

rfm_df['Segment'] = rfm_df.apply(segment, axis=1)

if rfm_df.empty:
    st.warning("Tidak ada data untuk segmentasi RFM pada rentang tanggal ini.")
else:
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.scatterplot(data=rfm_df, x='Recency', y='Frequency', size='Monetary',
                    hue='Segment', palette='Set2', sizes=(40, 300), alpha=0.8, ax=ax)
    ax.set_title('Visualisasi Segmentasi RFM Pengguna')
    ax.set_xlabel('Recency (Hari sejak terakhir menyewa)')
    ax.set_ylabel('Frequency (Jumlah penyewaan)')
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)
