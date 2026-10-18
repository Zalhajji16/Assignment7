
# Tools needed for the app
import streamlit as st
import pandas as pd

# App title
st.title("Coordinate Map")

# Instructions for  user
st.write("Enter a latitude and longitude to display the location on a map.")

# User to enter latitude
latitude = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=None, format="%.4f")

# User to enter longitude
longitude = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=None, format="%.4f")

# Check  both coordinates have been entered
if latitude is not None and longitude is not None:

    # Create a table containing the coordinates
    location = pd.DataFrame({"lat": [latitude], "lon": [longitude]})

    # Display the map with a marker at the location
    st.map(location, zoom=10)
