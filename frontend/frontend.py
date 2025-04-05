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
from dynamic_filter import dynamic_filter 



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


# Define translations
translations = {
    "English": {
        "title": "Welcome to HDB Decode",
        "description": "HDB Decode is an innovative platform designed to help you make smarter decisions when buying or selling second-hand HDB flats. Our price prediction algorithms and filtering tools simplify the home-buying experience — whether you're a first-time buyer or a seasoned property investor.",
        "homepage1": "What can HDB Decode do?",
        "homepage2" : "**Understand Market Trends 💸**",
        "homepage3" : "Get insights into price movements so you can time your purchase wisely.",
        "homepage4" : "Go to Price Trend",
        "homepage5" : "**Accurate Price Predictions 💰**",
        "homepage6" : "Know what a fair price should be, and avoid overpaying for your next home.",
        "homepage7" : "Go to Price Prediction",
        "homepage8" : "**Find Your Ideal Home 🔎**",
        "homepage9" : "Easily filter properties by price, location, and quality to find your ideal home.",
        "homepage10" : "Go to Home Finder",
        "price1" : "HDB Price Trend",
        "price2" : "Resale Transactions by Price Category",
        "price3" : "🔍 Key Trends in HDB Resale Market",
        "price4" : "🏠 Fewer resale flats priced below $300k in recent years",
        "price5" : "💸 Strong growth in high-value transactions ($700k and above), especially post-2021",
        "price6" : "📉 Sharp dip in transactions in early 2020 due to COVID-19, followed by strong recovery",
        "price7" : "📈 Rising resale prices driven by demand, inflation, and market trends",
        "price8" : "🔺 Overall increase in proportion of more expensive HDBs ($500k and above)",
        "price9" : "Average Price Over Time",
        "price10" : "You can select Town, Number of Rooms, and Remaining Lease Years to view a more specific monthly trend of resale HDB prices. If you don't choose any filters, the chart will show the overall trend for all resale HDB flats.",
        "price11" : "Select a Town:",
        "price12" : "Select Number of Rooms:",
        "price13" : "Select Remaining Lease Years:",
        "predict1" : "Predict Your HDB Price",
        "predict2" : "Enter Your HDB Details",
        "predict3" : "Postal Code",
        "predict4" : "Floor Area (sqm)",
        "predict5" : "Floor Number",
        "predict6" : "Number of Years of Remaining Lease",
        "predict7" : "Predict Price",
        "sidebar1" : "🏠 Homepage",
        "sidebar2" : "📊 HDB Price Trend",
        "sidebar3" : "📈 Predict Your HDB Price",
        "sidebar4" : "🏡 Find Your Ideal Home",
        "contact": "**Need help? Contact us at hdbdecode@gmail.com**",
        "navigation" : "Menu"
        
    },
    "华文": {
        "title": "欢迎来到 HDB Decode",
        "description": "HDB Decode 是一个全新的平台，致力于帮助您在购买或出售二手组屋时做出更明智的决策。借助我们的价格预测算法和智能筛选工具，我们致力于为每一位用户打造轻松愉快的购房体验——无论您是首次置业的新手，还是经验丰富的房地产投资者。",
        "homepage1": "HDB Decode 有什么功能？",
        "homepage2" : "**洞察市场趋势 💸**",
        "homepage3" : "掌握价格变动，选对购房时机。",
        "homepage4" : "前往价格趋势",
        "homepage5" : "**精准的价格预测 💰**",
        "homepage6" : "掌握合理房价，让您不再为下一个家多花冤枉钱。",
        "homepage7" : "前往价格预测",
        "homepage8" : "**寻找理想的家 🔎**",
        "homepage9" : "可根据价格、地点和房屋质量轻松筛选，快速锁定理想房源。",
        "homepage10" : "前往HDB查找器",
        "price1" : "HDB 价格趋势",
        "price2" : "按价格类别划分的转售交易",
        "price3" : "🔍 HDB 转售市场的主要趋势",
        "price4" : "🏠 近年来，售价低于 30 万美元的转售公寓数量减少",
        "price5" : "💸 高价值交易（70 万新币及以上）强劲增长，尤其是在 2021 年之后",
        "price6" : "📉 2020 年初受新冠疫情影响急剧下滑，随后强劲复苏",
        "price7" : "📈 通货膨胀和市场趋势推动转售价格上涨",
        "price8" : "🔺 随着时间的推移，整体上转向价格更高的 HDB",
        "price9" : "历时平均价格",
        "price10" : "请选择您感兴趣的城镇、房间数和 HDB 剩余年限，以根据不同的过滤器查看转售 HDB 价格的每月趋势！",
        "price11" : "选择一个城镇:",
        "price12" : "选择房间数量:",
        "price13" : "选择剩余年限:",
        "predict1" : "预测您的 HDB 价格",
        "predict2" : "输入您的 HDB 详细信息",
        "predict3" : "邮政编码",
        "predict4" : "建筑面积 (sqm)",
        "predict5" : "楼层数",
        "predict6" : "剩余年限",
        "predict7" : "预测价格",
        "sidebar1" : "🏠 首页",
        "sidebar2" : "📊 组屋价格趋势",
        "sidebar3" : "📈 预测您的 HDB 价格",
        "sidebar4" : "🏡 找到理想的家",
        "contact": "**有问题或需要帮助？欢迎通过 hdbdecode@gmail.com 联系我们!**",
        "navigation" : "菜单"
    },
    "Bahasa Melayu": {
        "title": "Selamat datang ke HDB Decode",
        "description": "HDB Decode ialah platform inovatif yang direka untuk membantu anda membuat keputusan yang lebih bijak apabila membeli atau menjual flat HDB jualan semula. Algoritma ramalan harga dan alat tapis kami memudahkan pengalaman membeli rumah — sama ada anda pembeli kali pertama atau pelabur hartanah berpengalaman.",
        "homepage1": "Apa yang boleh HDB Decode lakukan?",
        "homepage2" : "**Fahami Trend Pasaran 💸**",
        "homepage3" : "Dapatkan cerapan tentang pergerakan harga supaya anda boleh menentukan masa pembelian anda dengan bijak.",
        "homepage4" : "Trend Harga",
        "homepage5" : "**Ramalan Harga Tepat 💰**",
        "homepage6" : "Ketahui harga yang berpatutan, dan elak membayar lebih untuk rumah anda yang seterusnya.",
        "homepage7" : "Ramalan Harga",
        "homepage8" : "**Cari Rumah Impian Anda 🔎**",
        "homepage9" : "Tapis hartanah mengikut harga, lokasi dan kualiti dengan mudah untuk mencari rumah impian anda.",
        "homepage10" : "Carian Rumah",
        "price1" : "Trend Harga HDB",
        "price2" : "Transaksi Jualan Semula mengikut Kategori Harga",
        "price3" : "🔍 Trend Utama dalam Pasaran Jualan Semula HDB",
        "price4" : "🏠 Kurang rumah pangsa jualan semula berharga di bawah $300k dalam beberapa tahun kebelakangan ini",
        "price5" : "💸 Pertumbuhan kukuh transaksi bernilai tinggi (lebih $700k), terutamanya selepas 2021",
        "price6" : "📉 Penurunan mendadak bilangan transaksi awal 2020 disebabkan oleh COVID-19, diikuti dengan pemulihan yang kukuh",
        "price7" : "📈 Harga jualan semula yang meningkat didorong oleh permintaan, inflasi dan trend pasaran",
        "price8" : "🔺 Peralihan keseluruhan ke arah flat HDB berharga lebih tinggi (lebih $500k)",
        "price9" : "Harga Purata Sepanjang Masa",
        "price10" : "Sila pilih Bandar, Bilangan Bilik dan Baki Tahun Pajakan yang anda berminat untuk melihat trend bulanan harga jualan semula HDB berdasarkan penapis yang berbeza!",
        "price11" : "Pilih Bandar:",
        "price12" : "Pilih Bilangan Bilik:",
        "price13" : "Pilih Baki Tahun Pajakan:",
        "predict1" : "Ramalkan Harga HDB Anda",
        "predict2" : "Masukkan Butiran HDB Anda",
        "predict3" : "Poskod",
        "predict4" : "Luas Lantai (sqm)",
        "predict5" : "Nombor Lantai",
        "predict6" : "Bilangan Tahun Baki Pajakan",
        "predict7" : "Ramalkan Harga",
        "sidebar1" : "🏠 Laman Utama",
        "sidebar2" : "📊 Trend Harga HDB",
        "sidebar3" : "📈 Ramalkan Harga HDB Anda",
        "sidebar4" : "🏡 Cari Rumah Impian Anda",
        "contact": "**Perlu bantuan? Hubungi kami di hdbdecode@gmail.com**",
        "navigation" : "Menu"
    },
    "தமிழ்": {
        "title": "HDB Decodeக்கு உங்களை வரவேற்கிறோம்",
        "description": "HDB Decode என்பது பயன்படுத்தப்பட்ட HDB பிளாட்களை வாங்கும்போதோ அல்லது விற்கும்போதோ சிறந்த முடிவுகளை எடுக்க உதவும் வகையில் வடிவமைக்கப்பட்ட ஒரு புதுமையான தளமாகும். எங்கள் விலை கணிப்பு வழிமுறைகள், வடிகட்டுதல் கருவிகள் மற்றும் முதியோர்களுக்கு ஏற்ற அம்சங்கள் வீடு வாங்கும் அனுபவத்தை எளிதாக்குகின்றன - நீங்கள் முதல் முறையாக வாங்குபவராக இருந்தாலும் சரி அல்லது அனுபவம் வாய்ந்த சொத்து முதலீட்டாளராக இருந்தாலும் சரி.",
        "homepage1": "HDB Decode என்ன செய்ய முடியும்?",
        "homepage2" : "**சந்தைப் போக்குகளைப் புரிந்து கொள்ளுங்கள் 💸**",
        "homepage3" : "விலை நகர்வுகள் பற்றிய நுண்ணறிவுகளைப் பெறுங்கள், இதன் மூலம் உங்கள் கொள்முதலை புத்திசாலித்தனமாக திட்டமிடலாம்.",
        "homepage4" : "விலைப் போக்குக்குச் செல்லவும்",
        "homepage5" : "**துல்லியமான விலை கணிப்புகள் 💰**",
        "homepage6" : "நியாயமான விலை என்னவாக இருக்க வேண்டும் என்பதை அறிந்து கொள்ளுங்கள், மேலும் உங்கள் அடுத்த வீட்டிற்கு அதிக கட்டணம் செலுத்துவதைத் தவிர்க்கவும்.",
        "homepage7" : "விலைக் கணிப்புக்குச் செல்லவும்",
        "homepage8" : "**உங்கள் சிறந்த வீட்டைக் கண்டறியவும் 🔎**",
        "homepage9" : "உங்கள் சிறந்த வீட்டைக் கண்டுபிடிக்க விலை, இருப்பிடம் மற்றும் தரம் ஆகியவற்றின் அடிப்படையில் சொத்துக்களை எளிதாக வடிகட்டவும்.",
        "homepage10" : "Home Finder க்குச் செல்லவும்",
        "price1" : "HDB விலை போக்கு",
        "price2" : "விலை வகை வாரியாக மறுவிற்பனை பரிவர்த்தனைகள்",
        "price3" : "🔍 HDB மறுவிற்பனை சந்தையில் முக்கிய போக்குகள்",
        "price4" : "🏠 சமீபத்திய ஆண்டுகளில் $300,000க்கும் குறைவான விலையில் மறுவிற்பனை செய்யப்பட்ட பிளாட்கள் குறைவு.",
        "price5" : "💸 அதிக மதிப்புள்ள பரிவர்த்தனைகளில் வலுவான வளர்ச்சி ($700k மற்றும் அதற்கு மேல்), குறிப்பாக 2021க்குப் பிறகு",
        "price6" : "📉 கோவிட்-19 காரணமாக 2020 ஆம் ஆண்டின் தொடக்கத்தில் கூர்மையான சரிவு, அதைத் தொடர்ந்து வலுவான மீட்சி",
        "price7" : "📈 தேவை, பணவீக்கம் மற்றும் சந்தைப் போக்குகளால் உந்தப்படும் மறுவிற்பனை விலைகள் உயர்வு",
        "price8" : "🔺 காலப்போக்கில் அதிக விலை கொண்ட HDB பிளாட்களை நோக்கி ஒட்டுமொத்த மாற்றம்",
        "price9" : "காலப்போக்கில் சராசரி விலை",
        "price10" : "வெவ்வேறு வடிப்பான்களின் அடிப்படையில் HDB மறுவிற்பனை விலையின் மாதாந்திர போக்கைக் காண, HDB-க்கு நீங்கள் ஆர்வமாக உள்ள நகரம், அறைகளின் எண்ணிக்கை மற்றும் மீதமுள்ள குத்தகை ஆண்டுகளைத் தேர்ந்தெடுக்கவும்!",
        "price11" : "ஒரு நகரத்தைத் தேர்ந்தெடுக்கவும்:",
        "price12" : "அறைகளின் எண்ணிக்கையைத் தேர்ந்தெடுக்கவும்:",
        "price13" : "மீதமுள்ள குத்தகை ஆண்டுகளைத் தேர்ந்தெடுக்கவும்:",
        "predict1" : "உங்கள் HDB’யின் விலையை கணிக்கவும்",
        "predict2" : "உங்கள் HDB விவரங்களை உள்ளிடவும்",
        "predict3" : "அஞ்சல் குறியீடு",
        "predict4" : "தரை பரப்பளவு (sqm)",
        "predict5" : "மாடி எண்",
        "predict6" : "மீதமுள்ள குத்தகை ஆண்டுகளின் எண்ணிக்கை",
        "predict7" : "விலையை கணிக்க",
        "sidebar1" : "🏠 முகப்புப்பக்கம்",
        "sidebar2" : "📊 HDB விலை போக்கு",
        "sidebar3" : "📈 உங்கள் HDB விலையை கணிக்கவும்",
        "sidebar4" : "🏡 உங்கள் சிறந்த வீட்டைக் கண்டறியவும்",
        "contact": "**உதவி தேவையா? hdbdecode@gmail.com என்ற முகவரியில் எங்களைத் தொடர்பு கொள்ளவும்.**",
        "navigation" : "வழிசெலுத்தல்"
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
    st.title(t["title"])
    st.write(t["description"])
    
    st.markdown("---")
    st.header(t["homepage1"])

    st.markdown(t["homepage2"])
    st.markdown(t["homepage3"])
    if st.button(t["homepage4"], key="home_trend_btn"):
        st.query_params["page"] = "HDB Price Trend"
        st.session_state.page = "HDB Price Trend"
        st.rerun()
            
    left_col, right_col = st.columns([1.3, 1]) 

    with left_col:


   
        st.markdown(t["homepage5"])
        st.markdown(t["homepage6"])
        if st.button(t["homepage7"], key="home_predict_btn"):
            st.query_params["page"] = "Predict Your HDB Price"
            st.session_state.page = "Predict Your HDB Price"
            st.rerun()

        st.markdown(t["homepage8"])
        st.markdown(t["homepage9"])
        if st.button(t["homepage10"], key="home_finder_btn"):
            st.query_params["page"] = "Find Your Ideal Home"
            st.session_state.page = "Find Your Ideal Home"
            st.rerun()

    with right_col:
        st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)
        st.image("/Users/hushiqi/Desktop/DSE3101-HDB-Decode/frontend/hdb5.jpeg", use_container_width=True)


    
    st.markdown("---")
    st.markdown(t["contact"])

# Plot HDB Price Trend
elif page == "HDB Price Trend":
    
    st.title(t["price1"])
    
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
    st.subheader(t["price2"])
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_axisbelow(True)
    category_counts.plot(kind='bar', stacked=True, colormap='viridis', width=0.8, ax=ax)
    ax.set_title("Resale Transactions by Price Category")
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
    
    st.subheader(t["price3"])

    st.markdown(
    f"""
    - {t['price4']}
    - {t['price5']}
    - {t['price6']}
    - {t['price7']}
    - {t['price8']}
    """
    )

    st.subheader(t["price9"])
    st.warning(t["price10"])


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
        selected_town = st.selectbox(t["price11"], ["All"] + unique_towns, index=0)
    with col2:
        selected_flat_type = st.selectbox(t["price12"], ["All"] + unique_flat_type, index=0)
    with col3:
        selected_remaining_lease_years = st.selectbox(t["price13"], ["All"] + unique_lease_range, index=0)

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

    
    st.markdown("---")
    st.markdown(t["contact"])



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


    
    st.markdown("---")
    st.markdown(t["contact"])

    
 

elif page == "Find Your Ideal Home":

    @st.cache_data
    def load_data():
        return pd.read_csv("resale_price_cleaned.csv")

    df = load_data()

    # --- Page UI ---
    st.title("Find Your Ideal HDB")

    st.markdown("Select your budget and flat type, then choose 3 to 5 filters to narrow down your home search.")

    # Required filters
    budget_range = st.slider("Select your Budget Range (SGD)", 100000, 1500000, (400000, 700000), step=10000)

    flat_type_map = {
        "1 ROOM": 1,
        "2 ROOM": 2,
        "3 ROOM": 3,
        "4 ROOM": 4,
        "5 ROOM": 5,
        "6 ROOM": 6,
        "JUMBO": 7
    }

    selected_labels = st.multiselect("Select Flat Type", list(flat_type_map.keys()))
    flat_types = [flat_type_map[lbl] for lbl in selected_labels if lbl in flat_type_map]


    if budget_range and flat_types:
        # --- Optional Filters ---
        all_filters = ['town', 'storey_range', 'floor_area_sqm', 'remaining_lease', 'nearest_mrt_distance', 'nearest_bus_distance', 'education_score', 'shopping_score', 'food_score', 'recreation_score', 'healthcare_score']
        filter_order = st.multiselect("Choose up to 5 filters:", all_filters, max_selections=5)

        filter_values = {}

        if 'town' in filter_order:
            filter_values['town'] = st.multiselect("Select Town(s):", sorted(df['town'].dropna().unique()))

        if 'storey_range' in filter_order:
            storey = st.slider("Select Storey Range:", 1, 50, (5, 25))
            filter_values['storey_range'] = storey

        if 'floor_area_sqm' in filter_order:
            area = st.slider("Select Floor Area (sqm):", 30, 150, (70, 100))
            filter_values['floor_area_sqm'] = area

        if 'remaining_lease' in filter_order:
            lease = st.slider("Select Remaining Lease (Years):", 1, 99, (60, 99))
            filter_values['remaining_lease'] = lease

        if 'nearest_mrt_distance' in filter_order:
            mrt_choice = st.selectbox("Max MRT Distance:", ['<100m', '<500m', '<1km', '<2km', '<3km'])
            filter_values['nearest_mrt_distance'] = {
                '<100m': 100,
                '<500m': 500,
                '<1km': 1000,
                '<2km': 2000,
                '<3km': 3000
            }[mrt_choice]

        if 'nearest_bus_distance' in filter_order:
            bus_choice = st.selectbox("Max Bus Distance:", ['<100m', '<500m', '<1km'])
            filter_values['nearest_bus_distance'] = {'<100m': 100, '<500m': 500, '<1km': 1000}[bus_choice]

        for score in ['education_score', 'shopping_score', 'food_score', 'recreation_score', 'healthcare_score']:
            if score in filter_order:
                val = st.slider(f"Min {score.replace('_', ' ').title()} (1-5)", 1, 5, 3)
                filter_values[score] = val



        # --- Filter Button ---
        if st.button("Find My HDB"):
            results = dynamic_filter(df, budget_range, flat_types, filter_order, filter_values)
            st.write(f"### Showing top {min(len(results), 10)} of {len(results)} results")
            st.dataframe(results.head(10))

            
    st.markdown("---")
    st.markdown(t["contact"])

