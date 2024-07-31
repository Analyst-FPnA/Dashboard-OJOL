import requests
import zipfile
import io
import pandas as pd
import streamlit as st
import tempfile 
import os

url = 'https://drive.google.com/uc?export=download&id=1wMeJXGaFF1ku2-txWshzDLaHoxS_tBz0'
response = requests.get(url)
response.raise_for_status()

# Menyimpan file untuk pemeriksaan manual
with open(f'downloaded_file.zip', 'wb') as file:
    file.write(response.content)
st.write(os.listdir())

# Memeriksa konten file yang diunduh
with tempfile.TemporaryDirectory() as tmpdirname:

    with zipfile.ZipFile(f'{tmpdirname}/downloaded_file.zip', 'r') as zip_ref:
        zip_ref.extractall(tmpdirname)
    st.write(pd.read_csv(f'{tmpdirname}/Compile Breakdown (ALL).csv').head())
