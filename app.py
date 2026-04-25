# California Housing Dashboard
import streamlit as st
import pandas as pd
from sklearn.datasets import fetch_california_housing
import pydeck as pdk

# Page Configuration
st.set_page_config(
    page_title="California Housing Dashboard",
    layout="wide"
)

st.title("🏠 California Housing Interactive Dashboard")

# Load Dataset
@st.cache_data
def load_data():
    try:
        housing = fetch_california_housing(as_frame=True)
        df = housing.frame.copy()
    except:
        # Fallback (important for cloud stability)
        url = "https://raw.githubusercontent.com/ageron/handson-ml/master/datasets/housing/housing.csv"
        df = pd.read_csv(url)
        df.rename(columns={"median_house_value": "MedHouseVal"}, inplace=True)
    
    # Feature Engineering
    df["PopulationDensity"] = df["Population"] / df["AveOccup"]
    
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("🔎 Filter Options")

# Income Slider
min_income = float(df["MedInc"].min())
max_income = float(df["MedInc"].max())

income_range = st.sidebar.slider(
    "Median Income Range",
    min_value=min_income,
    max_value=max_income,
    value=(min_income, max_income)
)

# Filter dataset
filtered_df = df[
    (df["MedInc"] >= income_range[0]) &
    (df["MedInc"] <= income_range[1])
]

st.sidebar.write(f"📊 Filtered Rows: {filtered_df.shape[0]}")

# Layout (Columns)
col1, col2 = st.columns(2)

# Map Visualization (Advanced)
with col1:
    st.subheader("📍 House Value Map")

    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=filtered_df["Latitude"].mean(),
            longitude=filtered_df["Longitude"].mean(),
            zoom=5,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=filtered_df,
                get_position='[Longitude, Latitude]',
                get_radius=20000,
                get_fill_color='[200, 30, 0, 160]',
                pickable=True,
            ),
        ],
        tooltip={"text": "House Value: {MedHouseVal}"}
    ))

# Scatter Plot
with col2:
    st.subheader("📊 Income vs House Value")

    st.scatter_chart(
        filtered_df,
        x="MedInc",
        y="MedHouseVal"
    )

# Histogram
st.subheader("📈 Distribution of House Values")

st.bar_chart(filtered_df["MedHouseVal"].value_counts().sort_index())

# Summary Statistics
st.subheader("📋 Summary Statistics")
st.dataframe(filtered_df.describe())
