import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import base64
import plotly.express as px
import os
from dynamic_filter import dynamic_filter 
from folium.features import CustomIcon
from translations import get_translations
from homepage import homepage
from hdb_price_trend import hdb_price_trend
from predict_hdb_price import predict_hdb_price
from ideal_home import ideal_home

#Page layout
st.set_page_config(page_title="HDB Prediction and Finder", layout="wide")

st.markdown("""
    <style>
    html, body, div, p, span, label {
        font-size: 18px !important;
    }

    .stMarkdown, .stText, .stTextInput, .stSelectbox, .stButton {
        font-size: 18px !important;
    }
    </style>
    """, unsafe_allow_html=True)


st.markdown(
    """
    <style>
        .language-container {
            position: fixed;
            top: 5px;
            right: 10px;
            z-index: 1000;
        }
        .language-container select {
            width: auto !important;  /* Make select box smaller */

        }
    </style>
    <div class="language-container" id="language-container"></div>
    """,
    unsafe_allow_html=True,
)


# Language selection using radio buttons
language = st.radio("Select Language:", ["English", "华文", "Bahasa Melayu", "தமிழ்"], horizontal=True)
translations = get_translations()
# Get translations
t = translations[language]


# Move the select box into the custom container
st.markdown(
    """
    <script>
        document.getElementById("language-container").appendChild(
            document.querySelector('div[data-testid="stSelectbox"]')
        );
    </script>
    """,
    unsafe_allow_html=True,
)



logo_path = "photo.jpeg"  

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_base64 = get_image_base64(logo_path)

st.sidebar.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/jpeg;base64,{image_base64}" width="200">
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f5f5f5;  /* Soft background color */
    }
    h1, h2, h3, h4, h5, h6 {
        color: #333333;
        font-size: 30px; /* Larger text */
    }
    .sidebar .sidebar-content {
        background-color: #007bff;  /* Blue background for the sidebar */
        color: white;
        font-size: 20px; /* Larger font size */
        padding: 30px;
        border-radius: 10px;
    }
    .sidebar .sidebar-button {
        background-color: #0056b3; /* Darker blue for buttons */
        color: white;
        padding: 20px;
        font-size: 22px; /* Larger buttons */
        margin-bottom: 15px;
        border-radius: 12px;
        transition: background-color 0.3s;
    }
    .sidebar .sidebar-button:hover {
        background-color: #003366;
    }
    .button {
        background-color: #007bff;
        color: white;
        padding: 15px 30px;
        border-radius: 12px;
        font-size: 22px; /* Large button text */
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .button:hover {
        background-color: #003366;
    }
    .stTextInput input, .stNumberInput input {
        font-size: 20px;
    }
    .stSelectbox, .stRadio, .stButton, .stTextInput, .stNumberInput {
        margin: 10px 0;
    }
    .stMarkdown {
        font-size: 30px;
    }
    .stHeader {
        font-size: 26px;
    }
    .stSelectbox > div, .stRadio > div {
        font-size: 20px;
    }

    .st-radio label {
        font-size: 20px !important; /* Adjust the size as necessary */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Navigation
st.sidebar.title(t["navigation"])
if st.sidebar.button(t["sidebar1"], key="home", help="Go to Homepage", use_container_width=True):
    st.session_state.page = "Homepage"
if st.sidebar.button(t["sidebar2"], key="trend", use_container_width=True):
    st.session_state.page = "HDB Price Trend"
if st.sidebar.button(t["sidebar3"], key="predict", help="Predict your HDB price", use_container_width=True):
    st.session_state.page = "Predict Your HDB Price"
if st.sidebar.button(t["sidebar4"], key="quiz", help="Find your ideal HDB", use_container_width=True):
    st.session_state.page = "Find Your Ideal Home"


# Ensure session state is set for navigation
if "page" not in st.session_state:
    st.session_state.page = "Homepage"

# Page Routing
page = st.session_state.page

# Home Page
if page == "Homepage":
    homepage(t)

# Plot HDB Price Trend
elif page == "HDB Price Trend":
   hdb_price_trend(t) 
   
# Predict Your HDB Price
elif page == "Predict Your HDB Price":
    predict_hdb_price(t)

elif page == "Find Your Ideal Home":
    ideal_home(t)
    