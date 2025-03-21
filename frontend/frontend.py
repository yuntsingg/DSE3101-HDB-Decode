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
import os


st.set_page_config(page_title="HDB Prediction and Finder", layout="wide")

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




st.markdown("""
    <style>
        div[data-testid="stRadio"] label {
            font-size: 14px;  /* Adjust font size */
        }
    </style>
""", unsafe_allow_html=True)

# Language selection using radio buttons
language = st.radio("Select Language:", ["English", "Chinese", "Malay", "Tamil"], horizontal=True)

import streamlit as st

# Define translations
translations = {
    "English": {
        "title": "Welcome to HDB Decode",
        "description": "Easily estimate your HDB resale price and get personalized home recommendations.",
        "contact": "Need help? Contact us at hdbdecode@gmail.com"
    },
    "Chinese": {
        "title": "欢迎来到HDB Decode",
        "description": "轻松估算您的HDB转售价格，并获得个性化的房屋推荐。",
        "contact": "需要帮助？联系我们：hdbdecode@gmail.com"
    },
    "Malay": {
        "title": "Selamat datang ke HDB Decode",
        "description": "Anggarkan harga jualan semula HDB anda dengan mudah dan dapatkan cadangan rumah peribadi.",
        "contact": "Perlu bantuan? Hubungi kami di hdbdecode@gmail.com"
    },
    "Tamil": {
        "title": "HDB Decodeக்கு வரவேற்கிறோம்",
        "description": "உங்கள் HDB மீண்டும் விற்பனை மதிப்பை எளிதாக கணிக்கவும் மற்றும் தனிப்பயன் வீட்டு பரிந்துரைகளைப் பெறவும்.",
        "contact": "உதவி வேண்டுமா? எங்களை hdbdecode@gmail.com இல் தொடர்பு கொள்ளவும்"
    }
}

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
        font-size: 24px; /* Larger text */
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
        font-size: 22px;
    }
    .stHeader {
        font-size: 26px;
    }
    .stSelectbox > div, .stRadio > div {
        font-size: 20px;
    }

    .st-radio label {
        font-size: 18px !important; /* Adjust the size as necessary */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Navigation
st.sidebar.title("Navigation")
if st.sidebar.button("🏠 Homepage", key="home", help="Go to Homepage", use_container_width=True):
    st.session_state.page = "Homepage"
if st.sidebar.button("📈 Predict Your HDB Price", key="predict", help="Predict your HDB price", use_container_width=True):
    st.session_state.page = "Predict Your HDB Price"
if st.sidebar.button("🏡 Find Your Ideal Home", key="quiz", help="Find your ideal HDB", use_container_width=True):
    st.session_state.page = "Find Your Ideal Home"
if st.sidebar.button("❓ Help & About Us", key="help", help="Help and About Us", use_container_width=True):
    st.session_state.page = "Help & About Us"

# Ensure session state is set for navigation
if "page" not in st.session_state:
    st.session_state.page = "Homepage"

# Page Routing
page = st.session_state.page

# Home Page
if page == "Homepage":
    st.title(t["title"])
    st.write(t["description"])
    
    
    # Singapore Heatmap
    st.subheader("Singapore Heatmap")
    # Example data (coordinates of popular areas in Singapore)
    singapore_coords = [[1.3521, 103.8198], [1.2921, 103.7718], [1.2833, 103.8470], [1.3018, 103.8303]]
    
    # Create a folium map
    map_sg = folium.Map(location=[1.3521, 103.8198], zoom_start=12)
    HeatMap(singapore_coords).add_to(map_sg)
    
    # Render the map
    folium_static(map_sg, width=800, height=600)
    
    # Plot Graph of Average Price Over Time
    st.subheader("Average Price Over Time")
    
    # Load Data
    # Get the directory where the script is running
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Construct a relative path to the dataset
    data_path = os.path.join(BASE_DIR, "resale_price_cleaned.csv")

    # Load Data
    df = pd.read_csv(data_path)
    #df = pd.read_csv("/Users/hushiqi/Desktop/DSE3101project/DSE3101-HDB-Decode/data/cleaned/resale_price_cleaned.csv")

    # Convert 'month' column to datetime format
    df['month'] = pd.to_datetime(df['month'])

    # Define lease bins and labels
    bins = [40, 50, 60, 70, 80, 90, 100]
    labels = ["40-50", "50-60", "60-70", "70-80", "80-90", "90-99"]

    df["lease_range"] = pd.cut(df["remaining_lease"], bins=bins, labels=labels, right=False)

    # Extract unique values for dropdowns
    unique_towns = sorted(df['town'].unique().tolist())
    unique_flat_type = sorted(df['flat_type'].unique().tolist())
    unique_lease_range = sorted(df['lease_range'].dropna().unique().tolist())  # Drop NaN to avoid issues

    # Initialize session state for filter selection
    if "selected_town" not in st.session_state:
        st.session_state.selected_town = None
    if "selected_flat_type" not in st.session_state:
        st.session_state.selected_flat_type = None
    if "selected_lease_range" not in st.session_state:
        st.session_state.selected_lease_range = None

    # UI Layout for filters
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_town = st.selectbox("Select a Town:", ["All"] + unique_towns, index=0)
    with col2:
        selected_flat_type = st.selectbox("Select a Flat Type:", ["All"] + unique_flat_type, index=0)
    with col3:
        selected_remaining_lease_years = st.selectbox("Select Remaining Lease Years:", ["All"] + unique_lease_range, index=0)

    # Filter data based on selection
    if selected_town != "All":
        df = df[df["town"] == selected_town]
    if selected_flat_type != "All":
        df = df[df["flat_type"] == selected_flat_type]
    if selected_remaining_lease_years != "All":
        df = df[df["lease_range"] == selected_remaining_lease_years]

    # Aggregate Data: Compute average resale price per month
    price_trends = df.groupby('month')['resale_price'].mean().reset_index()

    # Plot using Plotly
    fig = px.line(price_trends, x='month', y='resale_price',
              labels={'month': 'Month', 'resale_price': 'Average Resale Price'},
              markers=True)

    fig.update_traces(mode="lines+markers", hovertemplate="%{x}: $%{y:.2f}")

    # Show the Plotly chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)




# Predict Your HDB Price
elif page == "Predict Your HDB Price":
    st.title("Predict Your HDB's Price")
    
    st.subheader("Enter Your HDB Details")
    
    # Input fields
    postal_code = st.text_input("Postal Code")
    floor_area = st.number_input("Floor Area (sq ft)", min_value=0)
    floor_number = st.number_input("Floor Number", min_value=0)
    lease_left = st.number_input("Number of Years of Lease Left", min_value=0)
    
    if st.button("Predict Price"):
        # Simulate a prediction model
        if postal_code and floor_area > 0:
            predicted_price = floor_area * 300 + floor_number * 50 + lease_left * 1000  # Example formula
            st.write(f"### Predicted Price: ${predicted_price:,.2f}")
        else:
            st.warning("Please fill out all fields!")

elif page == "Help & About Us":
    st.title("About Us")
    st.write("Welcome to HDB Decode!")
    st.write("Navigating the process of buying or selling an HDB flat can be complex and overwhelming. Homeowners must juggle financial considerations, lifestyle needs, and long-term planning, often with limited access to clear, personalized guidance. Whether resizing, relocating, or optimizing property investments, many struggle with scattered information and uncertainty.")
    st.write("The goal HDB Decode is to simplify this journey by providing data-driven insights and easy-to-use tools, empowering individuals to make informed and confident housing decisions.")
    st.markdown("""
    ### Our platform allows users to:
    - **Predict Property Prices**: Input details about your HDB flat to receive an estimated resale price, helping you make informed financial decisions.  
    - **Find Your Ideal Home**: Specify your desired home characteristics—such as budget, size, and proximity to amenities—and receive recommendations on suitable areas.  
    - **Analyze Market Trends**: View interactive graphs of HDB resale price trends over time, with filtering options by town to gain insights into specific locations.  
    """)

    st.markdown("---")  

    st.markdown("**Need help? Contact us at [hdbdecode@gmail.com](mailto:hdbdecode@gmail.com)**")
 

# Find Your Ideal Home Page

# Initialize session state to track quiz status
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}

