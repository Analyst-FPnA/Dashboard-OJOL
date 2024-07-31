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

with zipfile.ZipFile('downloaded_file.zip', 'r') as zip_ref:
    zip_ref.extractall()

st.write(os.listdir())
