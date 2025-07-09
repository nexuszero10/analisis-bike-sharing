# Submission Dicoding "Belajar Analisis Data dengan Python"

## Project Analisis Data

Repository ini berisi proyek data analytics yang saya kerjakan. Deployment in **Streamlit** <img src="https://user-images.githubusercontent.com/7164864/217935870-c0bc60a3-6fc0-4047-b011-7b4c59488c91.png" alt="Streamlit logo"></img>

## Deskripsi

Proyek ini bertujuan untuk menganalisis data pada Bike Sharing Dataset dari Washington DC. Tujuan akhirnya adalah untuk menghasilkan wawasan dan informasi yang berguna dari data yang dianalisis unutk membuat wisdon berupa kaputusan bisnis nantinya.

## Struktur Direktori

- **/data**: folder berisi dataset raw yang digunakan dalam format csv (coma separated value) .
- **/dashboard**: folder berisi dashboard.py unutk streamlit dan data yang sudah cleaning dalam format csv.
- **notebook.ipynb**: File ini yang digunakan untuk melakukan analisis data mulai data data wrangling, Exploratory Data Analysis (EDA), dan visualisasi & Explanatory serta analisis RFM.

## Instalasi

1. Clone repository ini ke komputer lokal Anda menggunakan perintah berikut:

   ```shell
   git clone https://github.com/nexuszero10/analisis-bike-sharing
   ```

2. Pastikan Anda memiliki Python environment yang sesuai dan pustaka-pustaka yang diperlukan. Anda dapat menginstal library tersebut dengan menjalankan perintah berikut:

    ```shell
    pip install streamlit
    pip install -r requirements.txt
    ```

## Penggunaan
1. Masuk ke direktori proyek (Local):

    ```shell
    cd bike-sharing-analisis/dashboard/
    streamlit run dashboard.py
    ```
    Atau bisa dengan kunjungi website ini [Project Data Analytics]