# Find Your Ideal Home Page
elif page == "Find Your Ideal Home":
    st.title("Find Your Ideal HDB")

    # Ask user to click a button to start the quiz
    if not st.session_state.quiz_started:
        start_quiz = st.button("Start Quiz")
        if start_quiz:
            st.session_state.quiz_started = True

    if st.session_state.quiz_started:
        st.subheader("Answer the Following Questions to Find Your Ideal HDB")

        # Question 1: Budget Range
        if 'budget' not in st.session_state.quiz_answers:
            budget = st.radio("What is your budget?", ["Below $300,000", "$300,000 - $500,000", "Above $500,000"])
            if st.button("Next"):
                st.session_state.quiz_answers['budget'] = budget
                # Use session state to manage navigation to the next question
                st.experimental_rerun()

        # Question 2: Number of Bedrooms
        elif 'num_bedrooms' not in st.session_state.quiz_answers:
            num_bedrooms = st.selectbox("How many bedrooms would you like?", [1, 2, 3, 4, 5])
            if st.button("Next"):
                st.session_state.quiz_answers['num_bedrooms'] = num_bedrooms
                st.experimental_rerun()

        # Question 3: Proximity to MRT Station
        elif 'proximity_mrt' not in st.session_state.quiz_answers:
            proximity_mrt = st.selectbox("How close do you want your HDB to be to an MRT station?", ["Very Close", "Moderately Close", "Far"])
            if st.button("Next"):
                st.session_state.quiz_answers['proximity_mrt'] = proximity_mrt
                st.experimental_rerun()

        # Question 4: Preferred Town
        elif 'preferred_town' not in st.session_state.quiz_answers:
            preferred_town = st.selectbox("Which town would you prefer?", ["Town A", "Town B", "Town C", "Town D"])
            if st.button("Next"):
                st.session_state.quiz_answers['preferred_town'] = preferred_town
                st.experimental_rerun()

        # After all questions are answered, show the ideal HDB suggestion
        else:
            st.write("### Based on your answers, here is your ideal HDB:")
            st.write(f"**Budget:** {st.session_state.quiz_answers['budget']}")
            st.write(f"**Number of Bedrooms:** {st.session_state.quiz_answers['num_bedrooms']}")
            st.write(f"**Proximity to MRT:** {st.session_state.quiz_answers['proximity_mrt']}")
            st.write(f"**Preferred Town:** {st.session_state.quiz_answers['preferred_town']}")
            st.write("We have found an HDB that matches your preferences!")

            # Reset the quiz for next user
            if st.button("Restart Quiz"):
                st.session_state.quiz_started = False
                st.session_state.quiz_answers = {}
                st.experimental_rerun()
