import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Set page config (This should be the first command in the script)
st.set_page_config(page_title="HDB Prediction and Finder", layout="wide")


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
if st.sidebar.button("🏠 Home Page", key="home", help="Go to Home Page", use_container_width=True):
    st.session_state.page = "Home Page"
if st.sidebar.button("📈 Predict Your HDB Price", key="predict", help="Predict your HDB price", use_container_width=True):
    st.session_state.page = "Predict Your HDB Price"
if st.sidebar.button("🏡 Find Your Ideal Home", key="quiz", help="Find your ideal HDB", use_container_width=True):
    st.session_state.page = "Find Your Ideal Home"


# Ensure session state is set for navigation
if "page" not in st.session_state:
    st.session_state.page = "Home Page"

# Page Routing
page = st.session_state.page

# Home Page
if page == "Home Page":
    st.title("Welcome to the HDB Decode!")
    
    # Singapore Heatmap
    st.subheader("Singapore Heatmap")
    # Example data (coordinates of popular areas in Singapore)
    singapore_coords = [[1.3521, 103.8198], [1.2921, 103.7718], [1.2833, 103.8470], [1.3018, 103.8303]]
    
    # Create a folium map
    map_sg = folium.Map(location=[1.3521, 103.8198], zoom_start=12)
    HeatMap(singapore_coords).add_to(map_sg)
    
    # Render the map
    folium_static(map_sg)
    
    # Plot Graph of Average Price Over Time
    st.subheader("Average Price Over Time by Town")
    
    # Example dataset (to simulate the data)
    towns = ['Town A', 'Town B', 'Town C', 'Town D']
    time = pd.date_range("2021-01-01", periods=12, freq="M")
    avg_price_data = {
        "Town A": np.random.randint(300000, 500000, size=12),
        "Town B": np.random.randint(400000, 600000, size=12),
        "Town C": np.random.randint(350000, 550000, size=12),
        "Town D": np.random.randint(450000, 650000, size=12),
    }
    df = pd.DataFrame(avg_price_data, index=time)

    selected_town = st.selectbox("Select a Town to View Average Price Over Time:", towns)
    
    st.write(f"### Average Price for {selected_town} Over Time")
    st.line_chart(df[selected_town])

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
