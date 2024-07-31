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

with zipfile.ZipFile('downloaded_file.zip', 'r') as zip_ref:
    zip_ref.extractall()

df_merge = pd.read_csv('Compile Merge (ALL).csv')
df_breakdown = pd.read_csv('Compile Breakdown (ALL).csv')

df_merge['DATE'] = pd.to_datetime(df_merge['DATE'],format='%Y-%m-%d')
df_breakdown['DATE'] = pd.to_datetime(df_breakdown['DATE'],format='%Y-%m-%d')

df_merge['KAT'] = df_merge['KAT'].str.upper()
df_merge2 = df_merge.groupby(['SOURCE','KAT'])[['NOM']].sum().reset_index()

df_merge3 = df_merge2[df_merge2['KAT'].isin(['QRIS ESB','QRIS TELKOM'])].groupby('SOURCE')[['NOM']].sum().reset_index()
df_merge3['KAT']='QRIS TELKOM/ESB'

st.dataframe(pd.pivot(data=pd.concat([df_merge2[df_merge2['KAT'].isin(['GO RESTO','GRAB FOOD','QRIS SHOPEE','SHOPEEPAY'])],df_merge3]), 
         index='SOURCE', columns='KAT', values='NOM').reset_index())
