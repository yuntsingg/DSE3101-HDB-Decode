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

def ideal_home(t):
    @st.cache_data
    def load_data():
        return pd.read_csv("find_your_ideal_home_v3.csv")

    df = load_data()
    df.columns = df.columns.str.strip()


    # --- Page UI ---
    st.title("Find Your Ideal HDB")

    st.markdown("Select your budget and flat type, then choose 3 to 5 filters to narrow down your home search.")

    # Required filters
    budget_range = st.slider("Select your Budget Range (SGD)", 220000, 1550000, (400000, 700000), step=10000)

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
        all_filters = ['town', 'storey_range',  'remaining_lease', 'nearest_mrt_distance', 'nearest_bus_distance', 'education_score', 'shopping_score', 'food_score', 'recreation_score', 'healthcare_score']
        filter_order = st.multiselect("Choose up to 5 filters:", all_filters, max_selections=5)

        filter_values = {}

        if 'town' in filter_order:
            filter_values['town'] = st.multiselect("Select Town(s):", sorted(df['town'].dropna().unique()))

        if 'storey_range' in filter_order:
            storey = st.slider("Select Storey Range:", 1, 50, (5, 25))
            filter_values['storey_range'] = storey


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

        # for score in ['education_score', 'shopping_score', 'food_score', 'recreation_score', 'healthcare_score']:
        #     if score in filter_order:
        #         val = st.slider(f"Min {score.replace('_', ' ').title()} (1-5)", 1, 5, 3)
        #         filter_values[score] = val



        # --- Filter Button ---
        if st.button("Find My HDB"):
            results = dynamic_filter(df, budget_range, flat_types, filter_order, filter_values)
            st.write(f"### Showing top {min(len(results), 10)} of {len(results)} results")
            st.dataframe(results.head(10))
    


    with st.expander("ℹ️ What is the Amenity Score?"):
        st.markdown("""
            **Amenity Score** reflects how well a location is served by key nearby facilities.  
            Scores range from 1️⃣ (few and far) to 5️⃣ (many and nearby), giving you a quick sense of convenience and accessibility.

            We evaluate amenities across five categories:
            - 🏥 **Healthcare**: Clinics, hospitals  
            - 🍽️ **Food**: Food courts  
            - 🛍️ **Shopping**: Supermarkets, malls  
            - 🎓 **Education**: Primary and secondary schools  
            - 🌳 **Recreation**: Parks, gyms, libraries  

            A higher score means better access to essential services and lifestyle options right around the corner.
        """)
        
    st.title(t["ideal1"])

    # Load CSV with postal codes, latitudes, and longitudes
    geospatial_data = pd.read_csv("hdb_geospatial.csv")

    # Initialize session state for storing postal codes
    if "postal_codes" not in st.session_state:
        st.session_state.postal_codes = []

    code = st.text_input(t["ideal2"])

    # Add button to append to list
    if st.button(t["ideal3"]):
        if code and code not in st.session_state.postal_codes:
            if code in geospatial_data["postal_code"].values:
                st.session_state.postal_codes.append(code)
                
            else:
                st.warning(t["ideal4"])

    st.subheader(t["ideal5"])

    cols = st.columns(4)  # Adjust number of columns as needed

    for i, code in enumerate(st.session_state.postal_codes):
        col = cols[i % 4]  # Wrap into columns
        with col:
            st.markdown(f"""
                <div style='
                    border: 1px solid #ccc;
                    padding: 10px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                    background-color: #f9f9f9;
                    text-align: center;
                '>
                    <b>{code}</b>
                </div>
            """, unsafe_allow_html=True)

            # Streamlit delete button below the box
            if st.button(t["ideal6"], key=f"remove_{code}"):
                st.session_state.postal_codes.remove(code)
                st.rerun()


    # Filter geospatial data
    filtered_data = geospatial_data[geospatial_data["postal_code"].isin(st.session_state.postal_codes)]

    # Plot the map
    if not filtered_data.empty:
        m = folium.Map(location=[1.3521, 103.8198], zoom_start=12)
        for _, row in filtered_data.iterrows():
            popup_text = (
                f"Postal Code: {row['postal_code']}<br>"
                f"Nearest MRT: {row['nearest_mrt_name']} ({int(row['nearest_mrt_distance'])}m)<br>"
                f"Nearest Bus Stop: {row['nearest_bus_name']} ({int(row['nearest_bus_distance'])}m)"
            )
            custom_icon = CustomIcon(
                icon_image="location.png",  
                icon_size=(45, 45),  # Resize as needed
            )   
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=folium.Popup(popup_text, max_width=300),
                icon = custom_icon
            ).add_to(m)

        # st.markdown("### 🗺️ Map of Selected HDBs")
        st_folium(m, width=700, height=500)
    else:
        st.info("Add valid postal codes to view them on the map.")
    
    if not filtered_data.empty:
        display_df = filtered_data[[
            "postal_code",
            "nearest_mrt_name",
            "nearest_mrt_distance",
            "nearest_bus_name",
            "nearest_bus_distance"
        ]].rename(columns={
            "postal_code": "Postal Code",
            "nearest_mrt_name": "Nearest MRT",
            "nearest_mrt_distance": "MRT Distance (m)",
            "nearest_bus_name": "Nearest Bus Stop",
            "nearest_bus_distance": "Bus Stop Distance (m)"
        })

        # Round the distances to the nearest whole number
        display_df["MRT Distance (m)"] = display_df["MRT Distance (m)"].round(0).astype(int)
        display_df["Bus Stop Distance (m)"] = display_df["Bus Stop Distance (m)"].round(0).astype(int)

        # Drop the index column (row number)
        display_df = display_df.reset_index(drop=True)

        st.subheader(t["ideal7"])
        st.dataframe(display_df, use_container_width=True)


            
    st.markdown("---")
    st.markdown(t["contact"])

