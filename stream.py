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


def read_csv_from_zip(zip_content):
    try:
        with zipfile.ZipFile(io.BytesIO(zip_content)) as z:
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


# Aplikasi Streamlit
st.title("Download dan Baca CSV dari ZIP di Google Drive")

# Input ID file Google Drive
zip_content = download_zip_from_google_drive()
if zip_content:
        df = read_csv_from_zip(zip_content)
        if df is not None:
            st.write("Data dari CSV:")
            st.dataframe(df)
