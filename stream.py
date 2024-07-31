import streamlit as st
import requests
import zipfile
import io
import pandas as pd
import os
import gdown

def download_file_from_google_drive(file_id, dest_path):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, dest_path, quiet=False)

file_id = '1wMeJXGaFF1ku2-txWshzDLaHoxS_tBz0'
dest_path = 'downloaded_file.zip'
download_file_from_google_drive(file_id, dest_path)

with zipfile.ZipFile('downloaded_file.zip.zip', 'r') as zip_ref:
    zip_ref.extractall()

st.write(os.listdir())
