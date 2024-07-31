import requests
import zipfile
import io
import pandas as pd
import streamlit as st

# URL file ZIP di Google Drive atau sumber lain
url = 'https://drive.google.com/uc?export=download&id=1wMeJXGaFF1ku2-txWshzDLaHoxS_tBz0'

# Mengunduh file ZIP
response = requests.get(url)
response.raise_for_status()  # Memastikan permintaan berhasil

# Mengecek jenis konten
content_type = response.headers.get('Content-Type')
st.write(f"Content-Type: {content_type}")

if 'application/zip' not in content_type:
    st.write("The downloaded file is not a ZIP file or is not correctly downloaded.")
else:
    try:
        # Membaca file ZIP dari respons
        with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
            st.write("Files in the ZIP:")
            thezip.st.writedir()
            
            # Membaca setiap file dalam ZIP
            for file_name in thezip.namelist():
                # Mengecek jika file adalah CSV
                if file_name.endswith('.csv'):
                    with thezip.open(file_name) as file:
                        # Membaca file CSV ke dalam DataFrame pandas
                        df = pd.read_csv(file)
                        st.write(f"\nData from {file_name}:")
                        st.write(df.head())  # Menampilkan beberapa baris pertama data
                else:
                    st.write(f"Skipping non-CSV file: {file_name}")

    except zipfile.BadZipFile:
        st.write("Failed to unzip the file. The file may be corrupted or not a ZIP file.")
