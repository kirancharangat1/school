import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("your_dataset.csv")

# List of ethnicity columns
ethnic_columns = [
    'American Indian / Alaskan Native', 
    'Asian', 
    'Black or African American', 
    'Hispanic', 
    'Native Hawaiian or other Pacific Islander(not hispanic)', 
    'Multi-Racial', 
    'White'
]

# Dropdown with "All" added
districts = ["All"] + sorted(df['DISTRICT_NAME'].unique().tolist())
district = st.selectbox("Select a School District", districts)

# --- Prepare data ---
if district == "All":
    # Aggregate across all districts
    district_data = df.copy()
    gender_data = district_data.groupby("GIFTED_TALENTED")[["Male", "Female"]].sum().reset_index()
else:
    # Filter to one district
    district_data = df[df['DISTRICT_NAME'] == district]
    gender_data = district_data[["GIFTED_TALENTED", "Male", "Female"]]

# --- Bar chart (Gifted Talented by Gender) ---
bar_data = gender_data.melt(
    id_vars=["GIFTED_TALENTED"],
    value_vars=["Male", "Female"],
    var_name="Gender",
    value_name="Count"
)

bar_fig = px.bar(
    bar_data,
    x="GIFTED_TALENTED",
    y="Count",
    color="Gender",
    barmode="group",
    title=f"Gifted Talented Distribution by Gender - {district}"
)

# --- Pie chart (Ethnicity) ---
ethnic_data = district_data[ethnic_columns].sum().reset_index()
ethnic_data.columns = ["Ethnicity", "Count"]

pie_fig = px.pie(
    ethnic_data,
    names="Ethnicity",
    values="Count",
    title=f"Ethnicity Breakdown - {district}"
)

# --- Display vertically ---
st.plotly_chart(bar_fig, use_container_width=True)
st.plotly_chart(pie_fig, use_container_width=True)
