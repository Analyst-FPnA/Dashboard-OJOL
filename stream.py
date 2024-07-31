import streamlit as st
import requests
import zipfile
import io
import pandas as pd
import os

# Fungsi untuk mendownload file ZIP dari Google Drive
url = 'https://drive.google.com/uc?export=download&id=1f-YfvMvFG0UaOw9H5RqNpkPRJEB-8gfa'
response = requests.get(url)
response.raise_for_status()

# Menyimpan file untuk pemeriksaan manual
with open('downloaded_file.zip', 'wb') as file:
    file.write(response.content)       
st.write(os.listdir())

def read_csv_from_zip():
    try:
        with zipfile.ZipFile('downloaded_file.zip') as z:
            file_names = z.namelist()
            if file_names:
                # Memilih file CSV pertama yang ditemukan
                csv_file = [name for name in file_names if name.endswith('.csv')]
                if csv_file:
                    with z.open(csv_file[0]) as f:
                        df = pd.read_csv(f).head()
                        return df
                else:
                    st.error("Tidak ada file CSV dalam ZIP.")
                    return None
            else:
                st.error("ZIP tidak berisi file.")
                return None
    except zipfile.BadZipFile:
        st.error("File yang diunduh bukan file ZIP yang valid.")
        return None
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        return None
read_csv_from_zip()
