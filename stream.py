import streamlit as st
import requests
import zipfile
import io
import pandas as pd
import os

# Let's spoof a common user-agent (e.g. Chrome 74 / Windows 10).
# Doing so will fool Apache into thinking that we're making a request
# via the Chrome web browser.
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

url = 'https://drive.google.com/uc?export=download&id=1f-YfvMvFG0UaOw9H5RqNpkPRJEB-8gfa'
request = requests.get(url, stream=True, headers=headers)

# Use the url to determine the filename to save the data as.
# Finally, write out the streamed data as binary data.
zip_filename = os.path.basename(url)
with open(zip_filename, 'wb') as zfile:
    zfile.write(request.content)
st.write(os.listdir())
