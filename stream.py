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
from st_aggrid import AgGrid, GridOptionsBuilder
import plotly.graph_objs as go
import streamlit as st

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
    
    # Membuat trace untuk y1
    trace1 = go.Scatter(
        x=df[x_col],
        y=df[y1_col],
        mode='lines+markers',
        name=f'{y1_col}',
        line=dict(color='dodgerblue', width=2),
        marker=dict(size=8)
    )

    # Membuat trace untuk y2
    trace2 = go.Scatter(
        x=df[x_col],
        y=df[y2_col],
        mode='lines+markers',
        name=f'{y2_col}',
        line=dict(color='orange', width=2),
        marker=dict(size=8)
    )

    # Membuat layout untuk plot
    layout = go.Layout(
        title=dict(text=title, x=0.5, font=dict(size=20, color='darkblue')),
        xaxis=dict(title=x_label, titlefont=dict(size=16, color='darkblue')),
        yaxis=dict(title=y_label, titlefont=dict(size=16, color='darkblue')),
        showlegend=True,
        legend=dict(font=dict(size=12), x=0, y=1, xanchor='left', yanchor='top'),
        margin=dict(l=50, r=50, t=50, b=50),
        hovermode='closest',
        plot_bgcolor='white',
        xaxis_gridcolor='lightgray',
        yaxis_gridcolor='lightgray',
        shapes=[
            # Garis putus-putus merah di y=0.5
            dict(
                type="line",
                x0=df[x_col].min(), x1=df[x_col].max(),
                y0=0.5, y1=0.5,
                line=dict(color="red", width=1, dash="dash")
            )
        ]
    )

    # Membuat figure dari trace dan layout
    fig = go.Figure(data=[trace1, trace2], layout=layout)

    # Menampilkan plot di Streamlit
    st.plotly_chart(fig, use_container_width=True)

    
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

        
file_id = '1SPwhedLNXLpsqXL3TsoIkxFEzmqK2P5y'
dest_path = f'downloaded_file.zip'
download_file_from_google_drive(file_id, dest_path)


def highlight_last_row(x):
    font_color = 'color: white;'
    background_color = 'background-color: #FF4B4B;'  # Warna yang ingin digunakan
    df_styles = pd.DataFrame('', index=x.index, columns=x.columns)
    
    # Memberikan warna khusus pada baris terakhir yang bernama 'SELISIH'
    df_styles.iloc[-1, :] = font_color + background_color

    return df_styles
               
def format_number(x):
    if x==0:
        return ''
    if isinstance(x, (int, float)):
        return "{:,.0f}".format(x)
    return x

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

if 'df_merge' not in locals():
    with zipfile.ZipFile(f'downloaded_file.zip', 'r') as z:
        with z.open('df_selisih_agustus.csv') as f:
            df_selisih = pd.read_csv(f)
        with z.open('merge_clean_agustus.csv') as f:
            df_merge = pd.read_csv(f)
        with z.open('breakdown_clean_agustus.csv') as f:
            df_breakdown = pd.read_csv(f)
        with z.open('PIC Ojol.xlsx') as f:
            pic = pd.read_excel(f)
        with z.open('CNS_NASIONAL.xlsx') as f:
            s_nas = pd.read_excel(f,sheet_name='SELISIH')
            cn_nas = pd.read_excel(f,sheet_name='CANCELNOTA')


st.header('Selisih', divider='gray')
st.caption('Selisih atas kategori diperiksa')

s_nas['CAB'] = s_nas['CAB'].str.split('.').str[-1]
s_nas['SELISIH'] = abs(s_nas['SELISIH'])
s_nas['MONTH'] = s_nas['MONTH'].dt.strftime('%B %Y')

cn_nas['CAB'] = cn_nas['CAB'].str.extract(r'\((.*?)\)')[0].fillna(cn_nas['CAB'])
cn_nas['CANCEL NOTA'] = abs(cn_nas['CANCEL NOTA'])

df_pic = df_breakdown[df_breakdown['Kategori'].isin([x.upper() for x in kat_diperiksa])].groupby(['MONTH','CAB'])[df_breakdown.columns[-5:]].sum().sum(axis=1).reset_index().rename(columns={0:'SELISIH'})
df_pic = df_pic.merge(pic,how='left',left_on=['CAB','MONTH'],right_on =['NAMA RESTO','BULAN']).groupby(['NAMA PIC','MONTH','CAB'])[['SELISIH']].sum().reset_index()
df_pic['SELISIH'] = abs(df_pic['SELISIH'])
#df_pic = pd.concat([df_pic,df_pic2],ignore_index=True)
df_pic = df_pic[df_pic['SELISIH']!=0]


df_pic = df_pic.sort_values(['NAMA PIC','MONTH'])
df_pic = df_pic.pivot(index=['NAMA PIC','CAB'],columns='MONTH',values='SELISIH').reset_index().reset_index()
df_pic = df_pic.melt(id_vars=['index','NAMA PIC','CAB'])

df_pic2 = df_pic[(df_pic['value'].isna())]
df_pic1 = df_pic[~(df_pic['value'].isna())].rename(columns={'value':'SELISIH'})
df_pic2 = df_pic2.merge(s_nas,how='left').fillna(0).drop(columns='value')

df_pic = pd.concat([df_pic1,df_pic2],ignore_index=True)
df_pic['Tanggal'] = pd.to_datetime(df_pic['MONTH'], format='%B %Y')
df_pic['MONTH'] = pd.Categorical(df_pic['MONTH'], categories=df_pic.sort_values('Tanggal')['MONTH'].unique(), ordered=True)
df_pic = df_pic.sort_values(['NAMA PIC','MONTH']).pivot(index=['NAMA PIC','CAB'],columns='MONTH',values='SELISIH').reset_index()
#df_pic = df_pic.fillna(0).style.format(lambda x: format_number(x)).background_gradient(cmap='Reds', axis=1, subset=df_pic.columns[2:])

styled_pivot_df = df_pic.style.format(lambda x: f"{format_number(x)}").background_gradient(cmap='Reds', axis=1, subset=df_pic.columns[2:])

def apply_red_symbol(row):
    for col in df_pic.columns:
        # Menambahkan simbol merah berdasarkan referensi
        row[col] = add_red_symbol(row[col], row, col)
    return row
    
# Membuat fungsi untuk menambahkan simbol 🔴 pada cell tertentu
def add_red_circle(val, row_index, col_name, zip_condition):
    # Mengecek apakah pasangan (index, MONTH) ada di dalam zip_condition
    if (row_index, col_name) in zip_condition:
        return 'attr: val;color:red;'  # Menambahkan simbol 🔴 jika kondisi terpenuhi
    else:
        return 'attr: val;'  # Jika tidak, nilai tetap seperti semula

# Menyusun pasangan (index, MONTH) dari df_pic2
zip_condition = list(zip(df_pic2['index'], df_pic2['MONTH']))

cell_styles = [
    {
        'selector': f'td[data-colname="{col_name}"][data-rowindex="{row_index}"]',
        'props': [('color', 'red')]
    }
    for row_index, col_name in zip_condition
]

# Terapkan gaya CSS ke DataFrame
styled_pivot_df = styled_pivot_df.set_table_styles(cell_styles)

st.dataframe(styled_pivot_df, use_container_width=True, hide_index=True) 
