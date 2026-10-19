
# Tools needed for the app
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup
from io import StringIO

# App title
st.title("GDP by Country and Region")

# Instructions for user
st.write("Select a data source to compare country GDPs by region.")

@st.cache_data
def get_data():

    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
    page = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    tables = BeautifulSoup(page.text, "html.parser").find_all("table", class_="wikitable")

    gdp = pd.read_html(StringIO(str(tables[0])))[0]
    gdp.columns = ["Country/Territory", "IMF", "World Bank", "United Nations"]

    region_url = "https://en.wikipedia.org/w/index.php?title=List_of_countries_by_GDP_(nominal)&oldid=1187446467"
    region_page = requests.get(region_url, headers={"User-Agent": "Mozilla/5.0"})
    region_tables = BeautifulSoup(region_page.text, "html.parser").find_all("table")

    regions = pd.read_html(StringIO(str(region_tables[2])))[0]
    regions = regions.iloc[:, :2]
    regions.columns = ["Country/Territory", "UN region"]

    gdp["Country/Territory"] = gdp["Country/Territory"].str.replace(r"\[.*?\]", "", regex=True).str.strip()
    regions["Country/Territory"] = regions["Country/Territory"].str.replace(r"\[.*?\]", "", regex=True).str.strip()

    # Merge GDP figures with country regions
    data = pd.merge(gdp, regions, on="Country/Territory", how="left")

    return data

# Load the GDP data
data = get_data()

# Allow the user to select the GDP source
source = st.selectbox("Select GDP Source", ["IMF", "World Bank", "United Nations"])

# Keep countries with a known region
plot_data = data[data["UN region"].notna()].copy()
plot_data = plot_data[plot_data["Country/Territory"] != "World"]

# Convert GDP values into numbers
plot_data["GDP"] = pd.to_numeric(
    plot_data[source].astype(str)
    .str.replace(r"\s*\(\d{4}\)", "", regex=True)
    .str.replace(",", "", regex=False),
    errors="coerce"
)

# Remove countries without GDP values for the selected source
plot_data = plot_data.dropna(subset=["GDP"])

# Create interactive stacked bar chart
fig = px.bar(
    plot_data,
    x="UN region",
    y="GDP",
    color="Country/Territory",
    barmode="stack",
    title="Nominal GDP by Country and Region - " + source,
    labels={"GDP": "GDP (million US$)"}
)

# Display the chart in Streamlit
st.plotly_chart(fig)
