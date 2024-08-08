import streamlit as st
import requests
import zipfile
import io
import pandas as pd
import os
import gdown
import tempfile

st.set_page_config(layout="wide")

def add_min_width_css():
    st.markdown(
        """
        <style>
        /* Set a minimum width for the app */
        .css-1d391kg {
            min-width: 3000px; /* Set the minimum width */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Add CSS styling to the app
add_min_width_css()

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
url = 'https://raw.githubusercontent.com/Analyst-FPnA/Dashboard-OJOL/main/list_cab.xlsx'

# Path untuk menyimpan file yang diunduh
save_path = 'list_cab.xlsx'

# Unduh file dari GitHub
download_file_from_github(url, save_path)

# Muat model dari file yang diunduh
if os.path.exists(save_path):
    list_cab = load_excel(save_path)
    print("File loaded successfully")
else:
    print("File does not exist")


st.title('Dashboard - Selisih Ojol')

if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

# Fungsi untuk mereset state button
def reset_button_state():
    st.session_state.button_clicked = False
    
col = st.columns(2)

with col[0]:
    all_cab = st.multiselect('Pilih Cabang', list_cab['CAB'].sort_values().unique(), on_change=reset_button_state)
    all_cab = list(all_cab)

with col[1]:
    list_bulan = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    all_bulan = st.multiselect('Pilih Bulan', list_bulan, on_change=reset_button_state)
    
def download_file_from_google_drive(file_id, dest_path):
    if not os.path.exists(dest_path):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, dest_path, quiet=False)
        with zipfile.ZipFile(f'downloaded_file.zip', 'r') as zip_ref:
            zip_ref.extractall()
            
        directory = f'Merge'    
        dfs = []
        # Iterate over each file in the directory
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                filepath = os.path.join(directory, filename)
                try:
                    # Read each CSV file into a DataFrame and append to the list
                    df = pd.read_csv(filepath)
                    df.columns = [x.strip() for x in df.columns]
                    dfs.append(df)
                    #empty_df = pd.DataFrame()
                    #empty_df.to_csv(file_path, index=False)
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
        if dfs:
            # Concatenate all DataFrames in the list along axis 0 (rows)
            df_merge = pd.concat(dfs, ignore_index=True)
         
        directory = f'Breakdown'
        dfs = []
        # Iterate over each file in the directory
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                filepath = os.path.join(directory, filename)
                try:
                    # Read each CSV file into a DataFrame and append to the list
                    dfs.append(pd.read_csv(filepath))
                    #empty_df = pd.DataFrame()
                    #empty_df.to_csv(file_path, index=False)
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
        if dfs:
            # Concatenate all DataFrames in the list along axis 0 (rows)
            df_breakdown = pd.concat(dfs, ignore_index=True)
        
        #df_merge = df_merge[df_merge['CAB'].isin(all_cab)]
        #df_breakdown = df_breakdown[df_breakdown['CAB'].isin(all_cab)]
        
        df_merge['NOM'] = df_merge['NOM'].fillna(0)
        df_merge['NOM'] = df_merge['NOM'].apply(lambda x: str(x).strip())
        df_merge = df_merge[(df_merge['NOM']!='Cek')]
        df_merge['NOM'] = df_merge['NOM'].apply(lambda x :x.strip().replace('Rp','').replace(',','') if 'Rp' in str(x) else x)
        df_merge['NOM'] = df_merge['NOM'].apply(lambda x: -int(x.replace('(', '').replace(')', '')) if '(' in str(x) and ')' in str(x) else x)
        df_merge['NOM'] = df_merge['NOM'].apply(lambda x :x.strip().replace(',','') if ',' in str(x) else x)
        df_merge = df_merge[(df_merge['NOM']!='-')]
        df_merge['NOM'] = df_merge['NOM'].astype(float)
        
        df_merge['DATE'] = pd.to_datetime(df_merge['DATE'],format='%d/%m/%Y')
        df_breakdown['DATE'] = pd.to_datetime(df_breakdown['DATE'],format='%d/%m/%Y')

        df_merge['MONTH'] = df_merge['DATE'].dt.month_name()
        df_breakdown['MONTH'] = df_breakdown['DATE'].dt.month_name()
        df_merge = df_merge[df_merge['MONTH'].isin(all_bulan)]
        df_breakdown = df_breakdown[df_breakdown['MONTH'].isin(all_bulan)]
        df_merge['KAT'] = df_merge['KAT'].str.upper()

        df_breakdown['Kategori'] = df_breakdown['Kategori'].str.upper()

        df_breakdown.columns = df_breakdown.columns[:-7].to_list() + ['GO RESTO','GRAB FOOD','QRIS SHOPEE','QRIS TELKOM/ESB','SHOPEEPAY'] + df_breakdown.columns[-2:].to_list()
        df_breakdown.iloc[:,9:14] = df_breakdown.iloc[:,9:14].applymap(lambda x: str(x).replace(',', '')).astype('float')

        df_selisih = df_breakdown[df_breakdown['Kategori'].isin(['DOUBLE INPUT','TIDAK ADA INVOICE OJOL','TIDAK ADA INVOICE QRIS'])].groupby(['MONTH','CAB'])[df_breakdown.columns[9:14]].sum().reset_index()
        df_selisih['SELISIH'] = df_selisih.iloc[:,2:].sum(axis=1)
        df_selisih = df_selisih.groupby('MONTH')[['SELISIH']].mean().reset_index()
        
        df_cancelnota = df_breakdown[df_breakdown['Kategori'].isin(['CANCEL NOTA'])].groupby(['MONTH','CAB'])[df_breakdown.columns[9:14]].sum().reset_index()
        df_cancelnota['CANCEL NOTA'] = df_cancelnota.iloc[:,2:].sum(axis=1)
        df_cancelnota = df_cancelnota.groupby('MONTH')[['CANCEL NOTA']].mean().reset_index()
        
        df_line = df_selisih.merge(df_cancelnota)
        df_line.iloc[:,1:] = abs(df_line.iloc[:,1:])
        df_line['MONTH'] = pd.Categorical(df_line['MONTH'], categories=['January','February','March','April','May','June','July'], ordered=True)
        df_line = df_line.sort_values('MONTH')
        
        df_merge.to_csv('merge.csv',index=False)
        df_breakdown.to_csv('breakdown.csv',index=False)
        df_line.to_csv('grafik.csv',index=False)
        df_merge = None
        df_breakdown = None
        df_line = None
        
file_id = '1BP3-98cKLKgY3flpsyuhjbE7zXWNSN3V'
dest_path = f'downloaded_file.zip'
download_file_from_google_drive(file_id, dest_path)

st.write(os.listdir())
df_line = pd.read_csv('grafik.csv')
df_line.set_index('MONTH', inplace=True)

# Display line chart
st.line_chart(df_line)

# Tombol untuk mengeksekusi aksi
if st.button('Process'):
    st.session_state.button_clicked = True

# Eksekusi kode jika tombol diklik
if st.session_state.button_clicked:
        df_merge = pd.read_csv('merge.csv')
        df_breakdown = pd.read_csv('breakdown.csv')
    
        st.cache_data.clear()
        st.cache_resource.clear()        
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
        for cab in all_cab:
            df_merge2 = df_merge[(df_merge['CAB'] == cab)]
            df_merge2 = df_merge2.groupby(['MONTH','SOURCE','KAT'])[['NOM']].sum().reset_index()
            for bulan in all_bulan:
                for i in ['GO RESTO','GRAB FOOD','QRIS SHOPEE','SHOPEEPAY']:
                    if i not in df_merge2[df_merge2['MONTH']==bulan]['KAT'].values:
                        df_merge2.loc[len(df_merge2)] = [bulan,'INVOICE',i,0]
                        df_merge2.loc[len(df_merge2)] = [bulan,'WEB',i,0]
            df_merge3 = df_merge2[df_merge2['KAT'].isin(['QRIS ESB','QRIS TELKOM'])].groupby(['MONTH','SOURCE'])[['NOM']].sum().reset_index()
            df_merge3['KAT']='QRIS TELKOM/ESB'
            
            for bulan in all_bulan:
                if df_merge3[df_merge3['MONTH']==bulan].empty:
                    df_merge3.loc[len(df_merge3)] = [bulan,'INVOICE',0,'QRIS TELKOM/ESB']
                    df_merge3.loc[len(df_merge3)] = [bulan, 'WEB',0,'QRIS TELKOM/ESB']
            df_merge_final = pd.concat([df_merge2[df_merge2['KAT'].isin(['GO RESTO','GRAB FOOD','QRIS SHOPEE','SHOPEEPAY'])],df_merge3]).sort_values('MONTH')
            def highlight_last_row(x):
                font_color = 'color: white;'
                background_color = 'background-color: #FF4B4B;'  # Warna yang ingin digunakan
                df_styles = pd.DataFrame('', index=x.index, columns=x.columns)
                
                # Memberikan warna khusus pada baris terakhir yang bernama 'SELISIH'
                df_styles.iloc[-1, :] = font_color + background_color
            
                return df_styles
                
            def format_number(x):
                if isinstance(x, (int, float)):
                    return "{:,.0f}".format(x)
                return x
                
            st.markdown(f'## {cab}')
            st.markdown('#### SELISIH PER-PAYMENT')
            
            col = st.columns(len(all_bulan))
            for i, bulan in enumerate(all_bulan):
                with col[i]:
                    st.write(f'{bulan}')
                    df_merge_bln = pd.pivot(data=df_merge_final[df_merge_final['MONTH']==bulan], 
                                index='SOURCE', columns=['KAT'], values='NOM').reset_index().fillna(0)
                    df_merge_bln.loc[len(df_merge_bln)] =['SELISIH']+list(df_merge_bln.iloc[0,].values[1:] - df_merge_bln.iloc[1,].values[1:])
                    # Terapkan format pada seluruh DataFrame
                    df_merge_bln = df_merge_bln.applymap(format_number)
                    # Menerapkan styling pada DataFrame
                    df_merge_bln = df_merge_bln.style.apply(highlight_last_row, axis=None)

                    # Menampilkan DataFrame di Streamlit
                    st.dataframe(df_merge_bln, use_container_width=True, hide_index=True)
           
                    
            st.markdown('#### KATEGORI PENGURANG')
            df_breakdown2 = df_breakdown[df_breakdown['CAB'] == cab]
            df_breakdown_pengurang = df_breakdown2[df_breakdown2['Kategori'].isin([x.upper() for x in kat_pengurang])].groupby(['MONTH','Kategori'])[df_breakdown.columns[-7:-2]].sum().reset_index()
            col = st.columns(len(all_bulan))
            for i, bulan in enumerate(all_bulan):
                with col[i]:
                    st.write(f'{bulan}')
                    df_breakdown_pengurang_bln = df_breakdown_pengurang[df_breakdown_pengurang['MONTH']==bulan].iloc[:,1:]
                    df_breakdown_pengurang_bln.loc[len(df_breakdown_pengurang_bln)] = ['TOTAL',
                                                                              df_breakdown_pengurang_bln.iloc[:,1].sum(),
                                                                              df_breakdown_pengurang_bln.iloc[:,2].sum(),
                                                                              df_breakdown_pengurang_bln.iloc[:,3].sum(),
                                                                              df_breakdown_pengurang_bln.iloc[:,4].sum(),
                                                                              df_breakdown_pengurang_bln.iloc[:,5].sum()]
                    df_breakdown_pengurang_bln = df_breakdown_pengurang_bln.applymap(format_number)
                    df_breakdown_pengurang_bln = df_breakdown_pengurang_bln.style.apply(highlight_last_row, axis=None)
                    st.dataframe(df_breakdown_pengurang_bln, use_container_width=True, hide_index=True)
    
            st.markdown('#### KATEGORI DIPERIKSA')
            df_breakdown_diperiksa = df_breakdown2[df_breakdown2['Kategori'].isin([x.upper() for x in kat_diperiksa])].groupby(['MONTH','Kategori'])[df_breakdown.columns[-7:-2]].sum().reset_index()
            col = st.columns(len(all_bulan))
            for i, bulan in enumerate(all_bulan):
                with col[i]:
                    st.write(f'{bulan}')
                    df_breakdown_diperiksa_bln = df_breakdown_diperiksa[df_breakdown_diperiksa['MONTH']==bulan].iloc[:,1:]
                    df_breakdown_diperiksa_bln.loc[len(df_breakdown_diperiksa_bln)] = ['TOTAL',
                                                                              df_breakdown_diperiksa_bln.iloc[:,1].sum(),
                                                                              df_breakdown_diperiksa_bln.iloc[:,2].sum(),
                                                                              df_breakdown_diperiksa_bln.iloc[:,3].sum(),
                                                                              df_breakdown_diperiksa_bln.iloc[:,4].sum(),
                                                                              df_breakdown_diperiksa_bln.iloc[:,5].sum()]
                    df_breakdown_diperiksa_bln = df_breakdown_diperiksa_bln.applymap(format_number)
                    df_breakdown_diperiksa_bln = df_breakdown_diperiksa_bln.style.apply(highlight_last_row, axis=None)
                    st.dataframe(df_breakdown_diperiksa_bln, use_container_width=True, hide_index=True)
                    
            st.markdown('---')
        df = None
        dfs = None
        df_merge = None
        df_merge_final = None
        df_breakdown = None
        df_breakdown2 = None
        df_breakdown_diperiksa = None
        df_breakdown_pengurang = None
        st.cache_data.clear()
        st.cache_resource.clear()
