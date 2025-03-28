import os
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import base64
import plotly.express as px

st.set_page_config(page_title="HDB Prediction and Finder", layout="wide")

# Language Translation Data
translations = {
    "english": {
        "homepage_title": "Welcome to the HDB Decode!",
        "average_price_over_time": "Average Price Over Time",
        "predict_hdb_price": "Predict Your HDB's Price",
        "find_ideal_home": "Find Your Ideal HDB",
        "help_and_about": "Help & About Us",
        "start_quiz": "Start Quiz",
        "budget_question": "What is your budget?",
        "next_button": "Next",
        "ideal_hdb": "Based on your answers, here is your ideal HDB:",
        "restart_quiz": "Restart Quiz"
    },
    "chinese": {
        "homepage_title": "欢迎来到 HDB 解码!",
        "average_price_over_time": "时间上的平均价格",
        "predict_hdb_price": "预测您的 HDB 价格",
        "find_ideal_home": "寻找您的理想 HDB",
        "help_and_about": "帮助和关于我们",
        "start_quiz": "开始测验",
        "budget_question": "您的预算是多少?",
        "next_button": "下一步",
        "ideal_hdb": "根据您的答案，这是您的理想 HDB:",
        "restart_quiz": "重新开始测验"
    },
    "malay": {
        "homepage_title": "Selamat datang ke HDB Decode!",
        "average_price_over_time": "Harga Purata Mengikut Masa",
        "predict_hdb_price": "Ramalkan Harga HDB Anda",
        "find_ideal_home": "Cari HDB Ideal Anda",
        "help_and_about": "Bantuan & Mengenai Kami",
        "start_quiz": "Mula Kuiz",
        "budget_question": "Apakah bajet anda?",
        "next_button": "Seterusnya",
        "ideal_hdb": "Berdasarkan jawapan anda, berikut adalah HDB ideal anda:",
        "restart_quiz": "Mulakan Semula Kuiz"
    },
    "tamil": {
        "homepage_title": "HDB டிகோடு இல் வரவேற்கின்றேன்!",
        "average_price_over_time": "காலப்பகுதியில் சராசரி விலை",
        "predict_hdb_price": "உங்கள் HDB விலையை முன்னறிவிக்கவும்",
        "find_ideal_home": "உங்கள் आदர HDB ஐ கண்டுபிடிக்கவும்",
        "help_and_about": "உதவி மற்றும் எங்களைப் பற்றி",
        "start_quiz": "கேள்வி தொகுப்பை துவங்கு",
        "budget_question": "உங்கள் பட்ஜெட் என்ன?",
        "next_button": "அடுத்தது",
        "ideal_hdb": "உங்கள் பதில்களைப் பொருந்திய HDB:",
        "restart_quiz": "மறுதலாக கேள்வி தொகுப்பை துவங்குங்கள்"
    }
}

# Streamlit select box for language
language = st.selectbox("Select Language", ["English", "Chinese", "Malay", "Tamil"], index=0)

# Map the selected language to the translation dictionary
language_key = language.lower()  # Convert the language to lowercase to match dictionary keys
translations_selected = translations.get(language_key, translations["english"])  # Default to English

# Streamlit UI Configuration
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

# Sidebar Navigation
st.sidebar.title("Navigation")
if st.sidebar.button("🏠 Homepage", key="home", help=translations_selected["homepage_title"], use_container_width=True):
    st.session_state.page = "Homepage"
if st.sidebar.button("📈 Predict Your HDB Price", key="predict", help=translations_selected["predict_hdb_price"], use_container_width=True):
    st.session_state.page = "Predict Your HDB Price"
if st.sidebar.button("🏡 Find Your Ideal Home", key="quiz", help=translations_selected["find_ideal_home"], use_container_width=True):
    st.session_state.page = "Find Your Ideal Home"
if st.sidebar.button("❓ Help & About Us", key="help", help=translations_selected["help_and_about"], use_container_width=True):
    st.session_state.page = "Help & About Us"

# Ensure session state is set for navigation
if "page" not in st.session_state:
    st.session_state.page = "Homepage"

# Page Routing
page = st.session_state.page

