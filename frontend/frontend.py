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


# Define translations
translations = {
    "English": {
        "title": "Welcome to HDB Decode",
        "description": "HDB Decode is an innovative platform designed to help you make smarter decisions when buying or selling second-hand HDB flats. Our price prediction algorithms, filtering tools, and elderly-friendly features simplify the home-buying experience — whether you're a first-time buyer or a seasoned property investor.",
        "homepage1": "What can HDB Decode do?",
        "homepage2" : "Understand Market Trends 💸",
        "homepage3" : "Get insights into price movements so you can time your purchase wisely.",
        "homepage4" : "Go to Price Trend",
        "homepage5" : "Accurate Price Predictions 💰",
        "homepage6" : "Know what a fair price should be, and avoid overpaying for your next home.",
        "homepage7" : "Go to Price Prediction",
        "homepage8" : "Find Your Ideal Home 🔎",
        "homepage9" : "Easily filter properties by price, location, and quality to find your ideal home.",
        "homepage10" : "Go to Home Finder",
        "price1" : "HDB Price Trend",
        "price2" : "Resale Transactions by Price Category",
        "price3" : "🔍 Key Trends in HDB Resale Market",
        "price4" : "🏠 Fewer resale flats priced below $300k in recent years",
        "price5" : "💸 Strong growth in high-value transactions ($700k and above), especially post-2021",
        "price6" : "📉 Sharp dip in early 2020 due to COVID-19, followed by strong recovery",
        "price7" : "📈 Rising resale prices driven by demand, inflation, and market trends",
        "price8" : "🔺 Overall shift toward higher-priced HDB flats over time",
        "price9" : "Average Price Over Time",
        "price10" : "Please select the Town, Number of Rooms and Remaining Lease Years you are interested for the HDB to view the monthly trend of resale HDB price based on different filters!",
        "price11" : "Select a Town",
        "price12" : "Select Number of Rooms",
        "price13" : "Select Remaining Lease Years",
        "predict1" : "Predict Your HDB Price",
        "predict2" : "Enter Your HDB Details",
        "predict3" : "Postal Code",
        "predict4" : "Floor Area (sqm)",
        "predict5" : "Floor Number",
        "predict6" : "Number of Years of Remaining Lease",
        "predict7" : "Predict Price",
        "contact": "Need help? Contact us at hdbdecode@gmail.com"
        
    },
    "Chinese": {
        "title": "欢迎来到HDB Decode",
        "description": "HDB Decode 是一个创新平台，旨在帮助您在购买或出售二手组屋时做出更明智的选择。借助我们的价格预测算法、智能筛选工具以及贴心的老人友好功能，我们致力于为每一位用户打造轻松愉快的购房体验——无论您是首次置业的新手，还是在寻找更具洞察力的房产决策参考。", 
        "contact": "需要帮助？联系我们：hdbdecode@gmail.com"
    },
    "Malay": {
        "title": "Selamat datang ke HDB Decode",
        "description": "HDB Decode ialah platform inovatif yang direka untuk membantu anda membuat keputusan yang lebih bijak apabila membeli atau menjual pangsapuri HDB terpakai. Dengan algoritma ramalan harga, alat penapisan, dan ciri mesra warga emas kami, kami bertujuan untuk mempermudahkan pengalaman membeli rumah bagi semua – sama ada anda pembeli rumah kali pertama atau seseorang yang mencari keputusan hartanah yang lebih berpengetahuan.",
        "contact": "Perlu bantuan? Hubungi kami di hdbdecode@gmail.com"
    },
    "Tamil": {
        "title": "HDB Decodeக்கு வரவேற்கிறோம்",
        "description": "HDB Decode என்பது ஒரு புதுமையான தளம், இரண்டாம் கை HDB ஃபிளாட்டுகளை வாங்குவதிலும் விற்குவதிலும் புத்திசாலியான முடிவுகளை எடுக்க உங்களுக்கு உதவுவதற்காக வடிவமைக்கப்பட்டது. எங்களுடைய விலை கணிப்பு ஆல்கொரிதம்கள், வடிகட்டும் கருவிகள் மற்றும் முதியோருக்கு உகந்த அம்சங்களின் மூலம், அனைவருக்கும் வீடு வாங்கும் அனுபவத்தை எளிதாக்குவதே எங்கள் நோக்கம் – நீங்கள் முதல் முறையாக வீடு வாங்குபவராக இருந்தாலும் அல்லது அறிவார்ந்த சொத்து முடிவை எதிர்பார்க்கும் நபராக இருந்தாலும்.",
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
st.sidebar.title("Navigation")
if st.sidebar.button("🏠 Homepage", key="home", help="Go to Homepage", use_container_width=True):
    st.session_state.page = "Homepage"
if st.sidebar.button("📊 HDB Price Trend", key="trend", use_container_width=True):
    st.session_state.page = "HDB Price Trend"
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
    
    st.markdown("---")
    st.header("What can HDB Decode do?")

    st.markdown("#### Understand Market Trends 💸")
    st.markdown("Get insights into price movements so you can time your purchase wisely.")
    if st.button("Go to Price Trend", key="home_trend_btn"):
        st.query_params["page"] = "HDB Price Trend"
        st.session_state.page = "HDB Price Trend"
        st.rerun()

   
    st.markdown("#### Accurate Price Predictions 💰")
    st.markdown("Know what a fair price should be, and avoid overpaying for your next home.")
    if st.button("Go to Price Prediction", key="home_predict_btn"):
        st.query_params["page"] = "Predict Your HDB Price"
        st.session_state.page = "Predict Your HDB Price"
        st.rerun()

    st.markdown("#### Find Your Ideal Home 🔎")
    st.markdown("Easily filter properties by price, location, and quality to find your ideal home.")
    if st.button("Go to Home Finder", key="home_finder_btn"):
        st.query_params["page"] = "Find Your Ideal Home"
        st.session_state.page = "Find Your Ideal Home"
        st.rerun()
            
        
        

    
    st.markdown("---")

# Plot HDB Price Trend
elif page == "HDB Price Trend":
    
    st.title("HDB Price Trend")
    
    # Load Data
    # Get the directory where the script is running
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Construct a relative path to the dataset
    data_path = os.path.join(BASE_DIR, "resale_price_cleaned.csv")

    # Load Data
    df = pd.read_csv(data_path)
    df = df.dropna(subset=['resale_price', 'month'])

    df['month'] = pd.to_datetime(df['month'])


    conditions = [
        (df['resale_price'] < 300000),
        (df['resale_price'] >= 300000) & (df['resale_price'] < 500000),
        (df['resale_price'] >= 500000) & (df['resale_price'] < 700000),
        (df['resale_price'] >= 700000) & (df['resale_price'] < 1000000),
        (df['resale_price'] >= 1000000)]
    categories = ['<300k', '300k-500k', '500k-700k', '700k-1M' ,'>=1M']
    df['Price Category'] = np.select(conditions, categories, default='Unknown')
    category_counts = df.groupby(['month', 'Price Category']).size().unstack(fill_value=0)
    category_counts = category_counts[['<300k', '300k-500k', '500k-700k', '700k-1M', '>=1M']]
    category_counts.index = pd.to_datetime(category_counts.index)

    # Stacked bar chart
    st.subheader("Resale Transactions by Price Category")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_axisbelow(True)
    category_counts.plot(kind='bar', stacked=True, colormap='viridis', width=0.8, ax=ax)
    ax.set_title("Resale Transactions by Price")
    ax.set_ylabel("Transaction Count")
    ax.set_xlabel("")
    ax.set_xticks(range(0, len(category_counts.index), 3))
    years = category_counts.index.year.unique()
    xticks = [category_counts.index.get_loc(f"{year}-01-01") for year in years]
    ax.set_xticks(xticks)
    ax.set_xticklabels(years, rotation=0, fontsize=10)
    ax.legend(title="Price Category")
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)
    
    st.markdown("## 🔍 Key Trends in HDB Resale Market")

    st.markdown("""
    - 🏠 **Fewer resale flats priced below $300k** in recent years  
    - 💸 **Strong growth in high-value transactions** ($700k and above), especially post-2021  
    - 📉 **Sharp dip in early 2020 due to COVID-19**, followed by strong recovery  
    - 📈 **Rising resale prices** driven by demand, inflation, and market trends  
    - 🔺 **Overall shift toward higher-priced HDB flats** over time  
    """)


    st.subheader("Average Price Over Time")
    st.warning('Please select the Town, Number of Rooms and Remaining Lease Years you are interested for the HDB to view the monthly trend of resale HDB price based on different filters!')


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
        selected_flat_type = st.selectbox("Select Number of Rooms:", ["All"] + unique_flat_type, index=0)
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
    fig = px.line(price_trends, x='month',y='resale_price',
              labels={'month': '', 'resale_price': 'Average Resale Price'},
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

    st.markdown(t["contact"])
 

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
                st.rerun()

        # Question 2: Number of Bedrooms
        elif 'num_bedrooms' not in st.session_state.quiz_answers:
            num_bedrooms = st.selectbox("How many bedrooms would you like?", [1, 2, 3, 4, 5])
            if st.button("Next"):
                st.session_state.quiz_answers['num_bedrooms'] = num_bedrooms
                st.rerun()

        # Question 3: Proximity to MRT Station
        elif 'proximity_mrt' not in st.session_state.quiz_answers:
            proximity_mrt = st.selectbox("How close do you want your HDB to be to an MRT station?", ["Very Close", "Moderately Close", "Far"])
            if st.button("Next"):
                st.session_state.quiz_answers['proximity_mrt'] = proximity_mrt
                st.rerun()

        # Question 4: Preferred Town
        elif 'preferred_town' not in st.session_state.quiz_answers:
            preferred_town = st.selectbox("Which town would you prefer?", ["Town A", "Town B", "Town C", "Town D"])
            if st.button("Next"):
                st.session_state.quiz_answers['preferred_town'] = preferred_town
                st.rerun()

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
                st.rerun()
