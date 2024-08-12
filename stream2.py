import streamlit as st
import requests
import zipfile
import io
import pandas as pd
import os
import gdown
import tempfile
import matplotlib.pyplot as plt
import seaborn as sns

def create_stylish_line_plot(df, x_col, y1_col, y2_col, title="Stylish Line Plot", x_label="X", y_label="Values"):
    """
    Membuat line plot yang menarik dengan dua kolom y berbeda dan kolom x sebagai sumbu x.

    Parameters:
    - df: DataFrame yang berisi data.
    - x_col: Nama kolom yang akan digunakan sebagai sumbu x.
    - y1_col: Nama kolom yang akan digunakan sebagai garis pertama.
    - y2_col: Nama kolom yang akan digunakan sebagai garis kedua.
    - title: Judul plot.
    - x_label: Label untuk sumbu x.
    - y_label: Label untuk sumbu y.
    """
    
    # Menggunakan seaborn style untuk plot yang lebih menarik
    sns.set(style="whitegrid")

    # Membuat figure dan axis
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plotting kolom y1
    ax.plot(df[x_col], df[y1_col], label='SELISIH', marker='o', markersize=8, linewidth=2, color='dodgerblue')

    # Plotting kolom y2
    ax.plot(df[x_col], df[y2_col], label='CANCEL NOTA', marker='o', markersize=8, linewidth=2, color='orange')
    # Menambahkan judul dengan font lebih besar dan bold
    ax.set_title(title, fontsize=20, fontweight='bold', color='darkblue', pad=20)

    # Menambahkan label sumbu dengan font lebih besar
    ax.set_xlabel(x_label, fontsize=15, fontweight='bold')
    ax.set_ylabel(y_label, fontsize=15, fontweight='bold')

    # Menambahkan anotasi pada titik tertinggi di Y1

    # Menambahkan legenda dengan pengaturan posisi dan font
    ax.legend(title_fontsize='13', fontsize='12', loc='upper left', frameon=True, shadow=True)

    # Menambahkan grid lebih halus dan tampak lebih rapi
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

    # Menambahkan batasan sumbu untuk sedikit ruang di sekitar garis
    #ax.set_xlim([df[x_col].min() - 0.5, df[x_col].max() + 0.5])
    #ax.set_ylim([df[[y1_col, y2_col]].min().min() - 0.05, df[[y1_col, y2_col]].max().max()])

    # Menghilangkan garis di bagian atas dan kanan
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Mengubah warna dan ukuran tick labels
    ax.tick_params(axis='x', colors='darkblue', size=10)
    ax.tick_params(axis='y', colors='darkblue', size=10)


    # Menampilkan plot
    plt.show()
    
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

def download_file_from_google_drive(file_id, dest_path):
    if not os.path.exists(dest_path):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, dest_path, quiet=False)

        
file_id = '1BP3-98cKLKgY3flpsyuhjbE7zXWNSN3V'
dest_path = f'downloaded_file.zip'
download_file_from_google_drive(file_id, dest_path)

if 'df_merge' not in locals():
    with zipfile.ZipFile(f'downloaded_file.zip', 'r') as z:
        with z.open('df_selisih.csv') as f:
            df_selisih = pd.read_csv(f)
        with z.open('merge_clean.csv') as f:
            df_merge = pd.read_csv(f)
        with z.open('breakdown_clean.csv') as f:
            df_breakdown = pd.read_csv(f)
            
all_cab_selisih = st.multiselect('Pilih Cabang', ['All'] + list_cab['CAB'].sort_values().unique(),default=['All'])
all_cab_selisih = list(all_cab)

if 'All' in all_cab_selisih:
    create_stylish_line_plot(df_selisih, 'MONTH', '%_SELISIH', '%_CANCEL NOTA', title="", x_label="Month", y_label="Percentage")

st.title('Data - Selisih Ojol')
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
    

            
# Tombol untuk mengeksekusi aksi
if st.button('Process'):
    st.session_state.button_clicked = True
    
# Eksekusi kode jika tombol diklik
if st.session_state.button_clicked:
        df_merge = df_merge[df_merge['MONTH'].isin(all_bulan)]
        df_breakdown = df_breakdown[df_breakdown['MONTH'].isin(all_bulan)]
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
            df_breakdown_pengurang = df_breakdown2[df_breakdown2['Kategori'].isin([x.upper() for x in kat_pengurang])].groupby(['MONTH','Kategori'])[df_breakdown.columns[-5:]].sum().reset_index()
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
            df_breakdown_diperiksa = df_breakdown2[df_breakdown2['Kategori'].isin([x.upper() for x in kat_diperiksa])].groupby(['MONTH','Kategori'])[df_breakdown.columns[-5:]].sum().reset_index()
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
