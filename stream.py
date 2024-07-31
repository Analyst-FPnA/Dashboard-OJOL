import requests

file_id = '1wMeJXGaFF1ku2-txWshzDLaHoxS_tBz0'
url = f'https://drive.google.com/uc?export=download&id={file_id}'
response = requests.get(url, stream=True)

with open('downloaded_file.zip', 'wb') as file:
    for chunk in response.iter_content(chunk_size=8192):
        file.write(chunk)
