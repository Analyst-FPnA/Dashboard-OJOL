import streamlit as st
import requests
import zipfile
import io
import pandas as pd

# Fungsi untuk mendownload file ZIP dari Google Drive
def download_zip_from_google_drive():
    url = f"https://drive.google.com/uc?export=download&id=1wMeJXGaFF1ku2-txWshzDLaHoxS_tBz0"
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        st.error("Gagal mendownload file ZIP.")
        return None

# Fungsi untuk membaca file CSV dari ZIP
def read_csv_from_zip(zip_content):
    with zipfile.ZipFile(io.BytesIO(zip_content)) as z:
        # Daftar nama file dalam ZIP
        file_names = z.namelist()
        # Misalkan kita hanya ingin membaca file CSV pertama
        if file_names:
            with z.open(file_names[0]) as f:
                df = pd.read_csv(f).head()
                return df
        else:
            st.error("Tidak ada file di dalam ZIP.")
            return None

# Aplikasi Streamlit
st.title("Download dan Baca CSV dari ZIP di Google Drive")

# Input ID file Google Drive
if file_id:
    zip_content = download_zip_from_google_drive()
    if zip_content:
        df = read_csv_from_zip(zip_content)
        if df is not None:
            st.write("Data dari CSV:")
            st.dataframe(df)
