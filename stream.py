import requests
import zipfile
import io
import pandas as pd
import streamlit as st

def download_and_extract_zip(url):
    try:
        # Unduh file dari URL
        response = requests.get(url)
        response.raise_for_status()  # Memastikan permintaan berhasil
        
        # Mencoba membaca file ZIP dari respons tanpa memeriksa Content-Type
        try:
            with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
                st.write("Daftar file dalam ZIP:")
                thezip.st.writedir()
                
                # Membaca setiap file dalam ZIP
                for file_name in thezip.namelist():
                    if file_name.endswith('.csv'):
                        with thezip.open(file_name) as file:
                            # Membaca file CSV ke dalam DataFrame pandas
                            df = pd.read_csv(file)
                            st.write(f"\nData dari {file_name}:")
                            st.write(df.head())  # Menampilkan beberapa baris pertama data
                    else:
                        st.write(f"Melewati file non-CSV: {file_name}")
        except zipfile.BadZipFile:
            st.write("Gagal mengekstrak file ZIP. File mungkin rusak atau bukan file ZIP.")
        
    except requests.RequestException as e:
        st.write(f"Permintaan gagal: {e}")
    except Exception as e:
        st.write(f"Terjadi kesalahan yang tidak terduga: {e}")

# URL file ZIP di Google Drive atau sumber lain
url = 'https://drive.google.com/uc?export=download&id=1wMeJXGaFF1ku2-txWshzDLaHoxS_tBz0'  # Ganti dengan ID file yang sesuai

# Memanggil fungsi
download_and_extract_zip(url)
