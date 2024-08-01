import streamlit as st
import requests
import zipfile
import io
import pandas as pd
import os
import gdown
import tempfile

def download_file_from_github(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully and saved to {save_path}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

def load_excel(file_path):
    with open(file_path, 'rb') as file:
        model = pd.read_excel(file, engine='openpyxl')
    return model

def list_files_in_directory(dir_path):
    # Fungsi untuk mencetak semua isi dari suatu direktori
    for root, dirs, files in os.walk(dir_path):
        st.write(f'Direktori: {root}')
        for file_name in files:
            st.write(f'  - {file_name}')

# URL file model .pkl di GitHub (gunakan URL raw dari file .pkl di GitHub)
url = 'https://raw.githubusercontent.com/ferifirmansah05/ads_mvn/main/database provinsi.xlsx'

# Path untuk menyimpan file yang diunduh
save_path = 'database provinsi.xlsx'

# Unduh file dari GitHub
download_file_from_github(url, save_path)

# Muat model dari file yang diunduh
if os.path.exists(save_path):
    df_prov = load_excel(save_path)
    print("Model loaded successfully")
else:
    print("Model file does not exist")

df_prov = df_prov[3:].dropna(subset=['Unnamed: 4']) 
df_prov.columns = df_prov.loc[3,:].values
df_prov = df_prov.loc[4:,]
df_prov = df_prov.loc[:265, ['Nama','Provinsi Alamat','Kota Alamat']]
df_prov = df_prov.rename(columns={'Nama':'Nama Cabang','Provinsi Alamat':'Provinsi', 'Kota Alamat': 'Kota/Kabupaten'})
list_cab = df_prov['Nama Cabang'].str.extract(r'\((.*?)\)')[0].values


st.title('Dashboard - Ojol')

all_cab = st.multiselect('Pilih Cabang', list_cab)
all_cab = list(all_cab)

if st.button('Show'):
    with tempfile.TemporaryDirectory() as tmpdirname:
        def download_file_from_google_drive(file_id, dest_path):
            if not os.path.exists(dest_path):
                url = f"https://drive.google.com/uc?id={file_id}"
                gdown.download(url, dest_path, quiet=False)
                with zipfile.ZipFile(f'{tmpdirname}/downloaded_file.zip', 'r') as zip_ref:
                    zip_ref.extractall(tmpdirname)
                    
        file_id = '1wMeJXGaFF1ku2-txWshzDLaHoxS_tBz0'
        dest_path = f'{tmpdirname}/downloaded_file.zip'
        download_file_from_google_drive(file_id, dest_path)
        
        df_merge = pd.read_csv(f'{tmpdirname}/Compile Merge (ALL).csv')
        df_breakdown = pd.read_csv(f'{tmpdirname}/Compile Breakdown (ALL).csv')
        #st.write(df_merge.loc[0,'DATE'])
        #st.write(start_date)
        
        df_merge = df_merge[df_merge['CAB']==all_cab[0]]
        df_breakdown = df_breakdown[df_breakdown['CAB']==all_cab[0]]
        
        df_merge['DATE'] = pd.to_datetime(df_merge['DATE'],format='%Y-%m-%d')
        df_breakdown['DATE'] = pd.to_datetime(df_breakdown['DATE'],format='%Y-%m-%d')
        
        df_merge['KAT'] = df_merge['KAT'].str.upper()
        df_merge2 = df_merge.groupby(['SOURCE','KAT'])[['NOM']].sum().reset_index()
        
        df_merge3 = df_merge2[df_merge2['KAT'].isin(['QRIS ESB','QRIS TELKOM'])].groupby('SOURCE')[['NOM']].sum().reset_index()
        df_merge3['KAT']='QRIS TELKOM/ESB'
        
        if df_merge3.empty:
            df_merge3.loc[len(df_merge3)] = ['INVOICE',0,'QRIS TELKOM/ESB']
            df_merge3.loc[len(df_merge3)] = ['WEB',0,'QRIS TELKOM/ESB']
        st.write(dF_merge3)
        st.write(pd.concat([df_merge2[df_merge2['KAT'].isin(['GO RESTO','GRAB FOOD','QRIS SHOPEE','SHOPEEPAY'])],df_merge3]))
        df_merge = pd.pivot(data=pd.concat([df_merge2[df_merge2['KAT'].isin(['GO RESTO','GRAB FOOD','QRIS SHOPEE','SHOPEEPAY'])],df_merge3]), 
                 index='SOURCE', columns='KAT', values='NOM')
        
        st.dataframe(df_merge)

        kat_pengurang = ['Invoice Beda Hari',
                         'Transaksi Kemarin',
                         'Selisih IT',
                         'Promo Marketing/Adjustment',
                         'Cancel Nota',
                         'Tidak Ada Transaksi di Web',
                         'Selisih Lebih Bayar QRIS',
                         'Selisih Lebih Bayar Ojol',
                         'Salah Slot Pembayaran']
        kat_diperiksa = ['Tidak Ada Invoice QRIS',
                         'Tidak Ada Invoice Ojol',
                         'Double Input',
                         'Selisih Kurang Bayar QRIS',
                         'Selisih Kurang Bayar Ojol',
                         'Bayar Lebih dari 1 Kali - 1 Struk (QRIS)',
                         'Bayar 1 Kali - Banyak Struk (QRIS)',
                         'Bayar Lebih dari 1 Kali - Banyak Struk (QRIS)',
                         'Kurang Input (Ojol)']
        df_breakdown['Kategori'] = df_breakdown['Kategori'].str.upper()
        df_breakdown.columns = df_breakdown.columns[:-7].to_list() + ['GO RESTO','GRAB FOOD','QRIS SHOPEE','QRIS TELKOM/ESB','SHOPEEPAY'] + df_breakdown.columns[-2:].to_list()

        df_breakdown_pengurang = df_breakdown[df_breakdown['Kategori'].isin([x.upper() for x in kat_pengurang])].groupby('Kategori')[df_breakdown.columns[-7:-2]].sum()
        st.dataframe(df_breakdown_pengurang)
        df_breakdown_diperiksa = df_breakdown[df_breakdown['Kategori'].isin([x.upper() for x in kat_diperiksa])].groupby('Kategori')[df_breakdown.columns[-7:-2]].sum()
        st.dataframe(df_breakdown_diperiksa)
