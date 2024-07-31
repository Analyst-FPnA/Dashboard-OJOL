import streamlit as st
import pandas as pd
import gdown
from io import BytesIO
import zipfile

# ID file dari Google Drive
file_id = '1wMeJXGaFF1ku2-txWshzDLaHoxS_tBz0'
download_url = f'https://drive.google.com/uc?id={file_id}'

# Lokasi penyimpanan file
output = '/path/to/save/file.zip'

try:
    gdown.download(download_url, output, quiet=False)
    print("File successfully downloaded.")
except Exception as e:
    print(f"An error occurred: {e}")
