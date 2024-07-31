import streamlit as st
import pandas as pd
import gdown
from io import BytesIO
import zipfile

# URL Google Drive dari file ZIP
file_url = 'https://drive.google.com/file/d/FILE_ID/view?usp=sharing'

# Mendapatkan ID file dari URL
file_id = file_url.split('/d/')[1].split('/view')[0]

# URL untuk mengunduh file
download_url = f'https://drive.google.com/uc?id={file_id}'

# Fungsi untuk mengunduh file ZIP dan membaca file Excel di dalamnya
@st.cache
def load_data_from_zip():
    output = BytesIO()
    gdown.download(download_url, output, quiet=False)
    output.seek(0)
    
    with zipfile.ZipFile(output, 'r') as zip_ref:
        # Menampilkan semua nama file di dalam ZIP
        file_list = zip_ref.namelist()
        st.write("File dalam ZIP:", file_list)
        
        # Membaca file Excel pertama dari ZIP (atau sesuai kebutuhan)
        with zip_ref.open(file_list[0]) as file:
            df = pd.read_excel(file)
    return df

# Memuat data
st.write("Mengunduh dan memuat data dari Google Drive...")
df = load_data_from_zip()

# Menampilkan data di aplikasi Streamlit
st.write("Berikut adalah data yang diunduh dari file Excel dalam ZIP:")
st.dataframe(df)
