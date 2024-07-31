import requests
import zipfile
import io

# URL file ZIP di Google Drive atau sumber lain
url = 'https://drive.google.com/uc?export=download&id=1wMeJXGaFF1ku2-txWshzDLaHoxS_tBz0'

# Mengunduh file ZIP
response = requests.get(url)
response.raise_for_status()  # Memastikan permintaan berhasil

# Mengecek jenis konten file yang diunduh
content_type = response.headers.get('Content-Type')
st.write(f"Content-Type: {content_type}")

# Cek apakah file memiliki ekstensi ZIP
if 'application/zip' not in content_type:
    st.write("The downloaded file is not a ZIP file.")
else:
    try:
        # Membaca file ZIP dari respons
        with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
            # Menampilkan semua nama file dalam ZIP
            st.write("Files in the ZIP:")
            thezip.st.writedir()
            
            # Membaca setiap file dalam ZIP
            for file_name in thezip.namelist():
                # Mengekstrak dan membaca file Excel (atau file lain)
                with thezip.open(file_name) as file:
                    # Jika file Excel
                    if file_name.endswith('.csv'):
                        import pandas as pd
                        df = pd.read_csv(file)
                        st.write(f"\nData from {file_name}:")
                        st.write(df.head())  # Menampilkan beberapa baris pertama data
    except zipfile.BadZipFile:
        st.write("Failed to unzip the file. The file may be corrupted or not a ZIP file.")
