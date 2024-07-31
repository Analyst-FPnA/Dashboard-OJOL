import streamlit as st
import requests
import zipfile
import io
import pandas as pd
import os

from google_drive_downloader import GoogleDriveDownloader as gdd

gdd.download_file_from_google_drive(file_id='1f-YfvMvFG0UaOw9H5RqNpkPRJEB-8gfa',
                                    dest_path='doqwnload.zip',
                                    unzip=True)
with zipfile.ZipFile('doqwnload.zip', 'r') as zip_ref:
    zip_ref.extractall()

st.write(os.listdir())
