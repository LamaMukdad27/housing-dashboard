# California Housing Dashboard
import streamlit as st
import pandas as pd
from sklearn.datasets import fetch_california_housing

# Page Config
st.set_page_config(page_title="California Housing Dashboard", layout="wide")
st.title("🏠 California Housing Interactive Dashboard")

# Load Data
@st.cache_data
def load_data():
    housing = fetch_california_housing(as_frame=True)
    df = housing.frame.copy()
    
    # Add Population Density
    df["PopulationDensity"] = df["Population"] / df["AveOccup"]
    
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("🔎 Filters")

# Income slider
min_income = float(df["MedInc"].min())
max_income = float(df["MedInc"].max())

income_range = st.sidebar.slider(
    "Median Income Range",
    min_value=min_income,
    max_value=max_income,
    value=(min_income, max_income)
)

# Filter data
filtered_df = df[
    (df["MedInc"] >= income_range[0]) &
    (df["MedInc"] <= income_range[1])
]

st.sidebar.write(f"Rows: {filtered_df.shape[0]}")

# Map Visualization
st.subheader("📍 House Values Map")

map_data = filtered_df[["Latitude", "Longitude"]]

st.map(map_data)

# Scatter Plot
st.subheader("📊 Income vs House Value")

st.scatter_chart(filtered_df[["MedInc", "MedHouseVal"]])

# Summary Statistics
st.subheader("📈 Summary Statistics")

st.dataframe(filtered_df.describe())
