import requests
import streamlit as st
from PIL import Image

from dependencies.database import *


@st.cache_data(show_spinner=False)
def fetch(url: String):
    data = Image.open(requests.get(url, stream=True).raw)
    return data
