import requests
import zipfile
import io
import pandas as pd
import streamlit as st

def download_and_extract_zip(url):
    try:
        # Mengunduh file ZIP
        response = requests.get(url)
        response.raise_for_status()  # Memastikan permintaan berhasil
        
        # Cek apakah respons adalah file ZIP
        content_type = response.headers.get('Content-Type', '')
        if 'application/zip' not in content_type:
            st.write("The downloaded file is not a ZIP file or is not correctly downloaded.")
            return

        # Membaca file ZIP dari respons
        with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
            st.write("Files in the ZIP:")
            thezip.st.writedir()
            
            # Membaca setiap file dalam ZIP
            for file_name in thezip.namelist():
                if file_name.endswith('.csv'):
                    with thezip.open(file_name) as file:
                        # Membaca file CSV ke dalam DataFrame pandas
                        df = pd.read_csv(file)
                        st.write(f"\nData from {file_name}:")
                        st.write(df.head())  # Menampilkan beberapa baris pertama data
                else:
                    st.write(f"Skipping non-CSV file: {file_name}")
    except requests.RequestException as e:
        st.write(f"Request failed: {e}")
    except zipfile.BadZipFile:
        st.write("Failed to unzip the file. The file may be corrupted or not a ZIP file.")
    except Exception as e:
        st.write(f"An unexpected error occurred: {e}")

# URL file ZIP di Google Drive atau sumber lain
url = 'https://drive.google.com/uc?export=download&id=1wMeJXGaFF1ku2-txWshzDLaHoxS_tBz0'

# Memanggil fungsi
download_and_extract_zip(url)