# Home Page
if page == "Homepage":
    st.title(translations_selected["homepage_title"])

    # Singapore Heatmap
    st.subheader(translations_selected["average_price_over_time"])
    singapore_coords = [[1.3521, 103.8198], [1.2921, 103.7718], [1.2833, 103.8470], [1.3018, 103.8303]]
    map_sg = folium.Map(location=[1.3521, 103.8198], zoom_start=12)
    HeatMap(singapore_coords).add_to(map_sg)
    folium_static(map_sg, width=800, height=600)

    # Plot Graph of Average Price Over Time
    st.subheader(translations_selected["average_price_over_time"])

    df = pd.read_csv("../data/cleaned/frontend_resale_price_cleaned.csv")
    df['month'] = pd.to_datetime(df['month'])
    bins = [40, 50, 60, 70, 80, 90, 100]
    labels = ["40-50", "50-60", "60-70", "70-80", "80-90", "90-99"]
    df["lease_range"] = pd.cut(df["remaining_lease"], bins=bins, labels=labels, right=False)
    unique_towns = sorted(df['town'].unique().tolist())
    unique_flat_type = sorted(df['flat_type'].unique().tolist())
    unique_lease_range = sorted(df['lease_range'].dropna().unique().tolist())

    if "selected_town" not in st.session_state:
        st.session_state.selected_town = None
    if "selected_flat_type" not in st.session_state:
        st.session_state.selected_flat_type = None
    if "selected_lease_range" not in st.session_state:
        st.session_state.selected_lease_range = None

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_town = st.selectbox("Select a Town:", ["All"] + unique_towns, index=0)
    with col2:
        selected_flat_type = st.selectbox("Select a Flat Type:", ["All"] + unique_flat_type, index=0)
    with col3:
        selected_remaining_lease_years = st.selectbox("Select Remaining Lease Years:", ["All"] + unique_lease_range, index=0)

    if selected_town != "All":
        df = df[df["town"] == selected_town]
    if selected_flat_type != "All":
        df = df[df["flat_type"] == selected_flat_type]
    if selected_remaining_lease_years != "All":
        df = df[df["lease_range"] == selected_remaining_lease_years]

    price_trends = df.groupby('month')['resale_price'].mean().reset_index()

    fig = px.line(price_trends, x='month', y='resale_price',
                  labels={'month': 'Month', 'resale_price': 'Average Resale Price'},
                  markers=True)

    fig.update_traces(mode="lines+markers", hovertemplate="%{x}: $%{y:.2f}")
    st.plotly_chart(fig, use_container_width=True)

# Predict Your HDB Price
elif page == "Predict Your HDB Price":
    st.title(translations_selected["predict_hdb_price"])
    
    st.subheader("Enter Your HDB Details")
    
    postal_code = st.text_input("Postal Code")
    floor_area = st.number_input("Floor Area (sq ft)", min_value=0)
    floor_number = st.number_input("Floor Number", min_value=0)
    lease_left = st.number_input("Number of Years of Lease Left", min_value=0)
    
    if st.button(translations_selected["next_button"]):
        if postal_code and floor_area > 0:
            predicted_price = floor_area * 300 + floor_number * 50 + lease_left * 1000
            st.write(f"### Predicted Price: ${predicted_price:,.2f}")
        else:
            st.warning("Please fill out all fields!")

# Find Your Ideal Home Page
elif page == "Find Your Ideal Home":
    st.title(translations_selected["find_ideal_home"])

    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}

    if not st.session_state.quiz_started:
        start_quiz = st.button(translations_selected["start_quiz"])
        if start_quiz:
            st.session_state.quiz_started = True

    if st.session_state.quiz_started:
        st.subheader(translations_selected["budget_question"])
        if 'budget' not in st.session_state.quiz_answers:
            budget = st.radio(translations_selected["budget_question"], ["Below $300,000", "$300,000 - $500,000", "Above $500,000"])
            if st.button(translations_selected["next_button"]):
                st.session_state.quiz_answers['budget'] = budget
                st.experimental_rerun()

        elif 'num_bedrooms' not in st.session_state.quiz_answers:
            num_bedrooms = st.selectbox("How many bedrooms would you like?", [1, 2, 3, 4, 5])
            if st.button(translations_selected["next_button"]):
                st.session_state.quiz_answers['num_bedrooms'] = num_bedrooms
                st.experimental_rerun()

        elif 'proximity_mrt' not in st.session_state.quiz_answers:
            proximity_mrt = st.selectbox("How close do you want your HDB to be to an MRT station?", ["Very Close", "Moderately Close", "Far"])
            if st.button(translations_selected["next_button"]):
                st.session_state.quiz_answers['proximity_mrt'] = proximity_mrt
                st.experimental_rerun()

        elif 'preferred_town' not in st.session_state.quiz_answers:
            preferred_town = st.selectbox("Which town would you prefer?", ["Town A", "Town B", "Town C", "Town D"])
            if st.button(translations_selected["next_button"]):
                st.session_state.quiz_answers['preferred_town'] = preferred_town
                st.experimental_rerun()

        else:
            st.write(f"### {translations_selected['ideal_hdb']}")
            st.write(f"**Budget:** {st.session_state.quiz_answers['budget']}")
            st.write(f"**Number of Bedrooms:** {st.session_state.quiz_answers['num_bedrooms']}")
            st.write(f"**Proximity to MRT:** {st.session_state.quiz_answers['proximity_mrt']}")
            st.write(f"**Preferred Town:** {st.session_state.quiz_answers['preferred_town']}")
            if st.button(translations_selected["restart_quiz"]):
                st.session_state.quiz_started = False
                st.session_state.quiz_answers = {}
                st.experimental_rerun()
